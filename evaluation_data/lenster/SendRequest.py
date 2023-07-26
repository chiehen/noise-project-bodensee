import os
import socket
import sys
import time

# Using env vars because at noise creation the project-specific values are unavailable
base = os.environ.get('BASE_SEND_REQUEST')
if base is None:
    raise ValueError("BASE_SEND_REQUEST environment variable is not set")

port = os.environ.get('PORT_SEND_REQUEST')
if port is None:
    raise ValueError("PORT_SEND_REQUEST environment variable is not set")
port = int(port)

timeout = float(sys.argv[2])
if timeout is None:
    print("No timeout value provided, using default value 1")
    timeout = 1

print(f"SendRequest targets {base} {port}, with timeout {timeout} seconds")

headers = """\
POST /auth HTTP/1.1\r
Content-Type: text/plain\r
Content-Length: {content_length}\r
Host: localhost:9000\r\n
Connection: close\r
\r\n"""
body = 'a' * 100
body_bytes = body.encode('ascii')
header_bytes = headers.format(
    content_length=len(body_bytes),
).encode('ascii')
payload = header_bytes + body_bytes
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((base, port))
        s.sendto(payload, (base, port))
        s.close()
    except ConnectionRefusedError:
        print("[ConstantNoise]: Can't connect to app")
    time.sleep(timeout)
