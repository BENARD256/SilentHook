import socket
import threading
import requests
from flask import current_app

MYSQL_RSP = b"\x5b\x00\x00\x00\x0a\x38\x2e\x30\x2e\x32\x36\x2d\x30\x75\x62\x75\x6e\x74\x75\x30\x2e\x32\x30\x2e\x30\x34\x2e\x32\x00\x13\x00\x00\x00\x14\x37\x06\x5c\x3c\x26\x2a\x01\x00\xff\xf7\xff\x02\x00\xff\xcf\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x50\x3c\x16\x61\x26\x60\x49\x4f\x4b\x6d\x7a\x37\x00\x63\x61\x63\x68\x69\x6e\x67\x5f\x73\x68\x61\x32\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00"

# Tracks (token, ip) pairs already logged — prevents duplicate alerts
seen_connections = set()
seen_lock        = threading.Lock()

CALLBACK_BASE = "http://127.0.0.1:5000"  # update to BASE_URL in production


def notify_callback(token: str, source_ip: str):
    #Bridge MySQL TCP connection to Flask HTTP callback route
    try:
        #CALLBACK_BASE = current_app.config['CALLBACK_URL'] # Accessing url from config.py
        url = f"{CALLBACK_BASE}/token/{token}/callback"
        res = requests.get(
            url,
            headers={
                'X-Forwarded-For': source_ip,
                'User-Agent': 'MySQL Replication Client'
            }
        )
        #print(f'[MYSQL BAIT] Callback fired → {url} | Status: {res.status_code}')
    except Exception as e:
        print(f'[MYSQL BAIT] Callback failed: {e}')


def handle_connection_and_log(conn, addr, app=None):
    src_ip = addr[0]
    try:
        conn.send(MYSQL_RSP)

        data = b''
        conn.settimeout(3)
        try:
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            pass

        if not data:
            return

        # Extract token from offset 36
        try:
            offset = 36
            end    = data.index(b'\x00', offset)
            token  = data[offset:end].decode('utf-8', errors='ignore')
        except Exception as e:
            print(f'[MYSQL BAIT] Token extraction failed: {e}')
            return

        # De-duplication of incoming alerts
        dedup_key = (token, src_ip)
        with seen_lock:
            if dedup_key in seen_connections:
                #print(f'[MYSQL BAIT] Duplicate suppressed token: {token} ip: {src_ip}')
                return ""
            seen_connections.add(dedup_key)

        # Only one thread reaches here per token+IP
        #print(f'[MYSQL BAIT] Token: {token} | Source IP: {src_ip}')

        # Bridge to Flask callback route via HTTP
        notify_callback(token=token, source_ip=src_ip)

    except Exception as e:
        print(f'[MYSQL BAIT] Error: {e}')
    finally:
        conn.close()


def mysql_listener(app=None, port=3308):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(5)
        print(f'[+] MySQL bait listener active on port {port}')
    
    except Exception as e:
        return f"[MYSQL ERROR] : {e}"
    
    while True:
        conn, addr = s.accept()
        t = threading.Thread(
            target=handle_connection_and_log,
            args=(conn, addr, app),
            daemon=True
        )
        t.start()


def start_mysql_listener(app, port=3308):
    threading.Thread(
        target=mysql_listener,
        args=(app, port),
        daemon=True
    ).start()
    print(f'[+] MySQL listener thread started on port {port}')


if __name__ == '__main__':
    print('[*] Running MySQL bait listener in standalone mode')
    print('[*] Token and IP will be printed no DB logging')
    print('[*] Press Ctrl+C to stop\n')
    try:
        mysql_listener(app=None, port=3308)
    except KeyboardInterrupt:
        print('\n[*] Listener stopped')
