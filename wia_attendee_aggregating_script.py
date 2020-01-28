import pandas as pd
import numpy as np

fn = input("Name of file (ex: Q4-2019 Attendees.csv): ")
print("Attempting to read in file.")
attendees = pd.read_csv(fn)
attendees_copy = attendees.rename(columns = {'Order #':'order#', 'Ticket Type':'ticket_type', 'Attendee #':'attendee#', 'Gender': 'gender', 
                                                      'City': 'city', 'Zip Code': 'zipcode', 'Country': 'country', 
                                                      'Dietary Restrictions': 'dietary_restrictions', 'Technical Expertise': 'technical_expertise',
                                                      'Analytics Experience': 'analytics_experience', 'Job Function': 'job_function', 'Industry': 'industry',
                                                      'What topics would you like to hear about?': 'topics_like_hear',
                                                      'Are you interested in being recruited by sponsoring companies?': 'interested_being_recruited',
                                                      'Do you plan on attending the opening reception on Wednesday, June 3rd, 2020? ': 'plan_attending_reception',
                                                      'Did someone refer you to this conference? If so, please list their name.': 'someone_referred_ifso_name',
                                                      'Additional Terms': 'additional_terms', 'Job Title': 'job_title', 'Company': 'company'})
col = ['ticket_type', 'attendee#', 'gender', 'city', 'zipcode',
       'country', 'dietary_restrictions', 'technical_expertise',
       'analytics_experience', 'job_function', 'industry', 'topics_like_hear',
       'interested_being_recruited', 'plan_attending_reception',
       'someone_referred_ifso_name', 'additional_terms', 'job_title',
       'company']
for i in col:
    attendees_copy[col] = attendees_copy[col].replace(np.nan,'No Answer')
print("Columns renamed. NA's replaced with No Answer.")

tech_agg = attendees_copy.technical_expertise.value_counts().to_frame().reset_index().rename(columns={'index':'Technical Expertise','technical_expertise':'Frequency'})
print('Technical expertise aggregated. Writing.')
tech_agg.to_csv('shortcut_tech_exp.csv')
print('Success.')
anexp_agg = attendees_copy.analytics_experience.value_counts().to_frame().reset_index().rename(columns={'index':'Analytics Experience','analytics_experience':'Frequency'})
print('Analytics experience aggregated. Writing.')
anexp_agg.to_csv('shortcut_an_exp.csv')
print('Success.')
ind_agg = attendees_copy.industry.value_counts().to_frame().reset_index().rename(columns={'index':'Industry','industry':'Frequency'})
print('Industries aggregated. Writing.')
ind_agg.to_csv('shortcut_ind.csv')
print('Success.')
locations = attendees_copy.zipcode.value_counts().to_frame().reset_index().rename(columns={'index':'zipcode','zipcode':'percent'})
locations.percent = (locations.percent / locations.percent.sum()) * 100
locations = locations.merge(attendees_copy[['zipcode','city']].drop_duplicates(),on='zipcode',how='left')
locations = locations[locations.zipcode != 'No Answer']
locations = locations[locations.city != '30 East Broad St, Floor 13']

from pyzipcode import ZipCodeDatabase
zcdb = ZipCodeDatabase()
lons = []
lats = []
for row in locations.iterrows():
    try:
        search = zcdb[row[1][0]]
    except Exception as e:
        print('A zip lookup failed: ' + str(row[1][0]))
        print(e)
    lons.append(search.longitude)
    lats.append(search.latitude)
locations['lon'] = lons
locations['lat'] = lats
print('Location lats lons found. Writing.')
locations.to_csv('shortcut_loc.csv')
print('Success.')

#word clouds
from nltk.collocations import QuadgramAssocMeasures,QuadgramCollocationFinder
import nltk
import re
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from operator import itemgetter
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
WNL = nltk.WordNetLemmatizer()

attendees_copy['job_title'] = attendees_copy['job_title'].str.replace(' / ', '')
attendees_copy['job_title'] = attendees_copy['job_title'].str.replace('Sr', 'Senior')

df2 = attendees_copy['job_title'].dropna(how='all').astype(str)
df2 = " ".join(job_title for job_title in df2)

stopwords = set(STOPWORDS)
stopwords.update(["I", "on", "and", "good", "etc", "make", "better", "depending"])

# Generate a word cloud image
text_content = [WNL.lemmatize(str(df2)) for t in df2]

tokens = nltk.word_tokenize(str(df2))
text = nltk.Text(tokens)

# Remove extra chars and remove stop words.
text_content = [''.join(re.split("[ .,;:!?‘’``''@#$%^_&*()<>{}~\n\t\\\-]", word)) for word in text]
text_content = [word for word in text_content if word not in stopwords]
 
# After the punctuation above is removed it still leaves empty entries in the list.
# Remove any entries where the len is zero.
text_content = [s for s in text_content if len(s) != 0]
 
# Best to get the lemmas of each word to reduce the number of similar words
# on the word cloud. The default lemmatize method is noun, but this could be
# expanded.
# ex: The lemma of 'characters' is 'character'.
text_content = [WNL.lemmatize(t) for t in text_content]
 
