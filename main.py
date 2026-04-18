"""
Sistema de Gestión para Librerías
main.py — Servidor HTTP local. Ejecutá este archivo para iniciar la aplicación.
"""

import os, sys, json, sqlite3, hashlib, base64, webbrowser, threading, mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
HTML_FILE  = os.path.join(BASE_DIR, "app.html")
DATA_DIR   = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DB_CAT     = os.path.join(DATA_DIR, "catalogo.db")
DB_VEN     = os.path.join(DATA_DIR, "ventas.db")
DB_APP     = os.path.join(DATA_DIR, "app.db")
HOST, PORT = "127.0.0.1", 8765

MIME_MAP = {
    "html": "text/html; charset=utf-8", "css": "text/css",
    "js": "application/javascript",     "png": "image/png",
    "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif",
    "svg": "image/svg+xml", "ico": "image/x-icon",
    "webp": "image/webp",  "json": "application/json",
}

# ══ Hashing ═══════════════════════════════════════════════════════════════════
def hp(p): return hashlib.sha256(p.encode()).hexdigest()

# ══ DB init ═══════════════════════════════════════════════════════════════════
def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    # ── app.db: config + usuarios ─────────────────────────────────────────────
    c = sqlite3.connect(DB_APP)
    c.execute("""CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY, value TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nombre   TEXT)""")
    c.commit()

    # Primer arranque: no hay usuarios → configuración inicial pendiente
    first = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0] == 0
    if first:
        set_cfg_raw(c, "setup_done", "false")
        print("[DB] Primera ejecución — se mostrará asistente de configuración.")
    c.commit(); c.close()

    # ── catalogo.db ───────────────────────────────────────────────────────────
    c = sqlite3.connect(DB_CAT)
    c.execute("""CREATE TABLE IF NOT EXISTS libros (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo     TEXT NOT NULL,
        autor      TEXT NOT NULL,
        ano        INTEGER,
        isbn       TEXT,
        digital    TEXT DEFAULT 'No',
        imprenta   TEXT DEFAULT 'No',
        ejemplares INTEGER DEFAULT 0,
        stock      TEXT DEFAULT 'Si')""")
    _migrate_libros(c)
    c.commit(); c.close()

    # ── ventas.db ─────────────────────────────────────────────────────────────
    c = sqlite3.connect(DB_VEN)
    c.execute("""CREATE TABLE IF NOT EXISTS ventas (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha    TEXT,
        cliente  TEXT,
        tienda   TEXT,
        evento   TEXT,
        libro    TEXT,
        cantidad INTEGER,
        precio   REAL,
        total    REAL)""")
    _migrate_ventas(c)
    c.commit(); c.close()

    print("[DB] Bases de datos listas.")

def _migrate_libros(c):
    cols = [r[1] for r in c.execute("PRAGMA table_info(libros)").fetchall()]
    if cols and "titulo" not in cols:
        try:
            c.execute("ALTER TABLE libros RENAME TO _libros_old")
            c.execute("""CREATE TABLE libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT, autor TEXT, ano INTEGER, isbn TEXT,
                digital TEXT, imprenta TEXT, ejemplares INTEGER, stock TEXT)""")
            old = [r[1] for r in c.execute("PRAGMA table_info(_libros_old)").fetchall()]
            if "Libro" in old:
                c.execute("""INSERT INTO libros (titulo,autor,ano,isbn,digital,imprenta,ejemplares,stock)
                    SELECT "Libro","Autor","Año","ISBN","Versión Digital","En Imprenta","Ejemplares","En Stock"
                    FROM _libros_old""")
            c.execute("DROP TABLE IF EXISTS _libros_old")
            print("[DB] Catálogo migrado.")
        except Exception as e:
            print(f"[DB] Aviso migración catálogo: {e}")

