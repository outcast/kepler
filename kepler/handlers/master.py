from BaseHTTPServer import BaseHTTPRequestHandler
from copy import copy
import socket
import os

endpoints = {}


def list_handlers():
    return [os.path.splitext(module)[0]
            for module in os.listdir(os.path.dirname(__file__))
            if module.endswith("handler.py")]


def register_endpoints(package):
    handlers = list_handlers()
    for h in handlers:
        mod = __import__('{}.handlers.{}'.format(package, h), fromlist=['{}.handlers'.format(package)])
        if not hasattr(mod, '__handlers__'):
            e = AttributeError()
            e.message = "Handler module {} do have attribute '__handlers__'"
            raise e

        for c in mod.__handlers__:
            print "Loading handler for endpoint: {}".format(c.endpoint)
            endpoints[c.endpoint] = c()


class MasterHandler(BaseHTTPRequestHandler):
    def _get_method_name(self,handler):
        match = False
        method_map = copy(self.endpointElements[2:])
        while not match:
            mname = "_".join(method_map)
            if len(mname) == 0:
                self.send_error(404)
                return
            if not hasattr(handler,mname):
                method_map.pop()
            else:

                match = True
        return mname

    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return

            self.endpointElements = self.path.split('/')
            endpointName = self.endpointElements[1]
            if endpointName not in endpoints:
                self.send_error(404, 'End Point {} Not Found'.format(endpointName))
                return
            handler = endpoints[endpointName]

            if len(self.endpointElements) > 2:
                mname = self._get_method_name(handler)
            else:
                mname = "default"

            if not hasattr(handler, mname):
                self.send_error(404, 'End Point {}.{} Not Found'.format(endpointName,mname))
                return

            method = getattr(handler, mname)
            method(self)
            self.wfile.flush()  # actually send the response if not already done.
        except socket.timeout, e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return


register_endpoints('kepler')
