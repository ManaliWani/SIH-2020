import numpy as np
from bokeh.embed import components, file_html,json_item
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Tabs,Panel
from bokeh.resources import CDN
def LineGraph(df):

	print("----------start of make_plot-------------------------")
	data_df=df
	source=ColumnDataSource(data_df)
	headers = list(data_df.head(0))
	
	plots=[]
	tab=[]

	for i in range(len(headers)-1):

		plot = figure(plot_height=400, plot_width=400)
		plot.line(x=headers[0],y=headers[i],source=source,line_width=2)
		tab.append(Panel(child=plot,title = headers[i]))

        
	tabs = Tabs(tabs=tab)
	script, div = components(tabs)
	plots.append((script,div))
	return plots

def Histogram(df):
	data_df=df
	source=ColumnDataSource(data_df)
	headers = list(data_df.head(0))
	
	plots=[]
	tab=[]
	for i in range(len(headers)-1):
		mu, sigma = 0, 0.5
		measured = data_df.iloc[:,i:i+1]
		hist, edges = np.histogram(measured, density=True, bins=50)


		plot = figure(plot_height = 450, plot_width = 450, 
           title = 'Histogram',
          x_axis_label = headers[i], 
           y_axis_label = "frequency of {}".format(headers[i]))

		plot.quad(top=hist,bottom=0,  
	       left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)


		#plot.line(x=headers[0],y=headers[i],source=source,line_width=2)
		tab.append(Panel(child=plot,title = headers[i]))

	tabs = Tabs(tabs=tab)
	script, div = components(tabs)
	plots.append((script,div))
	return plots

	
	# Add a quad glyph
	
# Show the plot

 