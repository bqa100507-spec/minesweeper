import socket
import threading
import json
import queue

class NetworkManager:
    def __init__(self, is_host, host_ip='', port=5555):
        self.is_host = is_host
        self.host_ip = host_ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn = None
        self.event_queue = queue.Queue()
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        if self.is_host:
            self.thread = threading.Thread(target=self._run_server, daemon=True)
        else:
            self.thread = threading.Thread(target=self._run_client, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
        try:
            self.socket.close()
        except:
            pass

    def send_message(self, msg_dict):
        if self.conn:
            try:
                data = json.dumps(msg_dict) + "\n"
                self.conn.sendall(data.encode('utf-8'))
            except Exception as e:
                print("Send error:", e)

    def _run_server(self):
        try:
            self.socket.bind(('', self.port))
            self.socket.listen(1)
            self.event_queue.put({'type': 'INFO', 'msg': f'Waiting for connection on port {self.port}...'})
            self.conn, addr = self.socket.accept()
            self.event_queue.put({'type': 'CONNECTED', 'addr': addr})
            self._receive_loop()
        except Exception as e:
            if self.running:
                self.event_queue.put({'type': 'ERROR', 'msg': str(e)})

    def _run_client(self):
        try:
            self.socket.connect((self.host_ip, self.port))
            self.conn = self.socket
            self.event_queue.put({'type': 'CONNECTED', 'addr': (self.host_ip, self.port)})
            self._receive_loop()
        except Exception as e:
            if self.running:
                self.event_queue.put({'type': 'ERROR', 'msg': str(e)})

    def _receive_loop(self):
        buffer = ""
        while self.running and self.conn:
            try:
                data = self.conn.recv(1024)
                if not data:
                    break
                buffer += data.decode('utf-8')
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        msg = json.loads(line)
                        self.event_queue.put(msg)
            except Exception as e:
                break
        if self.running:
            self.event_queue.put({'type': 'DISCONNECTED'})
