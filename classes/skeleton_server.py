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
               
            c.execute("select * from ports where port_type = 'tcp'")
            PORT = c.fetchone()[1]
            HOST = 'localhost'
            print "Serving TCP: "+str(PORT)
               
            objs['tcp_server'] = SocketServer.TCPServer((HOST, PORT), SkeletonTcpServer)
               
            try:
                objs['tcp_server'].serve_forever()
            except Exception as e:
                pass
                    
            objs['tcp_server'].server_close()
               
            print "Tcp Server stopped"
               
               
               
        elif self.server_type == 'udp':
            c.execute("select * from ports where port_type = 'udp'")
            PORT = c.fetchone()[1]
               
            HOST = "localhost"
               
            print "Serving udp: "+str(PORT)
               
            objs['udp_server'] = SocketServer.UDPServer((HOST, PORT), SkeletonUdpServer)
               
            try:
                objs['udp_server'].serve_forever()
            except Exception as e:
                pass
                    
            objs['udp_server'].server_close()
               
            print "Udp Server stopped"
               
               
               
        else:
               
               
            HOST_NAME = 'localhost'
            c.execute("select * from ports where port_type = 'http' ")
            PORT_NUMBER = c.fetchone()[1]
            server_class = BaseHTTPServer.HTTPServer
            objs['http_server'] = server_class((HOST_NAME, PORT_NUMBER), SkeletonHttpServer)
            print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
            try:
                objs['http_server'].serve_forever()
            except Exception as e:
                pass
            objs['http_server'].server_close()
            print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
               

