from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from pathlib import Path
import pandas as pd
import os

#initialise dash app
app = Dash(__name__)


def create_dash(flask_app):    
    """ Create a dash application"""
    dash_app = Dash(__name__, eager_loading=True, server=flask_app, url_base_pathname='/dashboard/')
    base_path = os.getcwd().split('backend')[0]
    filepath = os.path.join(base_path,"data_processing","e-GMAT_GMAT_Club_Reviews.csv")

    if Path(filepath).stat().st_size == 0:
        # check if the .csv file is empty and render a no records page in dash
        dash_app.layout = html.Div([html.H1("e-GMAT Reviews Dashboard",
                                            style={"textAlign": "center", "color": "#0a0a0a",
                                                "font-size": 40}
                                            ),
                                            html.P("No e-GMAT Reviews available",
                                            style={"textAlign": "center", "color": "#0a0a0a",
                                                "font-size": 20}),
                                    ])
    else:
        # if the .csv file contains records, render the dash page with dropdown charts and range controlled charts
        data = pd.read_csv(filepath)
        year = data['Year']
        min_year = min(year)
        max_year = max(year)
        years = ['Years']
        for y in range(min_year, max_year + 1):
            years.append(y)
        year_options = [{'label': str(year), 'value': year} for year in years]

        dash_app.layout = html.Div([html.H1("e-GMAT Reviews Dashboard",
                                            style={"textAlign": "center", "color": "#0a0a0a",
                                                "font-size": 40}),
                                            dcc.Dropdown(id="review-dropdown",
                                                        options=[
                                                            {"label": "All", "value": "All"},
                                                            {"label": "Stars", "value": "Stars"},
                                                            {"label": "ImprovedPoints", "value": "ImprovedPoints"},
                                                            {"label": "Course", "value": "Course"}
                                                        ],
                                                        value="All",
                                                        placeholder="Select",
                                                        searchable=True
                                            ),
                                            dcc.Dropdown(id="year-dropdown",
                                                        options=year_options,
                                                        value="Years",
                                                        placeholder="Select Year",
                                                        searchable=True
                                            ),
                                            html.Br(),
                                            html.Div(dcc.Graph(id="dynamic-chart"))
                                            ])

        # callback function for dropdown and range slider
        @dash_app.callback(
            Output("dynamic-chart", "figure"),
            [Input(component_id="review-dropdown", component_property="value"),
            Input(component_id="year-dropdown", component_property="value")]
        )
        def update_dynamic_chart(selected_value, selected_year):
            if selected_year == "Years":
                filtered_df = data
            else:
                filtered_df = data[data['Year'] == selected_year]
            if not selected_value:
                return []
            elif selected_value == "Stars":
                # Bar chart for source distribution
                fig = px.pie(filtered_df, names='Stars', title=f'Star Ratings Distribution ({selected_year})')
                return fig
            
            elif selected_value == "ImprovedPoints":
                # Pie chart for gender distribution
                fig = px.pie(filtered_df, names='ImprovedPoints', title=f'Improved Points ({selected_year})')
                return fig
            
            elif selected_value == "Course":
                # Box plot for zodiac sign distribution
                fig = px.pie(filtered_df, names='Course', title=f'Course Distribution ({selected_year})')
                return fig
        
            else:
                fig = px.parallel_categories(
                    filtered_df,
                    dimensions=['Course', 'ImprovedPoints', 'Stars'],
                    title=f'Parallel Categories ({selected_year})',
                    color_continuous_scale=px.colors.sequential.Inferno
                )
                return fig
            
    return dash_app
