import logging
import socket
import threading
import asynchat
import asyncore
import struct

#logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

UDP_IP = "127.0.0.1"
UDP_PORT = 4321
TIMEOUT = 0.1

class UdpHandler(asynchat.async_chat):
    """
    Handler of UDP pipe from AVR simulator. It provides basic network
    facilities. It shall be subclassed to implement specific behavior.
    """
    def __init__(self, ip=UDP_IP, port=UDP_PORT, timeout=TIMEOUT):
        asynchat.async_chat.__init__(self)
        self.set_terminator(1)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)
        self.socket.setblocking(False)
        self.ibuffer = ''
        self.ip = ip
        self.port = port
        
    def start(self):
        self.socket.sendto('', (self.ip, self.port))
        self._thread = threading.Thread(target=lambda: 
                                          asyncore.loop(timeout=1),
                                        name='UdpHandlerThread')
        self._thread.start()
    
    def collect_incoming_data(self, data):
        self.ibuffer += data

    def terminate(self):
        self.close()
        self._thread.join()


class UdpReader(UdpHandler):
    """ This handler does not answer anything. It accumulates data
    which it receives, i.e. does the same as the original one.
    """ 
    def found_terminator(self):
        pass
    
    def read(self):
        x = self.ibuffer
        self.ibuffer = ''
        return ''.join(x)
      
      
class UdpRepeater(UdpHandler):
    """ This handler repeats everything it receives back. """
    def __init__(self, ip=UDP_IP, port=UDP_PORT, timeout=TIMEOUT):
      super(UdpRepeater, self).__init__(ip, port, timeout)
      self.set_terminator(1)
      
    def found_terminator(self):
      resp = self.ibuffer
      self.ibuffer = ''
      self.socket.sendto(resp, (self.ip, self.port))
      

class HypotheticDevice(UdpHandler):
  """
  This class is example how to implement a set of UART connected devices
  communicating via simple protocol: receives address byte and command and
  response with 2 bytes of data.
  """
  def __init__(self, ip=UDP_IP, port=UDP_PORT, timeout=TIMEOUT):
    super(UdpRepeater, self).__init__(ip, port, timeout)
    self.set_terminator(1)
    self.addr = None
      
  def found_terminator(self):
    if self.addr == None:
      self.addr = struct.unpack('B', self.ibuffer)
    else:
      command = struct.unpack('B', self.ibuffer)
      response = self.reactOnCommand(self.addr, command)
      self.send(response)
      self.addr = None