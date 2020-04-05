# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_core_components as dcc
import dash
import dash_table
import pandas as pd

import dash.dependencies as dd

from io import BytesIO

import wordcloud
from wordcloud import WordCloud
import base64


def Header(app):
    return html.Div([get_header(app), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                   html.A(
                        html.Img(id="wia-link",
                        src=app.get_asset_url("WIA_logo.jpg"),
                        className="logo",
                        )
                    ,href="https://womeninanalytics.com"
                    ,style={"transition-duration":"1s"}
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Women in Analytics 2020 Conference: Q4 Report")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/venv/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
            html.Div(
                [html.H4("3 Days | 1200+ Attendees | 47 Speakers")],
                className="statbanner",
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/venv/overview",
                className="tab first",
            ),
            dcc.Link(
                "Titles",
                href="/venv/titles",
                className="tab",
            ),
            dcc.Link(
                "Companies",
                href="/venv/companies",
                className="tab",
            ),
            dcc.Link(
                "Experience Levels",
                href="/venv/experiencelevels",
                className="tab",
            ),
            dcc.Link(
                "Industries", href="/venv/industries",
                className="tab"
            ),
            dcc.Link(
                "Location",
                href="/venv/location",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    #""" Return a dash definition of an HTML table for a Pandas dataframe """
    #table = []
    #for index,  row in df.iterrows():
     #   html_row = []
      #  for i in range(len(row)):
       #     html_row.append(html.Td([row[i]]))
       # table.append(html.Tr(html_row))
   # return table

    table = dash_table.DataTable(
                    id='table',
                                     #columns=[{"name": i, "id": i} for i in df.columns],
                                     #data=df.to_dict('records'),
                                     #style_table={'overflowX': 'scroll'},
                    data=df.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    style_cell_conditional=[
                             {                   
                                'if': {'column_id': c},
                                'textAlign': 'left'
                             } for c in ['Date', 'Region']
                    ],  
                    style_data_conditional=[
                             {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                             }       
                    ],
                    style_header={
                             'backgroundColor': 'rgb(230, 230, 230)',
                             'fontWeight': 'bold'
                    },
                    style_table={'overflowX': 'scroll'},
                 )

    return table

# Word Cloud:

def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='black', width=480, height=360)
    wc.fit_words(d)
    return wc.to_image()


