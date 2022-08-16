#import basic python libraries
from flask import Flask, render_template
import pandas as pd
import numpy as np
import time
import asyncio

#import bokeh plotting tools
from bokeh.embed import server_document
from bokeh.io import curdoc,doc
from bokeh.models import ColumnDataSource,PanTool,ResetTool,CustomJS,HoverTool,BoxZoomTool,ResetTool
from bokeh.models.widgets import Select,Button,DataTable,TableColumn,Slider
from bokeh.plotting import figure
#import bokeh server and bokeh tornado
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
#import bokeh display class functions
from feature_display import FeatureDisplay
from display_compare import CompareDisplay
#start all processes

if __name__ == '__main__':
#sys.exit() raises an exception if python not great than 3.5 or linux operating system
	import sys
	sys.exit()

app = Flask(__name__)

def modify_doc_smcompare(doc):
	fs = CompareDisplay()
	layout = fs.smcompare()
	doc.add_root(layout)
def modify_doc_featid(doc):
	fs = FeatureDisplay()
	layout = fs.feat_id()
	doc.add_root(layout)

sockets, port = bind_sockets("", 0)

fi = Application(FunctionHandler(modify_doc_featid))
snn = Application(FunctionHandler(modify_doc_smcompare))

@app.route('/',methods=['GET'])
@app.route('/land',methods=['GET'])
def land():
	script = server_document('http://:%d/land' %port)
	return render_template('land.html',script=script,template='Flask')

@app.route('/about',methods=['GET'])
def about():
	script = server_document('http://:%d/about' %port)
	return render_template('about.html',script=script,template='Flask')

@app.route('/analytics',methods=['GET'])
def analytics():
	return render_template('analytics.html')

@app.route('/applications',methods=['GET'])
def applications():
	return render_template('applications.html')

@app.route('/contact',methods=['GET'])
def contact():
	return render_template('contact.html')

def bk_worker():

	asyncio.set_event_loop(asyncio.new_event_loop())

	bokeh_tornado = BokehTornado({'/about':fi,'/land':snn},io_loop=IOLoop(), allow_websocket_origin=[":5000"])
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()
