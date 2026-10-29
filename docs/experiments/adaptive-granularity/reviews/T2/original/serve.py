import http.server, threading, pathlib, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
for i in range(1,4):
    for stage,off in [('final',0),('initial',3)]:
        path=ROOT/f'variant-{i:02d}'/stage
        def factory(*a, directory=str(path), **kw):
            return http.server.SimpleHTTPRequestHandler(*a,directory=directory,**kw)
        server=http.server.ThreadingHTTPServer(('127.0.0.1',8080+i+off),factory)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        print(f'{path} -> http://127.0.0.1:{8080+i+off}',flush=True)
while True: time.sleep(30)
