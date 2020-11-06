import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import DatePicker, WidgetBox, Tabs, Panel
from bokeh.models import HoverTool, FactorRange, Title
from bokeh.plotting import figure, output_file, ColumnDataSource
from bokeh.transform import factor_cmap


def tab1():
    data = pd.read_csv('latimes-state-totals.csv')
    data['date_time'] = pd.to_datetime(data['date'])
    s_date = pd.to_datetime('20200801')
    e_date = pd.to_datetime('20200831')
    data = data[(data['date_time'] >= s_date) & (data['date_time'] <= e_date)]
    output_file('resulting.html')
    p = figure(y_axis_label='New cases', x_axis_type='datetime',
               plot_width=1030, plot_height=500)
    p.title.text = "New Coronavirus Cases in California in August"
    p.title.align = "center"
    p.title.text_font_size = "20px"
    p.align = "center"
    p.line('date_time', 'new_confirmed_cases', source=data)
    p.circle('date_time', 'new_confirmed_cases', source=data,
              fill_color="red", size=4)
    p.add_tools(HoverTool(
        tooltips=[
            ('Date', "@date_time{%Y-%m-%d}"),
            ('New cases', "@new_confirmed_cases")
        ],
        formatters={'@date_time': 'datetime'}
    ))

    p.add_layout(Title(
        text="Download data from "
             "https://github.com/datadesk/california-coronavirus-data/latimes-state-totals.csv",
        text_font_style="italic"),
        'below')
    p.add_layout(
        Title(text="Data Source: local public health agencies; "
                   "published by latimes.com/coronavirustracker",
              text_font_style="italic"), 'below')
    p.add_layout(
        Title(text="Date of last update: 2020-10-15", text_font_style="italic"),
        'below')
    tab = Panel(child=p,
                title='New coronavirus cases in California in August,2020')
    return tab


def tab2():
    data = pd.read_csv('cdph-race-ethnicity.csv')
    data['date_time'] = pd.to_datetime(data['date'])
    data = data[(data['age'] == 'all')]
    percentages = ['confirmed cases', 'general population']
    regions = ['asian', 'black', "cdph-other", 'latino', 'other', 'white']
    x = [(race, percent) for race in regions for percent in percentages]

    def create_dataset(df):
        counts = sum(
            zip(df['confirmed_cases_percent'], df['population_percent']),
            ())
        source = ColumnDataSource(data=dict(x=x, counts=counts))
        return source

    def create_plot(source):
        p = figure(x_range=FactorRange(*x),y_axis_label='Percentage',
                   plot_width=1030)
        p.title.text = "Confirmed_case% VS Population% by races"
        p.title.align = "center"
        p.title.text_font_size = "20px"
        p.vbar(x='x', top='counts', width=0.9, source=source,
               line_color="white",
               fill_color=factor_cmap('x', factors=percentages,
                                      palette=["#c9d9d3", "#718dbf"],
                                      start=1, end=2))
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        p.xgrid.grid_line_color = None
        p.add_tools(HoverTool(
            tooltips=[
                ('Race, category', "@x"),
                ('Percentage', "@counts")
            ],
        ))
        p.add_layout(Title(
            text="Data "
                 "published by latimes.com/coronavirustracker; download data "
                 "from "
                 "https://github.com/datadesk/california-coronavirus-data/cdph-race"
                 "-ethnicity.csv in GitHub", text_font_style="italic"), 'below')
        p.add_layout(
            Title(text="Data Source: California Department of Public Health "
                       "https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx",
                  text_font_style="italic"), 'below')
        p.add_layout(Title(text="Date of last update: 2020-10-14",
                            text_font_style="italic"), 'below')
        return p

    def callback(attr, old, new):
        new_src = create_dataset(data[(data['date_time'] == date_picker.value)])
        src.data.update(new_src.data)

    src = create_dataset(data[(data['date_time'] == '2020-10-01')])
    p = create_plot(src)
    date_picker = DatePicker(
        title='Choose a date',
        min_date="2020-05-14", max_date='2020-10-14')
    date_picker.on_change('value', callback)
    controls = WidgetBox(date_picker)
    layout = row(p, controls)
    tab = Panel(child=layout, title='Percentage of confirmed cases by race')
    return tab


def tab3():
    data = pd.read_csv('cdph-race-ethnicity.csv')
    data['date_time'] = pd.to_datetime(data['date'])
    data = data[(data['age'] == 'all')]
    percentages = ['deaths cases', 'general population']
    regions = ['asian', 'black', "cdph-other", 'latino', 'other', 'white']
    x = [(race, percent) for race in regions for percent in percentages]

    def create_dataset(df):
        counts = sum(zip(df['deaths_percent'], df['population_percent']), ())
        source = ColumnDataSource(data=dict(x=x, counts=counts))
        return source

    def create_plot(source):
        p = figure(x_range=FactorRange(*x), y_axis_label='Percentage',
                   plot_width=1030)
        p.title.text = "Death% VS Population% by races"
        p.title.align = "center"
        p.title.text_font_size = "20px"
        p.vbar(x='x', top='counts', width=0.9, source=source,
               line_color="white",
               fill_color=factor_cmap('x', factors=percentages,
                                      palette=["#c9d9d3", "#718dbf"],
                                      start=1, end=2))
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        p.xgrid.grid_line_color = None
        p.add_tools(HoverTool(
            tooltips=[
                ('Race, category', "@x"),
                ('Percentage', "@counts")
            ],
        ))
        p.add_layout(Title(
            text="Data published by latimes.com/coronavirustracker; download data from "
                 "https://github.com/datadesk/california-coronavirus-data/cdph-race"
                 "-ethnicity.csv", text_font_style="italic"), 'below')
        p.add_layout(
            Title(text="Data Source: California Department of Public Health "
                       "https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx",
                  text_font_style="italic"), 'below')
        p.add_layout(
            Title(text="Date of last update: 2020-10-14",
                  text_font_style="italic"),
            'below')
        return p

    def callback(attr, old, new):
        new_src = create_dataset(data[(data['date_time'] == date_picker.value)])
        src.data.update(new_src.data)

    src = create_dataset(data[(data['date_time'] == '2020-10-01')])
    p = create_plot(src)
    date_picker = DatePicker(
        title='Choose a date',
        min_date="2020-05-14", max_date='2020-10-14')
    date_picker.on_change('value', callback)
    controls = WidgetBox(date_picker)
    layout = row(p,controls)
    tab = Panel(child=layout, title='Percentage of deaths by race')
    return tab


tab1 = tab1()
tab2 = tab2()
tab3 = tab3()
# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
