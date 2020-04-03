from bokeh.embed import components, file_html,json_item
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Tabs,Panel
from bokeh.resources import CDN
def make_plot(df):

	print("----------start of make_plot-------------------------")
	data_df=df
	source=ColumnDataSource(data_df)
	headers = list(data_df.head(0))
	
	plots=[]
	tab=[]

	plot = figure(plot_height=500, plot_width=500)

	plot.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", source=source)
	
	'''for i in range(len(headers)-1):

		plot = figure(plot_height=500, plot_width=500)

		plot.line(x=headers[0],y=headers[i],source=source,line_width=2)
		tab.append(Panel(child=plot,title = headers[i]))'''

        
	'''tabs = Tabs(tabs=tab)
	script, div = components(tabs)
	plots.append((script,div))'''
	return plot
    

    
def make_plot1(df):
	print("Hello")

        

    
    
    
    
    
    


    
    #x1=range(len(data_df.iloc[0:,1:2]))
    