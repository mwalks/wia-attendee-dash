# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import pathlib
from dash.dependencies import Input, Output
from utils import Header, make_dash_table
import plotly as py
import plotly.graph_objs as go
from PIL import Image

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("../data").resolve()

# the donut chart:


attendees_copy_pie = pd.read_csv(DATA_PATH.joinpath("attendees_copy_pie_only.csv"), encoding = 'utf8')

labels = attendees_copy_pie['job_title'].tolist()
values = attendees_copy_pie['values'].tolist()

donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # title page
            html.Div(
                [
                    html.Div([
                        html.Hr(style={"border-top":"2px solid lightgrey","margin-top":"0","margin-bottom":"3.5rem"}),
                        html.H6(
                            "What job titles do attendees list most commonly?",
                            className="subtitle",style={"margin-left":"10%","margin-bottom":"25px","font-size":"2rem"}
                        ),
                        html.A(
                            html.Img(id="wia-titles",
                            src=app.get_asset_url("wia_title_wordcloud.PNG"),
                            style={"margin":"auto","width":"90%","display":"block"}
                            )
                        )
                    ],className="row"
                    ),
                    html.Br(),
                    html.Div(html.I(
                        r'''After homogeneizing the job titles that we considered most similar, 20.7% of the attendees have a Manager position, 7.5% have an Analyst position, 6.3% have a Director position, 6.3% have a Consultant position, and the rest have one of 67 other different titles.'''
                        ),className="row",style={"margin-left":"10%","margin-right":"10%","text-align":"justify"}
                    ),
                    
                    html.Br(),
                    
                    html.Div([
                        html.H6(
                            "Attendance by General Job Titles",
                            className="subtitle",style={"margin-left":"10%","margin-bottom":"25px","font-size":"2rem"}
                        ),
                       dbc.Row([
                            dcc.Graph(
                                    id="donut chart",
                                    figure=donut,
                                    config={
                                        'displayModeBar': False
                                    },
                                    style={"width":"100%","display": "inline-block","align":"center"}
                                ),
                        ])
                    ],className="row"
                    ),
                    html.Br(),
                    
                    html.Div(html.I('''23% of the attendees hold an Analyst or Data Scientist title, 22.4% are Managers, whereas around 13% of all the attendees hold a C-Level, SVP, VP or Director title.'''),className="row",style={"margin-left":"10%","margin-right":"10%","text-align":"justify"}
                    ),
                    
                    html.Br(),
                    html.Details([
                                html.Summary('Code:',style={"cursor":"pointer"}),
                                html.Div(
                                    dcc.Markdown(r'''
```py
import numpy as np
import io
import pandas as pd
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models
import gensim
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from PIL import Image
import PIL.ImageOps
import random
import nltk
import re
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from operator import itemgetter
WNL = nltk.WordNetLemmatizer()

#data assumed to be cleaned by this point

df = pd.DataFrame(q4_analysis_work['job_title'].value_counts())
data = dict(zip(df.index.tolist(), df['job_title'].tolist()))
wordcloud = WordCloud(background_color="white", width=800, height=400, max_words=200).generate_from_frequencies(data)

# # Display the generated image:
# # the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

wordcloud.to_file("wia_title_wordcloud.png")
```
'''
                                    ),className="row",style={"overflow":"scroll","height":"400px"}
                                )
                    ]),
                    html.P(
                        [
                            "More detailed code can be found at ",
                            html.A("https://github.com/mwalks/wia-attendee-dash",
                            href="https://github.com/mwalks/wia-attendee-dash"),
                            html.Br(),
                            "THANK YOU FOR YOUR SUPPORT!"
                        ],style={"color":"grey","text-size":"1.3rem","text-align":"center"}
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )


