import pandas as pd
import numpy as np
import pickle as pkl
from os.path import dirname, join
from bokeh.layouts import layout,column,row,widgetbox
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource,PanTool,ResetTool,CustomJS,HoverTool,BoxZoomTool,ResetTool
from bokeh.models.widgets import Select,Button,DataTable,TableColumn,Slider
from bokeh.plotting import figure

class CompareDisplay():
	def __init__(self):
		with open('Embed_Forecast.pkl', 'rb') as f:
			data_e = pd.read_pickle(f,compression=None)
		with open('LSTM_Forecast.pkl', 'rb') as f:
			data_l = pd.read_pickle(f,compression=None)
		filestr = 'Time_Series_Predict.pkl'
		with open(filestr, 'rb') as f:
			data_t = pd.read_pickle(f,compression=None)
		data_e = data_e.sort_values(by=['ID','Date'])
		data_l = data_l.sort_values(by=['ID','Date'])
		data_t = data_t.sort_values(by=['ID','Date'])
		data_e = data_e.reset_index(drop=True)
		data_l = data_l.reset_index(drop=True)
		data_t = data_t.reset_index(drop=True)
		self.data_e=data_e
		self.data_l=data_l
		self.data_t=data_t

	def smcompare(self):
		mon = list(self.data_t.Pred)
		ts = []
		for i in range(0,len(mon),3):
			sum = round(np.sum(mon[i:i+3]),2)
			ts.append(sum)

		data = pd.DataFrame()
		data['ID'] = self.data_e['ID']
		data['Date'] = self.data_e['Date']
		data['Act'] = self.data_e['Act']
		data['E_Pred'] = self.data_e['Pred']
		data['L_Pred'] = list(self.data_l['Pred'])
		data['T_Pred'] = ts
		#The next builds a time series chart to observe selected series.  Select box #changes id to present on update
		#select data by id and source update function
		def time_data(id, data):
			dt = data[data.ID == id]
			return dt
		#update data
		dt = time_data(data.ID[0], data)
		#timesource = ColumnDataSource()
		timesource = ColumnDataSource(dt)
		# Create the basic time plot
		plot = figure(x_axis_type='datetime')
		plot.line(x='Date',y='Act',source=timesource,line_color='black',line_dash='solid',line_width=1,legend='Actual')
		plot.line(x='Date',y='E_Pred',source=timesource,line_color='blue',line_dash='dashed',line_width=2,legend='Embedded Deep Learning')
		plot.line(x='Date',y='L_Pred',source=timesource,line_color='red',line_dash='dashed',line_width=1,legend='LSTM Trend')
		plot.line(x='Date',y='T_Pred',source=timesource,line_color='green',line_dash='dashed',line_width=1,legend='Time Series')
		plot.plot_width=800
		plot.plot_height=600
		plot.background_fill_color="lightgreen"
		plot.background_fill_alpha=0.3

		plot.title.text="Sales By Store ID"
		plot.title.text_color="black"
		plot.title.text_font="Arial"
		plot.title.text_font_size="28px"
		plot.title.align="center"

		plot.xaxis.axis_label="Date"
		plot.yaxis.axis_label="Sales"
		plot.axis.axis_label_text_font="Arial"
		plot.axis.axis_label_text_font_size="18px"

		plot.border_fill_color='whitesmoke'

		plot.tools=[PanTool(),ResetTool(),BoxZoomTool()]
		hover=HoverTool(tooltips=[('ID','@ID'),('Predicted','@Pred'),('High Prediction','@High'),('Low Prediction','@Low'),('Trend','@Trend')])
		plot.add_tools(hover)
		plot.toolbar_location = 'above'
		plot.toolbar.logo=None

		plot.grid
		plot.min_border = 100

		plot.legend.location='top_left'
		plot.legend.background_fill_color = 'green'
		plot.legend.background_fill_alpha=.1
		#build drop down box and callback function
		#select box
		options = [str(x) for x in list(data.ID.unique())]
		ID = Select(value=options[0], options=options, title='Select Store')
		#update function
		def ID_update(attribute, old, new):
			id = int(ID.value)
			dt = time_data(id,data)
			timesource.data = ColumnDataSource.from_df(dt)
			#ds = feature_data(ID.value)
			#featuresource.data=ColumnDataSource.from_df(ds)
		ID.on_change("value", ID_update)
		layout1 = layout(ID,plot)
		return layout1
