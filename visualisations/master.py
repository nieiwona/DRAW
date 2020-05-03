from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.models.widgets import Tabs
from bokeh.themes import Theme

from flask import Flask, render_template
import webbrowser
import pandas as pd
from bokeh.embed import server_document
from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from plots.pca import PCAPlot
from plots.smear import SmearPlot

app = Flask(__name__)
port = 5000

def get_plot(doc):
    #TODO Need data loader
    vsd = pd.read_csv('/home/paulina/Pulpit/ADP/visualisation/vsd.csv', index_col=0)
    res = pd.read_csv('/home/paulina/Pulpit/ADP/visualisation/res.csv', index_col=0)
    smear_plot = SmearPlot(res)
    tab1 = smear_plot.get_tabs()

    pca_plot = PCAPlot(vsd)
    tab2 = pca_plot.get_tabs()

    doc.theme = Theme('theme.yaml')
    doc.add_root(Tabs(tabs=[tab1, tab2]))
    doc.title = "DRAW report"


bokeh_app = Application(FunctionHandler(get_plot))

@app.route('/', methods = ['GET'])
def index():
    script = server_document('http://localhost:5001/bkapp')
    return render_template("index.html", script = script)

def bk_worker():
    server = Server(
        {'/bkapp': bokeh_app},
        io_loop = IOLoop(),
        allow_websocket_origin = ["localhost:{}".format(port)], port = port
    )
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target = bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:{}/'.format(port))
    webbrowser.open_new("http://localhost:{}/".format(port))
    app.run(port = port, debug = False)