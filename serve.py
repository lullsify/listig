import socket, os, mimetypes

ROOT = '/Users/lovisafast/Desktop/minlistor'
PORT = 4200

srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(('', PORT))
srv.listen(5)

while True:
    conn, _ = srv.accept()
    data = b''
    while b'\r\n\r\n' not in data:
        data += conn.recv(4096)
    line = data.split(b'\r\n')[0].decode()
    path = line.split(' ')[1].split('?')[0]
    if path == '/': path = '/index.html'
    fpath = ROOT + path
    try:
        with open(fpath, 'rb') as f:
            body = f.read()
        mt = mimetypes.guess_type(fpath)[0] or 'text/plain'
        conn.sendall(f'HTTP/1.1 200 OK\r\nContent-Type: {mt}\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n'.encode() + body)
    except:
        conn.sendall(b'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n')
    conn.close()
