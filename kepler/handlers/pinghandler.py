from kepler.handlers.basehandler import BaseHandler

class PingHandler(BaseHandler):

    endpoint = "ping"

    def default(self,handler):
        result_code = 200
        result_message = "OK"
        result_content_type = "text/plain"
        handler.send_response(result_code,result_message)
        handler.send_header("X-Module",self.__class__.__name__)
        handler.send_header("Content-Type",result_content_type)
        handler.end_headers()
        handler.wfile.write("OK")

__handlers__ = [PingHandler]
