import pandas as pd
import numpy as np
import pickle as pkl
from os.path import dirname, join
from bokeh.layouts import layout,column,row,widgetbox
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource,PanTool,ResetTool,CustomJS,HoverTool,BoxZoomTool,ResetTool
from bokeh.models.widgets import Select,Button,DataTable,TableColumn,Slider
from bokeh.plotting import figure

class  TimeDisplay():
	def __init__(self):
		with open('Time_Series_Predict.pkl', 'rb') as f:
			data = pd.read_pickle(f,compression=None)
		with open('TS_Predict_Total.pkl', 'rb') as f:
			data_tot = pd.read_pickle(f,compression=None)
		self.data = data
		self.data_tot=data_tot

	def cls_select(self):
		#create slope data set using idx
		data_last = self.data[self.data.Date == '2014-11-30'].reset_index(drop=True)
		data_slope = data_last.sort_values(by=['Slope'],ascending=True)
		data_slope['IDX'] = range(1,data_slope.shape[0]+1)
		data_change = data_last.sort_values(by=['Change'],ascending=True)
		data_change['IDX'] = range(1,data_change.shape[0]+1)
		#set source original for slope and change
		names = ['Registered','Premier','Silver','Gold','Platinum']

		ds = data_slope[data_slope.Class == names[0]]
		dc = data_change[data_change.Class == names[0]]

		source_s = ColumnDataSource(ds)
		source_c = ColumnDataSource(dc)

		#basic slope figure
		plot = figure()
		plot.circle(x='IDX',y='Slope',color='darkgreen',size=5,alpha=.5, source=source_s)

		plot.plot_width=650
		plot.plot_height=400
		plot.background_fill_color="lightgreen"
		plot.background_fill_alpha=0.3

		plot.title.text="Projected Relative Change"
		plot.title.text_color="black"
		plot.title.text_font="Arial"
		plot.title.text_font_size="28px"
		plot.title.align="center"

		plot.xaxis.axis_label="Partners"
		plot.yaxis.axis_label="Growth Ratio"
		plot.axis.axis_label_text_font="Arial"
		plot.axis.axis_label_text_font_size="18px"

		plot.border_fill_color='whitesmoke'
		plot.min_border_right = 80
		plot.min_border_left = 80

		plot.tools=[PanTool(),ResetTool(),BoxZoomTool()]
		hover=HoverTool(tooltips=[('ID','@ID'),('Class','@Class'),('Territory','@Territory')])
		plot.add_tools(hover)
		plot.toolbar_location = 'above'
		plot.toolbar.logo=None

		#basic figure for change
		plot1 = figure()
		plot1.circle(x='IDX',y='Change',color='darkgreen',size=5,alpha=.5,source=source_c)
		plot1.plot_width=650
		plot1.plot_height=400
		plot1.background_fill_color="lightgreen"
		plot1.background_fill_alpha=0.3

		plot1.title.text="Projected Absolute Change"
		plot1.title.text_color="black"
		plot1.title.text_font="Arial"
		plot1.title.text_font_size="28px"
		plot1.title.align="center"

		plot1.xaxis.axis_label="Partners"
		plot1.yaxis.axis_label="Absolute Change"
		plot1.axis.axis_label_text_font="Arial"
		plot1.axis.axis_label_text_font_size="18px"

		plot1.tools=[PanTool(),ResetTool(),BoxZoomTool()]
		hover=HoverTool(tooltips=[('ID','@ID'),('Class','@Class'),('Territory','@Territory')])
		plot1.add_tools(hover)
		plot1.toolbar_location = 'above'
		plot1.toolbar.logo=None

		plot1.border_fill_color='whitesmoke'
		plot1.grid
		plot1.min_border_right = 80
		plot1.min_border_left = 80
		#build select tool
		pc = Select(value=names[0], options=names, title='Select Class')
		#create update function
		def source_update(attribute, old, new):
			n = str(pc.value)
			ds = data_slope[data_slope['Class'] == n]
			dc = data_change[data_change['Class'] == n]
			source_s.data = ColumnDataSource.from_df(ds)
			source_c.data = ColumnDataSource(dc).from_df(dc)
		#set on change condition
		pc.on_change("value",source_update)
		widget1 = widgetbox(pc,width=500)
		#widget2 = widgetbox(button,width=500)
		layout1=layout([[widget1],[plot,plot1]])
		#curdoc().title = "Select Class"
		return layout1

	def partners_table(self):
		date = self.data.Date.max()
		df = self.data[self.data.Date == date]
		tablesource = ColumnDataSource()
		tablesource.data=ColumnDataSource.from_df(df)
		columns = [TableColumn(field='ID', title="Partner ID", width=100), TableColumn(field='Pred', title="Predicted", width=125), TableColumn(field='Low', title="Low Predicted", width = 125), TableColumn(field='High', title="High Predicted", width = 125), TableColumn(field='Trend', title="Baseline Trend", width = 125),	TableColumn(field='Change', title="Predicted Change", width = 125)]
		partners = DataTable(source=tablesource, columns=columns, width=700, row_headers=False)
		layout1=layout(partners)
		return layout1

	def time_series_plot(self):
		timesource = ColumnDataSource(self.data_tot)

		# Create the basic time plot
		plot = figure(x_axis_type='datetime')
		plot.line(x="Date",y="Act",source=timesource,line_color='black',line_width=1,legend='Actual')
		plot.line(x="Date",y="Pred",source=timesource,line_color='blue',line_width=1,legend='Predicted')
		plot.line(x="Date",y="High",source=timesource,line_color='red',line_width=.5)
		plot.line(x="Date",y="Low",source=timesource,line_color='red',line_width=.5)
		plot.circle(x="Date",y="Trend",source=timesource,size=5,color='green')

		plot.plot_width=1200
		plot.plot_height=750
		plot.background_fill_color="lightgreen"
		plot.background_fill_alpha=0.3

		plot.title.text="Projected Order Input"
		plot.title.text_color="black"
		plot.title.text_font="Arial"
		plot.title.text_font_size="28px"
		plot.title.align="center"

		plot.xaxis.axis_label="Date"
		plot.yaxis.axis_label="Order Input"
		plot.axis.axis_label_text_font="Arial"
		plot.axis.axis_label_text_font_size="18px"

		plot.border_fill_color='whitesmoke'

		plot.tools=[PanTool(),ResetTool(),BoxZoomTool()]
		hover=HoverTool(tooltips=[('Predicted','@Pred'),('High Prediction','@High'),('Low Prediction','@Low'),('Trend','@Trend')])
		plot.add_tools(hover)
		plot.toolbar_location = 'above'
		plot.toolbar.logo=None

		plot.grid
		plot.min_border = 100

		plot.legend.location='top_left'
		plot.legend.background_fill_color = 'green'
		plot.legend.background_fill_alpha=.1
		layout1 = layout(plot)
		return layout1

	def partners_range(self):
		#create data set for slope by new id
		df = self.data[self.data.Date == '2014-11-30'].reset_index(drop=True)
		df = df.sort_values(by=['Change'],ascending=True)
		df['IDX'] = range(1,df.shape[0]+1)
		#set source original and source to be moved with slider
		source_original = ColumnDataSource(df)
		source = ColumnDataSource(df)
		#basic figure
		plot = figure()
		plot.line(x='IDX',y='Change',source=source)
		plot.plot_width=1200
		plot.plot_height=650
		plot.background_fill_color="lightgreen"
		plot.background_fill_alpha=0.3

		plot.title.text="Projected Absolute Change"
		plot.title.text_color="black"
		plot.title.text_font="Arial"
		plot.title.text_font_size="28px"
		plot.title.align="center"

		plot.xaxis.axis_label="Partners"
		plot.yaxis.axis_label="Growth"
		plot.axis.axis_label_text_font="Arial"
		plot.axis.axis_label_text_font_size="18px"

		plot.border_fill_color='whitesmoke'
		plot.tools=[PanTool(),ResetTool(),BoxZoomTool()]
		hover=HoverTool(tooltips=[('ID','@ID'),('Class','@Class'),('Territory','@Territory')])
		plot.add_tools(hover)
		plot.toolbar_location = 'above'
		plot.toolbar.logo=None

		plot.grid
		plot.min_border_right = 80


		def set_range(attrname,old,new):
			source.data={key:[value for i, value in enumerate(source_original.data[key]) if source_original.data['IDX'][i]<=sliderhigh.value and source_original.data['IDX'][i]>=sliderlow.value] for key in source_original.data}


		#create loweer limit slider
		sliderlow=Slider(start=min(source_original.data['IDX']),end=max(source_original.data['IDX']),value=1,step=10,title="Lower Partner: ")
		sliderlow.on_change("value",set_range)

		#create upper limit slider
		sliderhigh=Slider(start=min(source_original.data['IDX'])-1,end=max(source_original.data['IDX']),value=500,step=10,title="Upper Partner: ")
		sliderhigh.on_change("value",set_range)
		widget1=widgetbox(sliderlow,sliderhigh, width = 500)
		layout1=layout([[widget1],[plot]])
		return layout1

	def partner_plot(self):
		#The next builds a time series chart to observe selected series.  Select box #changes id to present on update
		#select data by id and source update function
		data=self.data
		def time_data(id, data):
			dt = data[data.ID == id]
			return dt
		#update data
		dt = time_data(data.ID[0], data)
		timesource = ColumnDataSource(dt)

		# Create the basic time plot
		plot = figure(x_axis_type='datetime')
		plot.line(x='Date',y='Act',source=timesource,line_color='black',line_width=1,legend='Actual')
		plot.line(x='Date',y='Pred',source=timesource,line_color='blue',line_width=1,legend='Predicted')
		plot.line(x='Date',y='High',source=timesource,line_color='red',line_width=.5)
		plot.line(x='Date',y='Low',source=timesource,line_color='red',line_width=.5)
		plot.circle(x='Date',y='Trend',source=timesource,size=5,color='green')

		plot.plot_width=1200
		plot.plot_height=750
		plot.background_fill_color="lightgreen"
		plot.background_fill_alpha=0.3

		plot.title.text="Projected Order Input"
		plot.title.text_color="black"
		plot.title.text_font="Arial"
		plot.title.text_font_size="28px"
		plot.title.align="center"

		plot.xaxis.axis_label="Date"
		plot.yaxis.axis_label="Order Input"
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
		ID = Select(value=options[0], options=options, title='Select Partner')
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
