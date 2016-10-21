from kepler.config import config

class BaseHandler(object):

    endpoint = "base"

    def __init__(self):
        super(BaseHandler, self).__init__()
        self.config = config

    def default(self,handler):
        handler.send_response(200,"OK")
        handler.send_header("X-Module",self.__class__.__name__)
        handler.end_headers()
        handler.wfile.write("Hello World!")

__handlers__ =[BaseHandler]