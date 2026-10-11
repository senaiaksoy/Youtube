"""Tiny local server: serves work/thumb_ar and accepts POST /save (PNG) -> converts to final.jpg. Stops after the first save."""
import http.server, io, threading
from pathlib import Path
from PIL import Image

ROOT = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review\work\thumb_ar")


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(n)
        im = Image.open(io.BytesIO(data)).convert("RGB")
        im.save(ROOT / "final.png")
        im.save(ROOT / "echo-fiv-thumb-AR.jpg", quality=92, optimize=True)
        self.send_response(200); self.end_headers(); self.wfile.write(f"{im.size}".encode())
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H)
print("serving on 8765", flush=True)
srv.serve_forever()
print("saved", flush=True)
