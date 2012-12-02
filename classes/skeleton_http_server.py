import BaseHTTPServer, json, re

class SkeletonHttpServer(BaseHTTPServer.BaseHTTPRequestHandler):
    global objs, classes
     
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/javascript")
        self.end_headers()
         
        if 'callback' in self.path:
            req = self.path.split("?callback=")
            cb = req[1].split("&")[0]
            
            self.wfile.write(cb+"("+json.dumps({
                'bones': objs['positions'],
                'rgb': objs['video_data']
            })+")")
        else:
            self.wfile.write(json.dumps({
                'bones': objs['positions'],
                'rgb': objs['video_data']
            }))
          
          
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/javascript")
        self.end_headers()