#!/usr/bin/env python3
"""Minimal HTTP server for Pusat Generator Instrumen Ajar SMA.

Serves static files and provides a single POST /api/generate endpoint
that forwards structured requests to an AI provider (OpenAI by default).
"""

import base64
import hashlib
import hmac
import json
import os
import re
import ssl
import time
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("PORT", 5000))
AI_API_KEY = os.environ.get("AI_API_KEY", "").strip()
AI_BASE_URL = os.environ.get("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
AI_MODEL = os.environ.get("AI_MODEL", "gpt-4o-mini")

# Admin & storage configuration ---------------------------------------------
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "").strip()
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "").strip()
SESSION_SECRET = os.environ.get("SESSION_SECRET", "replit-default-session-secret")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CP_STORAGE_PATH = os.path.join(DATA_DIR, "cp-storage.json")

# Guru credentials (existing login kept — role = "guru", no CP management).
GURU_USERNAME = "guru"
GURU_PASSWORD = "merdeka2026"

AGAMA_MAPEL = {"PAI", "PAK", "Katolik", "Hindu", "Buddha"}
AGAMA_REGULASI = {
    "institution": "Kemendikdasmen",
    "regulation": "Keputusan Kepala BKPDM",
    "number": "020",
    "year": "2026",
}
NON_AGAMA_REGULASI = {
    "institution": "Kemendikdasmen",
    "regulation": "Keputusan Kepala BSKAP",
    "number": "046/H/KR/2025",
    "year": "2025",
}
SESSION_TTL_SECONDS = 24 * 60 * 60

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
    kegiatan_terms = (
        "kegiatan pembelajaran",
        "langkah-langkah pembelajaran",
        "langkah pembelajaran",
        "kegiatan belajar",
        "aktivitas pembelajaran",
        "sintaks",
    )
    asesmen_terms = ("asesmen", "penilaian", "evaluasi", "assessment")
    checks = {
        "capaian pembelajaran": "capaian pembelajaran" in lowered,
        "tujuan pembelajaran": "tujuan pembelajaran" in lowered,
        "kegiatan pembelajaran": any(t in lowered for t in kegiatan_terms),
        "asesmen": any(t in lowered for t in asesmen_terms),
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

    # ------------------------------------------------------------------
    def log_message(self, format, *args):
        # Quieter access log; keep errors visible.
        try:
            msg = format % args
            if " 5" in msg.split('"')[1] or " 4" in msg.split('"')[1]:
                super().log_message(format, *args)
        except Exception:
            pass

    def send_json(self, obj, status=200, extra_headers=None):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return None
        try:
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw)
        except Exception:
            return None

    # ------------------------------------------------------------------
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/login-status":
            self.send_json({
                "logged_in": is_logged_in(self),
                "admin": is_admin(self),
                "role": session_role(self),
                "admin_username_configured": bool(ADMIN_USERNAME),
                "admin_password_configured": bool(ADMIN_PASSWORD),
            })
            return
        if parsed.path == "/api/admin/status":
            self.send_json({
                "admin": is_admin(self),
                "role": session_role(self),
                "admin_username_configured": bool(ADMIN_USERNAME),
                "admin_password_configured": bool(ADMIN_PASSWORD),
            })
            return
        if parsed.path == "/api/admin/cp":
            if not is_admin(self):
                self.send_json({"error": "Unauthorized"}, status=401)
                return
            self.send_json(load_storage())
            return
        if parsed.path == "/api/cp":
            # Public read-only endpoint: any role (guru included) can fetch CP.
            # Admin-published CP are persisted on the server in CP storage;
            # the loaded storage is the source of truth (overlay default seed
            # already lives on the frontend, so do not return empty for non-admin).
            qs = parse_qs(parsed.query)
            data = load_storage()
            mapel_q = (qs.get("mapel") or [""])[0]
            fase_q = (qs.get("fase") or [""])[0]
            if mapel_q and fase_q in ("E", "F"):
                entry = (data.get(mapel_q) or {}).get(fase_q)
                if entry:
                    self.send_json({"entry": entry, "source": "admin"})
                else:
                    self.send_json({"entry": None, "source": "admin"})
                return
            self.send_json({"storage": data, "source": "admin"})
            return
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/login":
            data = self.read_json_body()
            if not isinstance(data, dict):
                self.send_json({"success": False, "message": "Body tidak valid."}, status=400)
                return
            u = (data.get("username") or "").strip()
            p = (data.get("password") or "").strip()

            # Guru login (legacy). Single endpoint memeriksa kedua-duanya; backend menentukan role.
            if hmac.compare_digest(u, GURU_USERNAME) and hmac.compare_digest(p, GURU_PASSWORD):
                token = make_session_token("guru")
                cookie = (
                    f"guru_session={token}; Path=/; HttpOnly; SameSite=Strict; "
                    f"Max-Age={SESSION_TTL_SECONDS}"
                )
                self.send_json(
                    {"success": True, "role": "guru"},
                    extra_headers={"Set-Cookie": cookie},
                )
                return

            # Admin login diverifikasi server-side dari env vars. Frontend tidak pernah memvalidasi.
            if ADMIN_USERNAME and ADMIN_PASSWORD:
                if hmac.compare_digest(u, ADMIN_USERNAME) and hmac.compare_digest(p, ADMIN_PASSWORD):
                    token = make_session_token("admin")
                    cookie = (
                        f"admin_session={token}; Path=/; HttpOnly; SameSite=Strict; "
                        f"Max-Age={SESSION_TTL_SECONDS}"
                    )
                    self.send_json(
                        {"success": True, "role": "admin"},
                        extra_headers={"Set-Cookie": cookie},
                    )
                    return

            if not ADMIN_USERNAME or not ADMIN_PASSWORD:
                self.send_json(
                    {"success": False, "message": "ADMIN_USERNAME / ADMIN_PASSWORD belum dikonfigurasi."},
                    status=503,
                )
                return
            self.send_json(
                {"success": False, "message": "Username atau password salah"},
                status=401,
            )
            return

        if parsed.path in ("/api/auth/login", "/api/auth/admin-login", "/api/admin/login"):
            # Backward-compat alias with legacy response shape.
            data = self.read_json_body()
            if not isinstance(data, dict):
                self.send_json({"error": "Body tidak valid."}, status=400)
                return
            u = (data.get("username") or "").strip()
            p = (data.get("password") or "").strip()
            if hmac.compare_digest(u, GURU_USERNAME) and hmac.compare_digest(p, GURU_PASSWORD):
                token = make_session_token("guru")
                cookie = (
                    f"guru_session={token}; Path=/; HttpOnly; SameSite=Strict; "
                    f"Max-Age={SESSION_TTL_SECONDS}"
                )
                self.send_json({"ok": True, "role": "guru"}, extra_headers={"Set-Cookie": cookie})
                return
            if ADMIN_USERNAME and ADMIN_PASSWORD:
                if hmac.compare_digest(u, ADMIN_USERNAME) and hmac.compare_digest(p, ADMIN_PASSWORD):
                    token = make_session_token("admin")
                    cookie = (
                        f"admin_session={token}; Path=/; HttpOnly; SameSite=Strict; "
                        f"Max-Age={SESSION_TTL_SECONDS}"
                    )
                    self.send_json({"ok": True, "role": "admin"}, extra_headers={"Set-Cookie": cookie})
                    return
            if not ADMIN_USERNAME or not ADMIN_PASSWORD:
                self.send_json({"error": "ADMIN_USERNAME / ADMIN_PASSWORD belum dikonfigurasi."}, status=503)
                return
            self.send_json({"error": "Username atau password salah."}, status=401)
            return

        if parsed.path in ("/api/auth/logout", "/api/admin/logout"):
            # Clear both cookie names so a single logout ends every session.
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Set-Cookie", "admin_session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0")
            self.send_header("Set-Cookie", "guru_session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))
            return

        if parsed.path == "/api/admin/cp":
            if not is_admin(self):
                self.send_json({"error": "Unauthorized"}, status=401)
                return
            data = self.read_json_body()
            err = validate_cp_payload(data)
            if err:
                self.send_json({"error": err}, status=400)
                return
            mapel = data["mapel"]
            fase = data["fase"]
            source = regulasi_untuk(mapel).copy()
            source["status"] = "active"
            entry = {
                "mapel": mapel,
                "fase": fase,
                "cp": data["cp"].strip(),
                "elements": data.get("elements") or [],
                "source": source,
            }
            storage = load_storage()
            storage.setdefault(mapel, {})[fase] = entry
            save_storage(storage)
            self.send_json({"ok": True, "entry": entry})
            return

        if parsed.path == "/api/generate":
            data = self.read_json_body()
            if data is None:
                self.send_json({"error": "Body kosong atau JSON tidak valid."}, status=400)
                return
            result = call_ai(data)
            status = 200 if "html" in result else 500
            self.send_json(result, status=status)
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not found")

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/admin/cp":
            self.send_response(404)
            self.end_headers()
            return
        if not is_admin(self):
            self.send_json({"error": "Unauthorized"}, status=401)
            return
        qs = parse_qs(parsed.query)
        mapel = (qs.get("mapel") or [""])[0]
        fase = (qs.get("fase") or [""])[0]
        if not mapel or fase not in ("E", "F"):
            self.send_json({"error": "mapel & fase wajib."}, status=400)
            return
        storage = load_storage()
        if mapel in storage and fase in storage[mapel]:
            del storage[mapel][fase]
            if not storage[mapel]:
                del storage[mapel]
            save_storage(storage)
            self.send_json({"ok": True})
        else:
            self.send_json({"error": "Entry tidak ditemukan."}, status=404)


# ---------------------------------------------------------------------------
# Admin helpers
# ---------------------------------------------------------------------------
def kategori_mapel(mapel):
    return "agama" if mapel in AGAMA_MAPEL else "non_agama"


def regulasi_untuk(mapel):
    return dict(AGAMA_REGULASI if mapel in AGAMA_MAPEL else NON_AGAMA_REGULASI)


def make_session_token(role):
    ts = str(int(time.time()))
    payload = f"{role}|{ts}"
    sig = hmac.new(SESSION_SECRET.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{role}|{ts}.{sig}"


def verify_role_cookie(cookie_header, expected_role):
    if not cookie_header:
        return False
    token = None
    cookie_name = "admin_session" if expected_role == "admin" else "guru_session"
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith(f"{cookie_name}="):
            token = part[len(cookie_name) + 1:]
            break
    if not token:
        return False
    try:
        role, rest = token.split("|", 1)
        ts, sig = rest.split(".", 1)
        if role != expected_role:
            return False
        payload = f"{role}|{ts}"
        expected = hmac.new(SESSION_SECRET.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return False
        return (time.time() - int(ts)) < SESSION_TTL_SECONDS
    except Exception:
        return False


def verify_session(cookie_header):
    # Backward compatible: admin session check.
    return verify_role_cookie(cookie_header, "admin")


def is_admin(handler):
    return verify_role_cookie(handler.headers.get("Cookie", ""), "admin")


def is_guru(handler):
    return verify_role_cookie(handler.headers.get("Cookie", ""), "guru")


def session_role(handler):
    for role in ("admin", "guru"):
        if verify_role_cookie(handler.headers.get("Cookie", ""), role):
            return role
    return None


def is_logged_in(handler):
    return session_role(handler) is not None


def load_storage():
    if not os.path.exists(CP_STORAGE_PATH):
        return {}
    try:
        with open(CP_STORAGE_PATH, "r", encoding="utf-8") as f:
            return json.loads(f.read() or "{}")
    except Exception:
        return {}


def save_storage(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = CP_STORAGE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, CP_STORAGE_PATH)


def validate_cp_payload(data):
    if not isinstance(data, dict):
        return "Body tidak valid."
    mapel = (data.get("mapel") or "").strip()
    fase = (data.get("fase") or "").strip()
    cp_text = (data.get("cp") or "").strip()
    if not mapel:
        return "Mata pelajaran wajib diisi."
    if fase not in ("E", "F"):
        return "Fase harus E atau F."
    if not cp_text:
        return "Capaian Pembelajaran tidak boleh kosong."
    expected_year = regulasi_untuk(mapel)["year"]
    provided_year = str(data.get("year") or "").strip() or expected_year
    if provided_year != expected_year:
        kategori = kategori_mapel(mapel)
        return f"Tahun regulasi tidak sesuai. Mapel {kategori} harus {expected_year}."
    elements = data.get("elements")
    if elements is not None and not isinstance(elements, list):
        return "Elemen CP harus berupa daftar."
    if isinstance(elements, list):
        for idx, item in enumerate(elements):
            if not isinstance(item, dict):
                return f"Elemen #{idx + 1} tidak valid."
            if "name" not in item or "cp" not in item:
                return f"Elemen #{idx + 1} harus memiliki name dan cp."
    return None


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), RequestHandler)
    print(f"Serving on port {PORT}")
    server.serve_forever()
