import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy as sql
import plotly.graph_objs as go
import pandas as pd


engine = sql.create_engine('postgresql://dianaransomhall:Pwd3244!!@dianadb.ch5xvghip7ci.us-west-1.rds.amazonaws.com:5432/dianadb')
data = pd.read_sql('select * from "ValidationStudy88_PlateID246"', con=engine)



# data manipulations
data1=data.groupby('well_drug_name').agg(['sum','count'])


# data
data['cell_alive']= (~data['cell_event']).apply(lambda x: int(x))
data2 = data.groupby(['well_name', 'cell_alive']).agg('count')
data3 = data.groupby(['well_name']).agg('mean')
data4 = data.groupby(['well_name', 'well_drug_name']).agg('count')
data.groupby(['well_name', 'well_drug_name']).agg('count').index.get_level_values(1)

count_alive=data2.iloc[range(0,(data2.shape[0]-10),2),0].tolist()
mean_cell_last_tp = data3['cell_last_tp'][0:(data3.shape[0]-6)].tolist()
drugs=data4.index.get_level_values(1)[0:90].tolist()

data5=pd.DataFrame({'num_alive': count_alive,
              'mean_cell_last_tp': mean_cell_last_tp,
              'drugs': drugs })

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(children=[
    html.H1(children='Cell Assay'),

    html.Div(children='''
        Visualize Experiments.
    '''),

    dcc.Graph(
        id='cell-count-by-well',
        figure={
            'data': [
                {'x': ["DMSO", "VRG0023", "VRG0024","VRG0037", "VRG0045","VRG0106"],
                 'y': [2946, 2489, 2382, 2782, 2879, 2948],

                 'type': 'bar', 'name': 'Trt'}
            ],
            'layout': {
                'title': 'Cell Count by Trt'
            }
        }
    ),
    dcc.Graph(
        id='Cell Count by Well',
        figure={
            'data': [
                go.Scatter(
                    x=data5[data5['drugs'] == i]['mean_cell_last_tp'],
                    y=data5[data5['drugs'] == i]['num_alive'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in data5.drugs.unique()
            ],
            'layout': go.Layout(
                xaxis={ 'title': 'Mean cell_last_tp'},
                yaxis={'title': '# Cells Alive'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )



])

if __name__ == '__main__':
    app.run_server(debug=False)