def _migrate_ventas(c):
    cols = [r[1] for r in c.execute("PRAGMA table_info(ventas)").fetchall()]
    if cols and "cliente" not in cols:
        try:
            c.execute("ALTER TABLE ventas RENAME TO _ventas_old")
            c.execute("""CREATE TABLE ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT, cliente TEXT, tienda TEXT, evento TEXT,
                libro TEXT, cantidad INTEGER, precio REAL, total REAL)""")
            old = [r[1] for r in c.execute("PRAGMA table_info(_ventas_old)").fetchall()]
            if "Cliente" in old:
                c.execute("""INSERT INTO ventas (fecha,cliente,tienda,evento,libro,cantidad,precio,total)
                    SELECT "Fecha","Cliente","Tienda","Evento","Libro","Cantidad","Importe Unitario","Total"
                    FROM _ventas_old""")
            c.execute("DROP TABLE IF EXISTS _ventas_old")
            print("[DB] Ventas migradas.")
        except Exception as e:
            print(f"[DB] Aviso migración ventas: {e}")

# ══ Config helpers ═════════════════════════════════════════════════════════════
def set_cfg_raw(c, key, value):
    c.execute("INSERT OR REPLACE INTO config VALUES(?,?)", (key, value))

def get_cfg(key):
    c = sqlite3.connect(DB_APP)
    r = c.execute("SELECT value FROM config WHERE key=?", (key,)).fetchone()
    c.close()
    return r[0] if r else None

def set_cfg(key, value):
    c = sqlite3.connect(DB_APP)
    c.execute("INSERT OR REPLACE INTO config VALUES(?,?)", (key, value))
    c.commit(); c.close()

def get_all_cfg():
    c = sqlite3.connect(DB_APP)
    rows = c.execute("SELECT key,value FROM config").fetchall()
    c.close()
    return {r[0]: r[1] for r in rows}

# ══ Auth helpers ═══════════════════════════════════════════════════════════════
def verify(username, password):
    c = sqlite3.connect(DB_APP)
    r = c.execute("SELECT password FROM usuarios WHERE username=?", (username,)).fetchone()
    c.close()
    return r and r[0] == hp(password)

def create_user(username, password, nombre=""):
    c = sqlite3.connect(DB_APP)
    try:
        c.execute("INSERT INTO usuarios (username,password,nombre) VALUES(?,?,?)",
                  (username, hp(password), nombre))
        c.commit(); c.close()
        return True
    except sqlite3.IntegrityError:
        c.close()
        return False

def change_password(username, new_password):
    c = sqlite3.connect(DB_APP)
    c.execute("UPDATE usuarios SET password=? WHERE username=?", (hp(new_password), username))
    c.commit(); c.close()

# ══ Business queries ═══════════════════════════════════════════════════════════
def qall(db, tbl):
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row
    rows = [dict(r) for r in c.execute(f"SELECT * FROM {tbl} ORDER BY id").fetchall()]
    c.close(); return rows

def ins_libro(d):
    c = sqlite3.connect(DB_CAT)
    cur = c.execute(
        "INSERT INTO libros (titulo,autor,ano,isbn,digital,imprenta,ejemplares,stock) VALUES(?,?,?,?,?,?,?,?)",
        (d.get("titulo",""), d.get("autor",""), int(d.get("ano") or 0) or None,
         d.get("isbn",""), d.get("digital","No"), d.get("imprenta","No"),
         int(d.get("ejemplares") or 0), d.get("stock","Si")))
    n = cur.lastrowid; c.commit(); c.close(); return n

def upd_libro(lid, d):
    c = sqlite3.connect(DB_CAT)
    c.execute("UPDATE libros SET titulo=?,autor=?,ano=?,isbn=?,digital=?,imprenta=?,ejemplares=?,stock=? WHERE id=?",
        (d.get("titulo",""), d.get("autor",""), int(d.get("ano") or 0) or None,
         d.get("isbn",""), d.get("digital","No"), d.get("imprenta","No"),
         int(d.get("ejemplares") or 0), d.get("stock","Si"), lid))
    c.commit(); c.close()

def del_libro(lid):
    c = sqlite3.connect(DB_CAT)
    c.execute("DELETE FROM libros WHERE id=?", (lid,)); c.commit(); c.close()

def ins_venta(d):
    total = float(d.get("cantidad", 0)) * float(d.get("precio", 0))
    c = sqlite3.connect(DB_VEN)
    cur = c.execute(
        "INSERT INTO ventas (fecha,cliente,tienda,evento,libro,cantidad,precio,total) VALUES(?,?,?,?,?,?,?,?)",
        (d.get("fecha",""), d.get("cliente",""), d.get("tienda",""), d.get("evento",""),
         d.get("libro",""), int(d.get("cantidad") or 0), float(d.get("precio") or 0), total))
    n = cur.lastrowid; c.commit(); c.close(); return n, total

