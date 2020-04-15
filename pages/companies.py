# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import pathlib
from dash.dependencies import Input, Output
from utils import Header, make_dash_table, plot_wordcloud
import dash_table

import dash.dependencies as dd

from io import BytesIO

from wordcloud import WordCloud
import base64



# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("../data").resolve()

# Fortune 500 table:

fortune500table = pd.read_csv(DATA_PATH.joinpath("fortune500table.csv"), encoding = 'utf8')

# Word Cloud:

dfm = pd.read_csv(DATA_PATH.joinpath("df.csv"), encoding = 'utf8')

img = BytesIO()
plot_wordcloud(data=dfm).save(img, format='PNG')
companies_wc = 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # companies page
            html.Div(
                [
                    html.Hr(style={"border-top":"2px solid lightgrey","margin-top":"0","margin-bottom":"3.5rem"}),
                    html.Div([
                        html.H6(
                            "What companies are the most represented?",
                            className="subtitle",style={"margin-left":"10%","margin-bottom":"25px","font-size":"2rem"}
                        ),
                       html.A(
                            html.Img(id="wia-company",
                            src=app.get_asset_url("wia_company_wordcloud.png"),
                            style={"margin":"auto","width":"90%","display":"block"}
                            )
                       )
                    ],className="row"
                    ),
                    html.Br(),
                    html.Div(html.I('''The companies with the most representation are currently Honda (17.8% of the attendees), Nationwide (11.5% of the attendees), Grange Insurance (6.9% of the attendees), CoverMyMeds (6.3% of the attendees), and The Ohio State University (5.7% of the attendees). If you click on \"Industries\" you\'ll see the presence of these companies reflected in the industries represented.'''),className="row",style={"margin-left":"10%","margin-right":"10%","text-align":"justify"}
                    ),
                    
                    html.Br(),
                    
                    html.Div([
                        html.H6(
                            "Forbes 500 Companies Attending WIA Conference",
                            className="subtitle",style={"margin-left":"10%","margin-bottom":"25px","font-size":"2rem"}
                        ),
                        html.A(make_dash_table(fortune500table))
                    ],className="row"
                    ),
                    html.Br(),
                    
                    html.Div(html.I('''Of all the companies that will attend our conference, 18 belong to the Forbes 500. The above table shows that, on average, those 18 companies have 101,570 employees, $50,431 million dollars in revenues, $3,909 million dollars in profits, $219,733 million dollars in assets, and an average market value of $108,332 million dollars.'''),className="row",style={"margin-left":"10%","margin-right":"10%","text-align":"justify"}
                    ),
                    
                    html.Br(),
                    
                    html.Details([
                                html.Summary('Code:',style={"cursor":"pointer"}),
                                html.Div(
                                    dcc.Markdown(r'''
```py
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image  
import PIL 

df = pd.DataFrame(attendees_copy['job_title'].value_counts())
data = dict(zip(df.index.tolist(), df['job_title'].tolist()))
wordcloud = WordCloud(background_color="white", width=800, height=400, max_words=200).generate_from_frequencies(data)

# # Display the generated image:
# # the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

wordcloud.to_file('wia_title_wordcloud.png')
print("Title word cloud created.")
```
'''
                                    ),className="row",style={"overflow":"scroll","height":"400px"}
                                )
                    ]),
                    html.Br(),
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

