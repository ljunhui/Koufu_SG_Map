# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Helper mod
import helper_drawtable


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title= "Koufu in SG - Visualization"
server = app.server

df = helper_drawtable.main()

def data_bars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #0074D9 0%,
                    #0074D9 {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles


app.layout = html.Div(
    children=[
        dcc.Markdown(
            children="""
                     # Koufu Group's Operations in Singapore
                     **Please note that this site has not been optimized for mobile.**
                     
                     For source code and more information, please refer to my [GitHub](https://github.com/ljunhui/Koufu_SG_Map).
                     """,
            style={"textAlign": "center"},
        ),
        html.Hr(),
        dcc.Markdown(
            children="""
                    #### Objectives:
                    
                    > If I could open an outlet in only 1 **residential** location, where should it be?
                    
                    - A data driven approach visualizing the population density of all 332 sub-zones found in Singapore and grouping them into 5 discrete brackets. Subzone information such as total area (in km2) and total population is provided in a tooltip.
                    - A table of summary is also provided at the bottom of the page that aggregates information about each subzone into their main planning areas.
                    - The dashboard is meant to be used as a supplementary tool, allowing BD managers to make quick decisions zone demographics, paving the way for further exploration regarding the business viability of opening outlets in those zones.
                    
                    ###### Future Work:
                    - Benchmark outlet sales performance against expected sales owing to population density.
                    - Identify best brands to bring into the subzone based on subzone age-group distribution.
                    
                    ###### Limitations:
                    - Future work can explore the density of commercial/industrial areas but that is beyond the scope of this project.
                     """
        ),
        html.Hr(),
        dcc.Markdown(
            children="""
                    #### Usage Instructions:
                    - By default, the map is set to show our foodcourt and coffeeshop brands (Koufu, Gourmet Paradise, Happy Hawkers etc). 
                    - **Using the layer control in the top right corner of the map gives you control of which brands to show.**
                    - The choropleth layer provides more information about the zone, with the colors indicating the population density of each zone. 
                     The darkest colors are zones that have the highest population density. 
                     """,
        ),
        html.Div(
            children=html.Iframe(
                id="map",
                srcDoc=open("./map.html", "r").read(),
                width="95%",
                height="750",
            ),
            style={"textAlign": "center"},
        ),
        html.Div(children="Summary table of zone information aggregated into their Planning Areas"),
        html.Div(children="Default sort by population density in descending order", style={'fontSize':'small', 'fontStyle':'italic'}),
        dash_table.DataTable(
            id="table",
            data=df.to_dict("records"),
            columns=([{"name": i, "id": i} for i in df.columns]),
            sort_action="native",
            style_header={"backgroundColor": "white", "fontWeight": "bold"},
            style_cell={
                "whiteSpace": "normal",
                "height": "auto",
                "textAlign": "center",
            },
            style_table={"height": "500px", "overflowX": "auto", "overflowY": "auto"},
            style_cell_conditional=[
                {"if": {"column_type": "any"}, "textAlign": "right"},
                {"if": {"column_id": "Planning Area"}, "textAlign": "left"},
            ],
            style_data_conditional=(
                data_bars(df, 'Population Density (/km2)') +
                [
                    {
                        "if": {
                            "filter_query": "{{{}}} != 0".format(col),
                            "column_id": col,
                        },
                        "backgroundColor": "tomato",
                        "color": "white",
                    }
                    for col in df.columns[4:]
                ]
            ),
        ),
    ],
    
)

if __name__ == "__main__":
    app.run_server(debug=True)