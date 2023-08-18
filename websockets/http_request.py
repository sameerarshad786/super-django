import os


class Request():

    def build_absolute_uri(self, value):
        host = os.getenv("SERVER_NAME")
        server_port = os.getenv("SERVER_PORT")
        if server_port:
            host = "%s:%s" % (host, server_port)
        else:
            host = "%s" % (host)
        return f"http://{host}{value}"
