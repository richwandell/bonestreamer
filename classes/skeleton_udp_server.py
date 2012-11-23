import SocketServer, json

class SkeletonUdpServer(SocketServer.BaseRequestHandler):
     global objs, classes
        
     def handle(self):
          print 'send'
          socket = self.request[1]          
          output = json.dumps(objs['positions'])+'{{end}}'
          for x in output:
               socket.sendto(bytes(x), self.client_address)