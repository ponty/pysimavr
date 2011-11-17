import logging
import socket
import threading

#logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

UDP_IP = "127.0.0.1"
UDP_PORT = 4321
TIMEOUT = 0.1

# TODO: better implementation needed

class UdpReader():
    def __init__(self, ip=UDP_IP, port=UDP_PORT, timeout=TIMEOUT):
        ''
        self.sock = None
        self._stop_thread = False
        self._thread = None
        self._buffer = []
        self.ip = ip
        self.port = port
        self.timeout = timeout
        
    def start(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                              socket.SOCK_DGRAM) # UDP
        self.sock.sendto('', (self.ip, self.port))
        
        self.sock.setblocking(False)
        self.sock.settimeout(self.timeout)
        
        def target():
            log.debug('thread start')
            while not self._stop_thread:
                try:
                    data = self.sock.recv(1024) # buffer size is 1024 bytes
#                    log.debug('recv:%s' % str(data))
                    if data:
                        self._buffer.append(data)
                except socket.error as e: # I get timeout error sometimes
#                    log.debug('socket error:%s' % str(e))
                    pass
            log.debug('thread end')
        self._thread = threading.Thread(target=target)
        self._thread.start()

    def read(self):        
        x = self._buffer
        self._buffer = []
        return ''.join(x)
    
    def terminate(self):
        self._stop_thread = True
        self._thread.join()
        self.sock.close()

