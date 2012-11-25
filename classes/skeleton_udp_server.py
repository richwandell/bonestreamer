import SocketServer, json

class SkeletonUdpServer(SocketServer.BaseRequestHandler):
     global objs, classes
        
     def handle(self):
          socket = self.request[1]          
          output = json.dumps({
                'bones': objs['positions'],
                'rgb': objs['video_data']
          })+'{{end}}'
          for x in output:
               socket.sendto(bytes(x), self.client_address)