import praw
import pandas as pd
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import json

def _remove_common_words_symbols_and_nums(dataframe, column):
    """Removes common words and numbers and other unwanted characters from text strings in a dataframe column"""

    s = (stopwords.words('english')) #nltk stopwords dictionary
    dataframe.dropna(inplace=True)
    dataframe[column] = dataframe[column].astype('str')
    dataframe = dataframe[dataframe[column] != '[removed]']
    dataframe = dataframe[dataframe[column] != '[deleted]']
    dataframe[column] = dataframe[column].str.replace(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', ' ')
    dataframe[column] = dataframe[column].str.replace(r'[^a-zA-Z]+', ' ')
    dataframe[column] = dataframe[column].str.replace('mr', '')
    dataframe[column] = dataframe[column].str.lower()
    dataframe[column] = dataframe[column].apply(lambda x: ' '.join([item for item in x.split() if item not in s]))

    return dataframe


def create_word_cloud(urls_list,silouette_file_path):

    print(silouette_file_path)

    with open('/Users/mike/Documents/login_details.json', 'r') as myfile:
        data=myfile.read()

    obj = json.loads(data)

    clientID = obj.get("client_id")
    clientSecret = obj.get("client_secret")
    password = obj.get("password")
    userAgent = obj.get("user_agent")
    username = obj.get("username")


    reddit = praw.Reddit(client_id=clientID,
                        client_secret=clientSecret,
                        password=password,
                        user_agent=userAgent,
                        username=username)


    comment_body_list = []
    for url in urls_list:
        print('done')
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=0)
        all_comments = submission.comments.list()
        for comment in all_comments:
            comment_body_list.append(comment.body)

    comment_df = pd.DataFrame(data=comment_body_list,columns=['comment'])
    comment_df = _remove_common_words_symbols_and_nums(comment_df,'comment')

    words_comments = comment_df['comment'].str.split()
    flat_list = [item for sublist in list(words_comments) for item in sublist]
    print(len(flat_list))
    words = pd.DataFrame({'word':flat_list})
    word_count_df = words['word'].value_counts().to_frame().reset_index()
    print(words.size)
    print(word_count_df.nlargest(100,'word'))

    if silouette_file_path=='word_mask_silhouettes/trump.jpg':
        word_count_df.to_csv('the_donald_words.csv')
    else:
        word_count_df.to_csv('sanders_for_president_words.csv')



    d = {}
    for a, x in word_count_df.values:
        d[a] = x

    mask = np.array(Image.open(silouette_file_path))

    wordcloud = WordCloud(width=400, height=400,
                        mask=mask,
                        background_color='white',
                        min_font_size=5).generate_from_frequencies(d)

    # plot the WordCloud image
    plt.figure(figsize=(6, 6), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()