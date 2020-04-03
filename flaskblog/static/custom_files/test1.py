from flask import Flask, render_template
import pandas as pd
import yaml
#from threading import Thread

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider,Select
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop
from bokeh.io import curdoc

#from bokeh.sampledata.iris import flowers
'''
app = Flask(__name__)


def modify_doc(doc):
'''    
   # df = pd.read_csv(r"C:\Users\Aditya\Downloads\IRIS.csv")
'''
    df['x']=df.iloc[:,0]
    df['y']=df.iloc[:,1]

   
    #df=flowers.copy()
    source = ColumnDataSource(data=df)

    plot = figure(y_range=(0, 10),
                  y_axis_label='iris dataset',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('x', 'y', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource(data=data).data
        
    def callback1(attr, old, new):
        if new == 0:
            data = df
        else:
            data=df
            data['y'] = data[y_axis.value]
        source.data = ColumnDataSource(data=data).data
    
    def callback2(attr, old, new):
        if new == 0:
            data = df
        else:
            data=df
            data['x'] = data[x_axis.value]
        source.data = ColumnDataSource(data=data).data

    
    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)
    
    x_axis = Select(title="X Axis", options=list((df.iloc[:,0:-2]).columns), value=df.columns[0])
    x_axis.on_change('value', callback2)
    
    
    y_axis = Select(title="Y Axis", options=list((df.iloc[:,0:-2]).columns), value=df.columns[1])
    y_axis.on_change('value', callback1)
    
    doc.add_root(column(slider,x_axis,y_axis, plot))

    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """, Loader=yaml.FullLoader))
    



@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    #server = Server(modify_doc, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()

#from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    app.run(port=8000,debug=True)
'''
def modify_doc(doc):
    df = pd.read_csv(r"C:\Users\Aditya\Downloads\IRIS.csv")

    df['x']=df.iloc[:,0]
    df['y']=df.iloc[:,1]
    #df=flowers.copy()
    source = ColumnDataSource(data=df)

    plot = figure(y_range=(0, 10),
                  y_axis_label='iris dataset',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('x', 'y', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource(data=data).data
            
    def callback1(attr, old, new):
        if new == 0:
            data = df
        else:
            data=df
            data['y'] = data[y_axis.value]
        source.data = ColumnDataSource(data=data).data
        
    def callback2(attr, old, new):
        if new == 0:
            data = df
        else:
            data=df
            data['x'] = data[x_axis.value]
        source.data = ColumnDataSource(data=data).data

        
    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)
        
    x_axis = Select(title="X Axis", options=list((df.iloc[:,0:-2]).columns), value=df.columns[0])
    x_axis.on_change('value', callback2)
        
        
    y_axis = Select(title="Y Axis", options=list((df.iloc[:,0:-2]).columns), value=df.columns[1])
    y_axis.on_change('value', callback1)

    layout=column(slider,x_axis,y_axis, plot)    
    doc().add_root(layout)

    doc().theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """))

modify_doc()
