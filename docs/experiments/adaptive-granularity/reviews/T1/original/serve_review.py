from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import threading, time

ROOT = Path(__file__).resolve().parents[1]
servers = []
for i in range(1, 4):
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT / f'variant-{i:02d}'))
    server = ThreadingHTTPServer(('127.0.0.1', 8210 + i), handler)
    servers.append(server)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f'variant-{i:02d}: http://127.0.0.1:{8210+i}/final/', flush=True)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    for server in servers:
        server.shutdown()
