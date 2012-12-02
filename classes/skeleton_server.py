import SocketServer, json, threading, time, BaseHTTPServer, sqlite3, socket, sys

from classes import skeleton_http_server, skeleton_tcp_server, skeleton_udp_server



class SkeletonServer(threading.Thread):
    global objs, classes
    server_type = 'udp'
     
    def run(self):
        
        skeleton_http_server.objs = objs
        skeleton_tcp_server.objs = objs
        skeleton_udp_server.objs = objs
          
        SkeletonUdpServer = skeleton_udp_server.SkeletonUdpServer
        SkeletonTcpServer = skeleton_tcp_server.SkeletonTcpServer
        SkeletonHttpServer = skeleton_http_server.SkeletonHttpServer
          
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
          
        if self.server_type == 'tcp':
               
            c.execute("select value from settings where type = 'port' and key = 'tcp' ")
            PORT = int(c.fetchone()[0])
            
            c.execute("select value from settings where type = 'host' and key = 'tcp' ")
            HOST = c.fetchone()[0]
            
            print "Serving TCP: "+str(PORT)
            
            
            objs['tcp_server'] = SocketServer.TCPServer((HOST, PORT), SkeletonTcpServer)
               
            try:
                objs['tcp_server'].serve_forever()
            except Exception as e:
                pass
                    
            objs['tcp_server'].server_close()
               
            print "Tcp Server stopped"
               
               
               
        elif self.server_type == 'udp':
            c.execute("select value from settings where type = 'port' and key = 'udp' ")
            PORT = int(c.fetchone()[0])
               
            c.execute("select value from settings where type = 'host' and key = 'udp' ")
            HOST = str(c.fetchone()[0])
               
            print "Serving udp: "+str(PORT)
               
            objs['udp_server'] = SocketServer.UDPServer((HOST, PORT), SkeletonUdpServer)
               
            try:
                objs['udp_server'].serve_forever()
            except Exception as e:
                pass
                    
            objs['udp_server'].server_close()
               
            print "Udp Server stopped"
               
               
               
        else:
               
            c.execute("select value from settings where type = 'host' and key = 'http' ")
            HOST_NAME = str(c.fetchone()[0])
            
            c.execute("select value from settings where type = 'port' and key = 'http' ")
            PORT_NUMBER = int(c.fetchone()[0])
            
            server_class = BaseHTTPServer.HTTPServer
            objs['http_server'] = server_class((HOST_NAME, PORT_NUMBER), SkeletonHttpServer)
            print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
            try:
                objs['http_server'].serve_forever()
            except Exception as e:
                pass
            objs['http_server'].server_close()
            print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
               

