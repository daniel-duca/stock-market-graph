from pandas_datareader import data
import datetime
from bokeh.plotting import figure,show,output_file
from bokeh.embed import components
from bokeh.resources import CDN


def status(c,o):
    if c < o:
        val="inc"
    elif c > o:
        val = "dec"
    else:
        val = "eql"
    return val

start_time=datetime.datetime(2019,1,1)
end_time=datetime.datetime.now()
company_name="TEVA"
hours_12=12*60*60*1000
df=data.DataReader(name=company_name,data_source="yahoo",start=start_time,end=end_time)

df["Status"]=[status(c,o) for c,o in zip(df.Close,df.Open)]
df["Middle"]= (df.Open+df.Close)/2
df["Heigth"]=abs(df.Open-df.Close)

fg=figure(x_axis_type='datetime',width=1500,height=600,sizing_mode="scale_width")
fg.title.text="Candlestick Chart"
fg.grid.grid_line_alpha=0

fg.segment(df.index,df.High,df.index,df.Low,color="black")

fg.rect(df.index[df.Status=="inc"],df.Middle[df.Status=="inc"],hours_12,df.Heigth[df.Status=="inc"],
fill_color="green",line_color="black")

fg.rect(df.index[df.Status=="dec"],df.Middle[df.Status=="dec"],hours_12,df.Heigth[df.Status=="dec"],
fill_color="red",line_color="black")

fg.rect(df.index[df.Status=="eql"],df.Middle[df.Status=="eql"],hours_12,df.Heigth[df.Status=="eql"],
fill_color="gray",line_color="black")

script1,div1 = components(fg)
cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files

output_file("CS.html")
show(fg)


