#!/usr/bin/env python3
"""Minimal HTTP server for Pusat Generator Instrumen Ajar SMA.

Serves static files and provides a single POST /api/generate endpoint
that forwards structured requests to an AI provider (OpenAI by default).
"""

import json
import os
import re
import ssl
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = int(os.environ.get("PORT", 5000))
AI_API_KEY = os.environ.get("AI_API_KEY", "").strip()
AI_BASE_URL = os.environ.get("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
AI_MODEL = os.environ.get("AI_MODEL", "gpt-4o-mini")

ALLOWED_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6", "p", "br", "ul", "ol", "li", "table",
    "thead", "tbody", "tr", "th", "td", "strong", "b", "em", "i", "u", "span",
    "div", "blockquote", "sup", "sub"
}
ALLOWED_ATTRS = {"colspan", "rowspan", "style"}


def sanitize_html(raw: str) -> str:
    """Strip everything except a simple whitelist of HTML tags and attributes."""
    if not raw:
        return ""
    # Remove script/style/iframe tags and their contents
    raw = re.sub(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", raw, flags=re.IGNORECASE | re.DOTALL)
    raw = re.sub(r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>", "", raw, flags=re.IGNORECASE | re.DOTALL)
    raw = re.sub(r"<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>", "", raw, flags=re.IGNORECASE | re.DOTALL)
    # Remove event handlers and javascript: URLs
    raw = re.sub(r"\s*on\w+\s*=\s*['\"].*?['\"]", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s*on\w+\s*=\s*[^\s>]+", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"javascript:\s*[^\"'>]+", "", raw, flags=re.IGNORECASE)

    def tag_replacer(match):
        tag = match.group(1).lower()
        if tag.startswith("/"):
            closing = tag[1:]
            if closing in ALLOWED_TAGS:
                return f"</{closing}>"
            return ""
        if tag in ALLOWED_TAGS:
            attrs = match.group(2) or ""
            cleaned_attrs = ""
            for attr_match in re.finditer(r"(\w+)\s*=\s*['\"](.*?)['\"]", attrs, flags=re.IGNORECASE):
                name, value = attr_match.group(1).lower(), attr_match.group(2)
                if name in ALLOWED_ATTRS:
                    cleaned_attrs += f' {name}="{value}"'
            return f"<{tag}{cleaned_attrs}>"
        return ""

    return re.sub(r"<\s*(/?\w+)([^>]*)\s*>", tag_replacer, raw)


def build_system_prompt() -> str:
    return (
        "ANDA ADALAH MESIN PENYUSUN DOKUMEN PEMBELAJARAN SMA.\n"
        "SUMBER KEBENARAN UTAMA ADALAH CAPAIAN PEMBELAJARAN YANG DIKIRIM APLIKASI.\n\n"
        "ATURAN:\n"
        "1. Jangan membuat CP baru.\n"
        "2. Jangan mengubah redaksi CP.\n"
        "3. Jangan menggunakan CP dari pengetahuan internal model.\n"
        "4. Jangan mengganti fase.\n"
        "5. Jangan menambahkan kompetensi yang bertentangan dengan CP.\n"
        "6. Tujuan Pembelajaran harus dapat ditelusuri ke CP.\n"
        "7. Kegiatan pembelajaran harus mendukung TP.\n"
        "8. Asesmen harus mengukur TP.\n"
        "9. Jika data tidak cukup, nyatakan bahwa data tidak cukup.\n"
        "10. Jangan mengarang regulasi.\n"
        "11. Jangan mengarang nomor keputusan.\n"
        "12. Gunakan Bahasa Indonesia formal untuk dokumen.\n"
        "13. Konten Bahasa Inggris boleh digunakan sesuai kebutuhan mata pelajaran.\n"
        "14. Hasil harus siap ditampilkan dalam dokumen guru.\n"
        "15. Gunakan tag HTML sederhana: h1, h2, h3, p, ul, li, table, tr, th, td.\n"
        "16. Jangan gunakan tag script, iframe, javascript, atau event handler.\n"
        "17. Jangan membuat asesmen yang tidak mengukur TP.\n"
    )


def build_user_prompt(payload: dict) -> str:
    elements = payload.get("elements") or []
    elements_text = "\n".join(
        f"- {e.get('name', '-')}:\n{e.get('cp', '-')}" for e in elements
    ) if elements else "Tidak ada elemen terpisah."

    return (
        f"CAPAIAN PEMBELAJARAN RESMI:\n{payload.get('cp', '')}\n\n"
        f"ELEMEN CP:\n{elements_text}\n\n"
        f"MATA PELAJARAN: {payload.get('mapel', '')}\n"
        f"FASE: {payload.get('fase', '')}\n"
        f"KELAS: {payload.get('kelas', '')}\n"
        f"SEMESTER: {payload.get('semester', '')}\n"
        f"TAHUN PELAJARAN: {payload.get('tahunPelajaran', '')}\n\n"
        f"TUJUAN PEMBELAJARAN:\n{payload.get('tp', '')}\n\n"
        f"MATERI: {payload.get('materi', '')}\n\n"
        f"ALOKASI: {payload.get('jp', '')} JP\n"
        f"JUMLAH PERTEMUAN: {payload.get('pertemuan', '')}\n\n"
        f"JENIS DOKUMEN: {payload.get('jenisDokumen', '')}\n\n"
        "Buat dokumen lengkap sesuai jenis dokumen di atas."
    )


def validate_ai_output(html: str):
    if not html or not html.strip():
        return False, ["output kosong"]
    lowered = html.lower()
    checks = {
        "capaian pembelajaran": "capaian pembelajaran" in lowered,
        "tujuan pembelajaran": "tujuan pembelajaran" in lowered,
        "kegiatan pembelajaran": (
            "kegiatan pembelajaran" in lowered
            or "langkah-langkah pembelajaran" in lowered
        ),
        "asesmen": ("asesmen" in lowered or "penilaian" in lowered),
    }
    missing = [name for name, present in checks.items() if not present]
    return (not missing), missing


def call_ai(payload: dict) -> dict:
    if not AI_API_KEY:
        return {"error": "AI API belum dikonfigurasi."}

    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(payload)

    request_body = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.4,
        "max_tokens": 4000,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AI_API_KEY}",
    }

    req = urllib.request.Request(
        f"{AI_BASE_URL}/chat/completions",
        data=json.dumps(request_body).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode("utf-8"))
            msg = detail.get("error", {}).get("message", str(e))
        except Exception:
            msg = str(e)
        return {"error": f"AI API gagal: {msg}"}
    except Exception as e:
        return {"error": f"AI API gagal: {str(e)}"}

    choices = body.get("choices") or []
    if not choices or not choices[0].get("message", {}).get("content"):
        return {"error": "Respons AI kosong."}

    raw_html = choices[0]["message"]["content"]
    # If the model wraps output in markdown code fences, unwrap it.
    if raw_html.strip().startswith("```html"):
        raw_html = raw_html.strip()[7:]
        if raw_html.endswith("```"):
            raw_html = raw_html[:-3]
    elif raw_html.strip().startswith("```"):
        raw_html = raw_html.strip()[3:]
        if raw_html.endswith("```"):
            raw_html = raw_html[:-3]

    raw_html = raw_html.strip()
    sanitized = sanitize_html(raw_html)
    ok, missing = validate_ai_output(sanitized)
    if not ok:
        # Persist what AI actually returned so we can diagnose intermittent validation failures.
        try:
            with open("/tmp/ai-last-response.html", "w") as f:
                f.write(sanitized)
        except Exception:
            pass
        return {"error": f"Hasil AI belum memenuhi struktur ({', '.join(missing)}). Silakan coba kembali."}

    return {"html": sanitized}


class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/generate":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Body kosong."}).encode("utf-8"))
            return

        try:
            body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(body)
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"JSON tidak valid: {str(e)}"}).encode("utf-8"))
            return

        result = call_ai(payload)
        status = 200 if "html" in result else 500
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), RequestHandler)
    print(f"Serving on port {PORT}")
    server.serve_forever()
