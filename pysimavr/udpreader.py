import logging
import socket
import threading
import time

log = logging.getLogger(__name__)

UDP_IP = "127.0.0.1"
UDP_PORT = 4321

class UdpReader():
    def __init__(self, ip=UDP_IP, port=UDP_PORT):
        ''
        self.sock = None
        self._stop_thread = False
        self._thread = None
        self.buffer = ''
        self.ip = ip
        self.port = port
        
    def start(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                              socket.SOCK_DGRAM) # UDP
        self.sock.sendto('', (self.ip, self.port))
        self.sock.setblocking(0)
        
        def target():
            while not self._stop_thread:
                try:
                    data = self.sock.recv(1024) # buffer size is 1024 bytes
                    if data:
                        self.buffer += data
                except socket.error:
                    pass
                time.sleep(1.0 / (9600 / 8))
        self._thread = threading.Thread(target=target)
        self._thread.start()


    def terminate(self):
        self._stop_thread = True
        self._thread.join()
        self.sock.close()

class UdpReader2():
    def __init__(self, ip=UDP_IP, port=UDP_PORT):
        ''
        self.sock = None
        self.buffer = ''
        self.ip = ip
        self.port = port
        
    def start(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                              socket.SOCK_DGRAM) # UDP
        self.sock.sendto('', (self.ip, self.port))
#        self.sock.setblocking(0)
        self.sock.settimeout(0.1)
    def read(self):        
        try:
            while 1:
                x = self.sock.recv(1024)
                if not x:
                    break
                self.buffer += x
        except socket.error:
            pass

        self.sock.close()
        log.debug('udp read:"%s"' % self.buffer)
        return self.buffer