# setup and score the bigrams using the raw frequency.
finder = BigramCollocationFinder.from_words(text_content)
bigram_measures = BigramAssocMeasures()
scored = finder.score_ngrams(bigram_measures.raw_freq)



# By default finder.score_ngrams is sorted, however don't rely on this default behavior.
# Sort highest to lowest based on the score.
scoredList = sorted(scored, key=itemgetter(1), reverse=True)
 
# word_dict is the dictionary we'll use for the word cloud.
# Load dictionary with the FOR loop below.
# The dictionary will look like this with the bigram and the score from above.
# word_dict = {'bigram A': 0.000697411,
#             'bigram B': 0.000524882}
 
word_dict = {}
 
listLen = len(scoredList)
 
# Get the bigram and make a contiguous string for the dictionary key. 
# Set the key to the scored value. 
for i in range(listLen):
    word_dict[' '.join(scoredList[i][0])] = scoredList[i][1]
 
word_dict.update({'Analyst Data':0,'Data Analytics':0})

def red_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 99%%, %d%%)" % random.randint(40, 70)

#ASSETS_PATH = BASE_PATH.joinpath("assets").resolve()

#wia_mask = np.array(Image.open(ASSETS_PATH.joinpath("WIA_logo_heavy.jpg")))


# -----
 
# Set word cloud params and instantiate the word cloud.
# The height and width only affect the output image file.
WC_height = 500
WC_width = 1000
WC_max_words = 100
 
wc = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width,stopwords=stopwords, background_color="white")
 
wc.generate_from_frequencies(word_dict)
 
plt.imshow(wc.recolor(color_func=red_color_func, random_state=5), interpolation='bilinear')
plt.axis("off")
plt.show()
wc.to_file("wia_title_wordcloud.png")
print("Title word cloud created.")

# company word cloud 

df2 = attendees_copy['company'].dropna(how='all').astype(str)

df2.replace('CMM','CoverMyMeds',inplace=True)
df2.replace('The James Cancer Hospital/OSUWMC','The James Cancer Hospital',inplace=True)
df2.replace('James Cancer Hospital','The James Cancer Hospital',inplace=True)
df2.replace('OSU - The James','The James Cancer Hospital',inplace=True)
df2.replace('OSUCCC - The James','The James Cancer Hospital',inplace=True)
df2.replace('Ohio State University Wexner Medical Center The James','The Ohio State University Wexner Medical Center',inplace=True)
df2.replace('Nationwide','Nationwide Insurance',inplace=True)

#df2 = "_".join(company_title for company_title in df2)

stopwords = set(STOPWORDS)

# Generate a word cloud image
text_content = [WNL.lemmatize(str(df2)) for t in df2]

tokens = nltk.word_tokenize(str(df2))
text = nltk.Text(tokens)

# Remove extra chars and remove stop words.
text_content = [''.join(re.split("[ .,;:!?‘’``''@#$%^_&*()<>{}~\n\t\\\-]", word)) for word in text]
text_content = [word for word in text_content if word not in stopwords]
 
# After the punctuation above is removed it still leaves empty entries in the list.
# Remove any entries where the len is zero.
text_content = [s for s in text_content if len(s) != 0]
 
# Best to get the lemmas of each word to reduce the number of similar words
# on the word cloud. The default lemmatize method is noun, but this could be
# expanded.
# ex: The lemma of 'characters' is 'character'.
#text_content = [WNL.lemmatize(t) for t in text_content]
 
# setup and score the bigrams using the raw frequency.
finder = QuadgramCollocationFinder.from_words(text_content)
quadgram_measures = QuadgramAssocMeasures()
scored = finder.score_ngrams(quadgram_measures.raw_freq)



# By default finder.score_ngrams is sorted, however don't rely on this default behavior.
# Sort highest to lowest based on the score.
scoredList = sorted(scored, key=itemgetter(1), reverse=True)
 
# word_dict is the dictionary we'll use for the word cloud.
# Load dictionary with the FOR loop below.
# The dictionary will look like this with the bigram and the score from above.
# word_dict = {'bigram A': 0.000697411,
#             'bigram B': 0.000524882}
 
word_dict = {}
 
listLen = len(scoredList)
 
# Get the bigram and make a contiguous string for the dictionary key. 
# Set the key to the scored value. 
for i in range(listLen):
    word_dict[' '.join(scoredList[i][0])] = scoredList[i][1]

def blue_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(240, 99%%, %d%%)" % random.randint(20, 80)

# Set word cloud params and instantiate the word cloud.
# The height and width only affect the output image file.
WC_height = 500
WC_width = 1000
WC_max_words = 100
 
wc = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width, background_color="white",prefer_horizontal=0.7)

wc.generate_from_frequencies(dict(df2.value_counts()))

plt.imshow(wc.recolor(color_func=blue_color_func, random_state=5),interpolation='bilinear')
plt.axis("off")
plt.show()
wc.to_file("wia_company_wordcloud.png")
print('Company word cloud created.')