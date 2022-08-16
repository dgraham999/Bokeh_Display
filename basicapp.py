#import basic python libraries
from flask import Flask, render_template
import pandas as pd
import numpy as np
import time

from bokeh.embed import server_document
from bokeh.io import curdoc,doc
from bokeh.models import ColumnDataSource,PanTool,ResetTool,CustomJS,HoverTool,BoxZoomTool,ResetTool
from bokeh.models.widgets import Select,Button,DataTable,TableColumn,Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler

#import bokeh functions
from feature_display import FeatureDisplay
from display_compare import CompareDisplay

app = Flask(__name__)

def modify_doc_smcompare(doc):
	fs = CompareDisplay()
	layout = fs.smcompare()
	doc.add_root(layout)
def modify_doc_featid(doc):
	fs = FeatureDisplay()
	layout = fs.feat_id()
	doc.add_root(layout)
def modify_doc_featall(doc):
	fs = FeatureDisplay()
	layout = fs.feat_all()
	doc.add_root(layout)
fa = Application(FunctionHandler(modify_doc_featall))
fi = Application(FunctionHandler(modify_doc_featid))
snn = Application(FunctionHandler(modify_doc_smcompare))

@app.route('/',methods=['GET'])
@app.route('/land',methods=['GET'])
def land():
	script = server_document('http://localhost:5006/land')
	return render_template('land.html',script=script,template='Flask')
@app.route('/about',methods=['GET'])
def about():
	script = server_document('http://localhost:5006/about')
	return render_template('about.html',script=script,template='Flask')
@app.route('/analytics',methods=['GET'])
def analytics():
	return render_template('analytics.html')
@app.route('/applications',methods=['GET'])
def applications():
	script = server_document('http://localhost:5006/applications')
	return render_template('applications.html',script=script,template='Flask')
@app.route('/contact',methods=['GET'])
def contact():
	return render_template('contact.html')

def bk_worker():
	server = Server({'/about':fa,'/land':snn,'/applications':fi},io_loop=IOLoop(), allow_websocket_origin=["localhost:5000"])
	server.start()
	server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':

	app.run(port=5000)
