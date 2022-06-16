#%%
from Channel import channel
from Playlist import playlist
import pandas as pd
from collections import defaultdict

def main():
        
    youtubers = {
        "Mark Rober": "UCY1kMZp36IQSyNx_9h4mpCg",
        #"Marques Brownlee":'UUBJycsmduvYEL83R_U4JriQ',
        "Kurzgesagt": 'UCsXVk37bltHxD1rDPwtNM8Q',
        "Joma Tech": 'UCV0qA-eDDICsRR9rPcnG7tw',
        "Linus Tech Tips": 'UCXuqSBlHAE6Xw-yeJA0Tunw',
        "Hacksmith Industries": 'UCjgpFI5dU-D1-kh9H1muoxQ',
        "Jayz Two Cents": "UCkWQ0gDrqOCarmUKmppD7GQ",
        "Lofi Girl": "UCSJ4gkVC6NrvII8umztf0Ow",
        "Dani Game Dev": "UCIabPXjvT5BVTxRDPCBBOOQ",
        "Matt Lowne": "UCiW7-IEQCTqS9l7223whHZA",
        "Seth Everman": "UCoNRSwYHJdy-yV1b82ZdHfQ",
        "VICE": "UCn8zNIfYAQNdrFRrr8oibKw",
        "Smarter Every Day": "UC6107grRI4m0o2-emgoDnAA"
    }
    #%%
    views = {}
    likes = {}
    comments = {}

    for yt in youtubers:
        print(yt)
        ch = channel(youtubers[yt])
        print(ch.get_uploads_id())
        plist = playlist(ch.get_uploads_id())
        vid_data = plist.get_data('statistics')
        vid_data = [defaultdict(int, x) for x in vid_data]
        print(vid_data[0:5])

        metrics = [(vid['viewCount'], vid['likeCount'], vid['commentCount']) for vid in vid_data]
        v, l, c = zip(*metrics)
        print(v)
        print(l)
        print(c)
        views[yt] = list(v)
        likes[yt] = list(l)
        comments[yt] = list(c)
        break
    #%%

    # WORKAROUND
    # Cannot perform standard pd.DataFrame(views) due to unequal list lengths 
    view_df = pd.DataFrame({k: pd.Series(v) for k, v in views.items()})
    like_df = pd.DataFrame({k: pd.Series(v) for k, v in likes.items()})
    comment_df = pd.DataFrame({k: pd.Series(v) for k, v in comments.items()})

    print(view_df.shape)
    print(like_df.shape)
    print(comment_df.shape)
    # %%
