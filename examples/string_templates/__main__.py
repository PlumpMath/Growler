#
# examples/string_templates/__main__.py
#
"""
Example script to demonstrate route decorating, string-template
rendering and low-level server.
"""


from os import path

import asyncio

from growler import (App)
from growler.aio import GrowlerHTTPProtocol
from growler.middleware import (
    Logger,
    StringRenderer,
)

app = App('GrowlerServer')

view_dir = path.join(path.dirname(__file__), "views")

app.use(Logger())
app.use(StringRenderer(view_dir))


@app.get('/')
def index(req, res):
    obj = {'title': "FooBar"}
    res.render("home", obj)


@app.get('/hello')
def hello_world(req, res):
    res.send_text("Hello World!!")


@app.use
def error_handler(req, res, err):
    res.send_text("404 : Hello World!!")


app.print_middleware_tree()

loop = asyncio.get_event_loop()

server_params = {
    'host': '127.0.0.1',
    'port': 8000,
}

# This is explicitly calling asyncio functions;
# the same could be accomplished with the one line:
#   app.create_server_and_run_forever(**server_params)
make_server = loop.create_server(lambda: GrowlerHTTPProtocol(app),
                                 **server_params)
loop.run_until_complete(make_server)

loop.run_forever()
