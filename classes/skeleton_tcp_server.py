import SocketServer, json

class SkeletonTcpServer(SocketServer.BaseRequestHandler):
    global objs, classes
    
    def handle(self):    
        self.data = self.request.recv(1024).strip()
        output = json.dumps({
            'bones': objs['positions'],
            'rgb': objs['video_data']
        })+'{{end}}'
        self.request.sendall(bytes(output))