from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output, State

import base64
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from animal_shelter import AnimalShelter





###########################
# Data Manipulation / Model
###########################
# FIX ME change for your username and password and CRUD Python module name
username = "aacuser"
password = "password123"
shelter = AnimalShelter(username, password)


# class read method must support return of cursor object
# read only dogs for customer's purposes.
df = pd.DataFrame.from_records(shelter.read_all({"animal_type":"Dog"}))



#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'Grazioso Salvare Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('Nicholas Ciesla SNHU CS-340 Dashboard'))),
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
    html.Hr(),
    html.Div(
        
#FIXME Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.

        dcc.RadioItems(
            id = 'radioitems-id-filter',
            options=[
                {'label': 'Water Rescue', 'value': 'w'},
                {'label': 'Wilderness or Mountain Rescue', 'value': 'wm'},
                {'label': 'Disaster Rescue or Tracking', 'value': 'dt'},
                {'label': 'Reset', 'value': 'r'}
            ],
            value='r'
        )

    ),
    html.Hr(),
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
#FIXME: Set up the features for your interactive data table to make it user-friendly for your client
#If you completed the Module Six Assignment, you can copy in the code you created here
        sort_action = "native",
        row_selectable="single",
        selected_rows=[0],
        page_size =10
        
    ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('radioitems-id-filter', 'value')])
def update_dashboard(filter_value):
### FIX ME Add code to filter interactive data table with MongoDB queries
    
    if filter_value == 'r' or filter_value is None:
        # reset selected... or somehow none...
        df = pd.DataFrame.from_records(shelter.read_all({"animal_type":"Dog"}))
    elif filter_value == 'w':
        # water selected
        df = pd.DataFrame.from_records(shelter.read_all({'$and':[{"animal_type":"Dog"}, 
                                                                 {"sex_upon_outcome": "Intact Female"},
                                                                 {'$or':[
                                                                     {"breed": "Labrador Retriever Mix"},
                                                                     {"breed": "Chesapeake Bay Retriever"},
                                                                     {"breed": "Newfoundland"}
                                                                 ]},
                                                                 {'$and':[
                                                                     {"age_upon_outcome_in_weeks": {'$gte': 26}},
                                                                     {"age_upon_outcome_in_weeks": {'$lte': 156}}
                                                                 ]}
                                                                ]
                                                        }))
    elif filter_value == 'wm':
        # wilderness/mountain selected
        df = pd.DataFrame.from_records(shelter.read_all({'$and':[{"animal_type":"Dog"}, 
                                                                 {"sex_upon_outcome": "Intact Male"},
                                                                 {'$or':[
                                                                     {"breed": "German Shepherd"},
                                                                     {"breed": "Alaskan Malamute"},
                                                                     {"breed": "Old English Sheepdog"},
                                                                     {"breed": "Siberian Husky"},
                                                                     {"breed": "Rottweiler"}
                                                                 ]},
                                                                 {'$and':[
                                                                     {"age_upon_outcome_in_weeks": {'$gte': 26}},
                                                                     {"age_upon_outcome_in_weeks": {'$lte': 156}}
                                                                 ]}
                                                                ]
                                                        }))
    elif filter_value == 'dt':
        # disaster/tracking selected
        df = pd.DataFrame.from_records(shelter.read_all({'$and':[{"animal_type":"Dog"}, 
                                                                 {"sex_upon_outcome": "Intact Male"},
                                                                 {'$or':[
                                                                     {"breed": "Doberman Pinscher"},
                                                                     {"breed": "German Shepherd"},
                                                                     {"breed": "Golden Retriever"},
                                                                     {"breed": "Bloodhound"},
                                                                     {"breed": "Rottweiler"}
                                                                 ]},
                                                                 {'$and':[
                                                                     {"age_upon_outcome_in_weeks": {'$gte': 20}},
                                                                     {"age_upon_outcome_in_weeks": {'$lte': 300}}
                                                                 ]}
                                                                ]
                                                        }))

        
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
        
        
    return (data,columns)

@app.callback(
    Output('graph-id', 'children'),
    [Input('datatable-id', "derived_viewport_data")]) #derived_virtual_data for all data. this gets messy
def update_graphs(data):
    if data is not None:
        # get displayed data and convert to dataframe
        dff = pd.DataFrame.from_dict(data)
        # pull out list of unique breed names and count of doccuments that contain each breed.
        names = dff['breed'].value_counts().keys().tolist()
        values = dff['breed'].value_counts().tolist()
        # return pie chart
        return [
            dcc.Graph(        
                figure = px.pie(
                    data_frame=dff,
                    values = values,
                    names = names,
                    width=800,
                    height=500
                )
            )
        ]
    else:
        return None

@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', 'derived_viewport_data'),
    Input('datatable-id', "derived_viewport_selected_rows")]
)
def update_map(viewData, rowsSelected):
#FIXME Add in the code for your geolocation chart
    # convert data to dataframe
    if rowsSelected is not None:
        dff = pd.DataFrame.from_dict(viewData)
    
        return [
            dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            dl.Marker(position=[(dff.iloc[rowsSelected[0],13]), (dff.iloc[rowsSelected[0],14])], children=[
                dl.Tooltip(dff.iloc[rowsSelected[0],4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[rowsSelected[0],9])
                    ])
                ])
            ])
        ]
    
    else:
        return None


app

