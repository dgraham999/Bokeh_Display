import pandas as pd
import numpy as np
import pickle as pkl
from os.path import dirname, join
from bokeh.layouts import layout,column,row,widgetbox
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource,PanTool,ResetTool,CustomJS,HoverTool,BoxZoomTool,ResetTool
from bokeh.models.widgets import Select,Button,DataTable,TableColumn,Slider
from bokeh.plotting import figure
class FeatureDisplay():
	def __init__(self):
		filestr = 'Feature_Importance_ID.pkl'
		with open(filestr,'rb') as f:
			dd = pd.read_pickle(f,compression=None)
		filestr = 'Feature_Importance.pkl'
		with open(filestr,'rb') as f:
			da = pd.read_pickle(f,compression=None)
		self.dd=dd
		self.da=da

	def feat_id(self):
		dd=self.dd
		j = list(dd.keys())[0]
		index = range(len(dd[j]))
		def feature_data(id):
			ds = pd.DataFrame(index=index,columns=['Rank','Weight','Feature'])
			ds['Feature'] = [str(dd[id][i][1]) for i in index]
			ds['Rank'] = [str(dd[id][i][0]) for i in index]
			wts=[dd[id][i][2] for i in index]
			wtsr=[round((w*100),2) for w in wts]
			ds['Weight'] = wtsr
			return ds
		ds = feature_data(j)
		#build feature datasource
		#featuresource = ColumnDataSource()
		featuresource = ColumnDataSource(ds)
		#build datatable
		feature_columns = [TableColumn(field='Feature', title="Feature", width=200), TableColumn(field='Weight', title="Weight", width=125), TableColumn(field='Rank', title="Rank", width = 100)]
		features = DataTable(source=featuresource,columns=feature_columns,width=425)
		##build drop down box and callback function
		##select box
		options = [str(x) for x in list(dd.keys())]
		ID = Select(value=options[0], options=options, title='Select Store')
		#update function
		def ID_update(attribute, old, new):
			id = ID.value
			#print type(int(id))
			#dt = time_data(id,data)
			#timesource.data = ColumnDataSource.from_df(dt)
			ds = feature_data(int(id))
			featuresource=ColumnDataSource(ds)
		ID.on_change("value", ID_update)
		layout1 = layout(ID,features)
		return layout1

	def feat_all(self):
		num_features = len(self.da)
		index = range(num_features)
		ds = pd.DataFrame()
		ds['Feature'] = [self.da[i][1] for i in index]
		wts = [self.da[i][2] for i in index]
		wtsr = [round(w*100,2) for w in wts]
		ds['Weight'] = wtsr
		ds['Rank'] =  [self.da[i][0] for i in index]
		#featuresource = ColumnDataSource()
		featuresource = ColumnDataSource(ds)
		#build datatable
		feature_columns = [TableColumn(field='Feature', title="Feature", width=200), TableColumn(field='Weight', title="Weight", width=125), TableColumn(field='Rank', title="Rank", width = 100)]
		features = DataTable(source=featuresource,columns=feature_columns,width=425)
		layout1 = layout(features)
		return layout1
