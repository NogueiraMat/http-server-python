from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv
import logging
import json

FAKE_DB = []

class Server(BaseHTTPRequestHandler):
    def _set_response(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    def do_GET(self):
        logging.info(f"GET - {self.path} - {self.headers}")

        self._set_response()

        # FUNCAO QUE FAZ UM SELECT NUM BANCO
        self.wfile.write(json.dumps(FAKE_DB).encode('utf-8'))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        try: 
            data = json.loads(body.decode("utf-8"))
            # self._set_response()

            if not data.get("name", False) or not data.get("age", False):
                self._set_response(status=400)
                self.send_response(400)
                self.wfile.write(json.dumps({"error": "Envie 'name' e 'age'"}).encode("utf-8"))
                return 
            
            self._set_response(status=201)
            
            # UMA FUNCAO QUE FAZ UM INSERT NO BANCO
            new_user = {
                data["name"]: {
                    "age": data["age"]
                }
            }
            
            FAKE_DB.append(new_user)

            self.wfile.write(json.dumps(data).encode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)

    httpd = server_class(server_address, handler_class)
    logging.info("Starting server...")
    try: 
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Stopping server...")


if __name__ == "__main__":
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()