import praw
import pandas as pd
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import json

def remove_common_words_symbols_and_nums(dataframe, column):
    """Removes common words and numbers from text strings in a dataframe column"""

    s = (stopwords.words('english')) #nltk stopwords dictionary
    dataframe.dropna(inplace=True)
    dataframe[column] = dataframe[column].astype('str')
    dataframe = dataframe[dataframe[column] != '[removed]']
    dataframe = dataframe[dataframe[column] != '[deleted]']
    dataframe[column] = dataframe[column].str.replace(r'(https?:\ / \ /)(\s)*(www\.)?(\s) * ((\w | \s) +\.) * ([\w\-\s]+\ /) * ([\w\-]+)((\?)?[\w\s] *= \s * [\w\ % &] * ) *', ' ')
    dataframe[column] = dataframe[column].str.replace(r'[^a-zA-Z]+', ' ')
    dataframe[column] = dataframe[column].str.replace('mr', '')
    dataframe[column] = dataframe[column].str.lower()
    dataframe[column] = dataframe[column].apply(lambda x: ' '.join([item for item in x.split() if item not in s]))

    return dataframe



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

urls = ["https://www.reddit.com/r/The_Donald/comments/4uxdbn/im_donald_j_trump_and_im_your_next_president_of/"]#,
         # "https://www.reddit.com/r/The_Donald/comments/5bzjv5/donald_j_trump_declared_the_winner/",
         # "https://www.reddit.com/r/The_Donald/comments/5jt9xs/cnn_will_soon_be_1when_searching_for_the_term/",
         # "https://www.reddit.com/r/The_Donald/comments/5bz5ds/all_celebrities_that_vowed_to_leave_the_usa_if/",
         # "https://www.reddit.com/r/The_Donald/comments/5byneu/imminent_victory_thread/",
         # "https://www.reddit.com/r/The_Donald/comments/5cxunu/its_official_trump_will_become_the_first_us/",
         # "https://www.reddit.com/r/The_Donald/comments/5c2t5d/press_f_to_pay_respect/",
         # "https://www.reddit.com/r/The_Donald/comments/5cax76/youtube_removed_countless_copies_of_this_video_of/",
         # "https://www.reddit.com/r/The_Donald/comments/5tqp0b/her_name_is_nazi_paikidze_and_shes_the_united/",
         # "https://www.reddit.com/r/The_Donald/comments/5fsgz9/when_you_tear_out_a_mans_tongue_you_havent_proved/",
         # "https://www.reddit.com/r/The_Donald/comments/59vld8/this_just_in_from_chaffetz_fbi_dir_just_informed/"]

comment_body_list = []
for url in urls:
    print('done')
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)
    all_comments = submission.comments.list()
    for comment in all_comments:
        comment_body_list.append(comment.body)

comment_df = pd.DataFrame(data=comment_body_list,columns=['comment'])
comment_df = remove_common_words_symbols_and_nums(comment_df,'comment')

words_comments = comment_df['comment'].str.split()
flat_list = [item for sublist in list(words_comments) for item in sublist]
words = pd.DataFrame({'word':flat_list})
word_count_df = words['word'].value_counts().to_frame().reset_index()
print(words.size)
print(word_count_df.nlargest(100,'word'))

d = {}
for a, x in word_count_df.values:
    d[a] = x

trump_mask = np.array(Image.open('word_mask_silhouettes/trump.jpg'))

wordcloud = WordCloud(width=400, height=400,
                      mask=trump_mask,
                      background_color='white',
                      min_font_size=5).generate_from_frequencies(d)

# plot the WordCloud image
plt.figure(figsize=(6, 6), facecolor=None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()