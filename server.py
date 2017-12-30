from http.server import BaseHTTPRequestHandler, HTTPServer
import load_data

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        fo = open('index.html', mode='r', encoding='utf-8')

        # Send headers
        if "/neko/cover" in self.path:
            self.send_header('Content-type', 'image/jpg')
            self.send_header('Cache-Control', 'max-age=0')
            self.send_header('If-Modified-Since', 'Tue, 03 Jan 2017 07:46:03 GMT')
            self.end_headers()

            s = str(self.path).split("/neko/cover/")[1].split(".jpg")[0]
            fo = open("./neko/cover/"+str(s)+'.jpg', mode='rb')
            message = fo.read()
            self.wfile.write(message)

        elif "neko" in self.path:
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            s = str(self.path).split("/neko/")[1]
            load_data.__init__(s)
            fo = open('./neko/list/'+str(s)+'/index.html', mode='r', encoding='utf-8')
            message = str(fo.read())
            self.wfile.write(bytes(message, "utf8"))
        if "/" == self.path:
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Send message back to client
            message = str(fo.read())
            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))



        if "404.png" in self.path:
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            fo = open('404.png', mode='rb')
            message = fo.read()
            self.wfile.write(message)
        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()