def del_venta(vid):
    c = sqlite3.connect(DB_VEN)
    c.execute("DELETE FROM ventas WHERE id=?", (vid,)); c.commit(); c.close()

# ══ HTTP Handler ═══════════════════════════════════════════════════════════════
class H(BaseHTTPRequestHandler):

    def log_message(self, fmt, *a):
        if a and str(a[1]) not in ("200", "204"):
            print(f"  [HTTP] {a[0]}  →  {a[1]}")

    def jres(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def fres(self, path, mime="text/html; charset=utf-8"):
        with open(path, "rb") as f: data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n).decode()) if n else {}

    def nf(self): self.send_response(404); self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        for h,v in [("Access-Control-Allow-Origin","*"),
                    ("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS"),
                    ("Access-Control-Allow-Headers","Content-Type")]:
            self.send_header(h, v)
        self.end_headers()

    # ── GET ───────────────────────────────────────────────────────────────────
    def do_GET(self):
        p = urlparse(self.path).path

        if p in ("/", "/index.html"):
            self.fres(HTML_FILE, "text/html; charset=utf-8"); return

        if p.startswith("/assets/"):
            fname = os.path.basename(p)
            fp = os.path.join(ASSETS_DIR, fname)
            if os.path.isfile(fp):
                ext = fname.rsplit(".", 1)[-1].lower()
                self.fres(fp, MIME_MAP.get(ext, "application/octet-stream"))
            else:
                self.nf()
            return

        # ── API ───────────────────────────────────────────────────────────────
        if p == "/api/status":
            cfg = get_all_cfg()
            setup_done = cfg.get("setup_done", "false") == "true"
            self.jres({
                "ok": True,
                "setup_done": setup_done,
                "nombre_libreria": cfg.get("nombre_libreria", ""),
                "logo_filename":   cfg.get("logo_filename", ""),
                "theme":           cfg.get("theme", "dark"),
            }); return

        if p == "/api/libros":
            self.jres({"ok": True, "data": qall(DB_CAT, "libros")}); return

        if p == "/api/ventas":
            self.jres({"ok": True, "data": qall(DB_VEN, "ventas")}); return

        self.nf()

    # ── POST ──────────────────────────────────────────────────────────────────
    def do_POST(self):
        p = urlparse(self.path).path
        d = self.body()

        # ── Setup inicial ─────────────────────────────────────────────────────
        if p == "/api/setup":
            nombre    = d.get("nombre_libreria", "").strip()
            username  = d.get("username", "").strip()
            password  = d.get("password", "").strip()
            logo_b64  = d.get("logo_b64", "")       # data:image/...;base64,...
            logo_ext  = d.get("logo_ext", "png")
            theme     = d.get("theme", "dark")

            if not nombre or not username or not password:
                self.jres({"ok": False, "error": "Nombre, usuario y contraseña son obligatorios"}, 400); return
            if len(password) < 6:
                self.jres({"ok": False, "error": "La contraseña debe tener al menos 6 caracteres"}, 400); return

            # Guardar logo si se proporcionó
            logo_filename = ""
            if logo_b64 and ";base64," in logo_b64:
                try:
                    raw = base64.b64decode(logo_b64.split(";base64,")[1])
                    logo_filename = f"logo_libreria.{logo_ext}"
                    with open(os.path.join(ASSETS_DIR, logo_filename), "wb") as f:
                        f.write(raw)
                except Exception as e:
                    print(f"[LOGO] Error guardando logo: {e}")

            if not create_user(username, password, nombre):
                self.jres({"ok": False, "error": "Ese nombre de usuario ya existe"}, 409); return

            set_cfg("nombre_libreria", nombre)
            set_cfg("logo_filename",   logo_filename)
            set_cfg("theme",           theme)
            set_cfg("setup_done",      "true")
            print(f"[SETUP] Librería configurada: '{nombre}' | usuario: '{username}'")
            self.jres({"ok": True}); return

        # ── Login ─────────────────────────────────────────────────────────────
        if p == "/api/login":
            u = d.get("username", "").strip()
            pw = d.get("password", "")
            if verify(u, pw):
                cfg = get_all_cfg()
                self.jres({
                    "ok": True,
                    "nombre_libreria": cfg.get("nombre_libreria", ""),
                    "logo_filename":   cfg.get("logo_filename", ""),
                    "theme":           cfg.get("theme", "dark"),
                })
            else:
                self.jres({"ok": False, "error": "Usuario o contraseña incorrectos"}, 401)
            return

        # ── Cambiar contraseña ────────────────────────────────────────────────
        if p == "/api/change-password":
            u    = d.get("username", "").strip()
            old  = d.get("old_password", "")
            new  = d.get("new_password", "").strip()
            if len(new) < 6:
                self.jres({"ok": False, "error": "Mínimo 6 caracteres"}, 400); return
            if not verify(u, old):
                self.jres({"ok": False, "error": "Contraseña actual incorrecta"}, 401); return
            change_password(u, new)
            self.jres({"ok": True}); return

        # ── Cambiar configuración de librería ─────────────────────────────────
        if p == "/api/config":
            for key in ("nombre_libreria", "theme"):
                if key in d:
                    set_cfg(key, d[key])
            # Logo nuevo
            logo_b64 = d.get("logo_b64", "")
            logo_ext = d.get("logo_ext", "png")
            if logo_b64 and ";base64," in logo_b64:
                try:
                    raw = base64.b64decode(logo_b64.split(";base64,")[1])
                    logo_filename = f"logo_libreria.{logo_ext}"
                    with open(os.path.join(ASSETS_DIR, logo_filename), "wb") as f:
                        f.write(raw)
                    set_cfg("logo_filename", logo_filename)
                except Exception as e:
                    print(f"[LOGO] Error actualizando logo: {e}")
            self.jres({"ok": True, "config": get_all_cfg()}); return

        # ── Libros ────────────────────────────────────────────────────────────
        if p == "/api/libros":
            if not d.get("titulo") or not d.get("autor"):
                self.jres({"ok": False, "error": "Título y autor son obligatorios"}, 400); return
            self.jres({"ok": True, "id": ins_libro(d)}); return

        # ── Ventas ────────────────────────────────────────────────────────────
        if p == "/api/ventas":
            if not d.get("cliente") or not d.get("libro"):
                self.jres({"ok": False, "error": "Cliente y libro son obligatorios"}, 400); return
            nid, total = ins_venta(d)
            self.jres({"ok": True, "id": nid, "total": total}); return

        self.nf()

    # ── PUT ───────────────────────────────────────────────────────────────────
    def do_PUT(self):
        p = urlparse(self.path).path; d = self.body()
        pts = p.strip("/").split("/")
        if len(pts) == 3 and pts[0] == "api" and pts[1] == "libros":
            try: upd_libro(int(pts[2]), d); self.jres({"ok": True})
            except Exception as e: self.jres({"ok": False, "error": str(e)}, 400)
        else: self.nf()

    # ── DELETE ────────────────────────────────────────────────────────────────
    def do_DELETE(self):
        p = urlparse(self.path).path
        pts = p.strip("/").split("/")
        if len(pts) == 3 and pts[0] == "api":
            try:
                rid = int(pts[2])
                if   pts[1] == "libros": del_libro(rid)
                elif pts[1] == "ventas": del_venta(rid)
                else: self.nf(); return
                self.jres({"ok": True})
            except Exception as e:
                self.jres({"ok": False, "error": str(e)}, 400)
        else: self.nf()

# ══ Arranque ══════════════════════════════════════════════════════════════════
def main():
    init_db()
    server = HTTPServer((HOST, PORT), H)
    url = f"http://{HOST}:{PORT}"
    print()
    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║   Sistema de Gestión para Librerías           ║")
    print("  ╚═══════════════════════════════════════════════╝")
    print(f"  Servidor activo:  {url}")
    print(f"  Datos:            {DATA_DIR}")
    print(f"  Ctrl+C para detener.")
    print()
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  [✓] Servidor detenido.")
        sys.exit(0)

if __name__ == "__main__":
    main()
