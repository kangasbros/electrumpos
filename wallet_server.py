#!/usr/bin/env python
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2011 thomasv@gitorious
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import time, thread, sys, socket

import os

# see http://code.google.com/p/jsonrpclib/
import jsonrpclib
try:
    from lib import Wallet, WalletSynchronizer, format_satoshis, mnemonic, prompt_password
except ImportError:
    from electrum import Wallet, WalletSynchronizer, format_satoshis, mnemonic, prompt_password
try:
    from lib.util import print_error
except ImportError:
    from electrum.util import print_error

"""
Simple wallet daemon for webservers.
- generates new addresses on request
- private keys are not needed in order to generate new addresses. A neutralized wallet can be used (seed removed)
- no gap limit: use 'getnum' to know how many addresses have been created.

todo:
- return the max gap
- add expiration date

"""


host = 'localhost'
port = 8444
wallet_path = 'wallet_path'
username = 'foo'
password = 'bar'
wallet = Wallet()
master_public_key_hex = "112cee2e893f9e2531b15f013b05a921b917933a310191122470661995e9083ad873e574929a982e142fb3c3c1c3c38a98894802feef7b1c177cc3970cbf708b"
# wallet.master_public_key = master_public_key_hex.decode("hex")
stopping = False

wallets = {}

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCRequestHandler
import SimpleXMLRPCServer

class authHandler(SimpleJSONRPCRequestHandler):
    def parse_request(self):
        if SimpleXMLRPCServer.SimpleXMLRPCRequestHandler.parse_request(self):
            if self.authenticate(self.headers):
                return True
            else:
                self.send_error(401, 'Authentication failed')
            return False

    def authenticate(self, headers):
        from base64 import b64decode
        basic, _, encoded = headers.get('Authorization').partition(' ')
        assert basic == 'Basic', 'Only basic authentication supported'
        x_username, _, x_password = b64decode(encoded).partition(':')
        return username == x_username and password == x_password


def do_stop():
    global stopping
    stopping = True

def get_wallet_or_create(mpk):
    if mpk in wallets.keys():
        return wallets[mpk]
    if os.path.exists("wallets/"+mpk):
        w = Wallet()
        w.set_path("wallets/"+mpk)
        w.read()
        return w
    w = Wallet()
    w.master_public_key = mpk.decode('hex')
    w.set_path("wallets/"+mpk)
    w.create_new_address(False)
    w.save()
    return w

def new_wallet(mpk):
    try:
        w = get_wallet_or_create(mpk)
    except Exception:
        return 0
    return 1

def get_new_address(mpk):
    w = get_wallet_or_create(mpk)
    a = w.create_new_address(False)
    w.save()
    return a

def get_balance(mpk, address):
    w = get_wallet_or_create(mpk)
    w.synchronize()
    a = w.get_addr_balance(address)
    return a

def get_num(mpk):
    w = get_wallet_or_create(mpk)
    return len(w.addresses)

def get_mpk(mpk):
    w = get_wallet_or_create(mpk)
    return w.master_public_key.encode('hex')

if __name__ == '__main__':

    if len(sys.argv)>1:
        import jsonrpclib
        server = jsonrpclib.Server('http://%s:%s@%s:%d'%(username, password, host, port))
        cmd = sys.argv[1]
        arg = None
        if len(sys.argv)>2:
            arg = sys.argv[2]
        addr = None
        if len(sys.argv)>3:
            addr = sys.argv[3]

        try:
            if cmd == 'new_wallet':
                out = server.new_wallet(arg)
            if cmd == 'getnum':
                out = server.getnum(arg)
            elif cmd == 'getkey':
                out = server.getkey(arg)
            elif cmd == 'getnewaddress':
                out = server.getnewaddress(arg)
            elif cmd == 'getbalance':
                out = server.getbalance(arg, addr)
            elif cmd == 'stop':
                out = server.stop()
        except socket.error:
            print_error("Server not running")
            sys.exit(1)
        print out
        sys.exit(0)

    else:

        # nw = get_wallet_or_create(master_public_key_hex)
        # nw.synchronize()
        # print nw.get_balance()

        wallet.set_path(wallet_path)
        wallet.read()

        def server_thread():
            from SocketServer import ThreadingMixIn
            from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
            server = SimpleJSONRPCServer(( host, port), requestHandler=authHandler)
            server.register_function(new_wallet, 'new_wallet')
            server.register_function(get_num, 'getnum')
            server.register_function(get_new_address, 'getnewaddress')
            server.register_function(get_balance, 'getbalance')
            server.register_function(get_mpk, 'getkey')
            server.register_function(do_stop, 'stop')
            server.serve_forever()

        thread.start_new_thread(server_thread, ())
        while not stopping: time.sleep(0.1)


