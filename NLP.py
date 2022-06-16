#%%
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from Channel import channel
from Playlist import playlist
from collections import defaultdict
import matplotlib.pyplot as plt


class nlp:

    vect = TfidfVectorizer(stop_words={'english'})
    tfdata = []

    cluster = []
    plotdata = None

    def __init__(self, text):
        self.tfdata = self.vect.fit_transform(text)
        self.pca_complete = False
        self.kmeans_complete = False


    # function to run KMeans clustering using the elbow method 
    def get_kmeans_clusters(self):

        if self.kmeans_complete:
            print("KMeans already run.")
            return 

        print("Running elbow...")
        scores = []

        # run a quick hyperparameter search 
        test_vals = np.arange(2,12)
        for k in test_vals:
            km = KMeans(n_clusters=k, max_iter=300)
            km = km.fit(self.tfdata)
            scores += [km.inertia_]

        # locate the argmin of Kmeans inertial scores 
        best_k = np.argmin(scores)

        # create the best KMeans model and fit it  
        model = KMeans(n_clusters=test_vals[best_k], max_iter=300)
        model.fit(self.tfdata)

        # predict 
        predictions = model.predict(self.tfdata)

        # record results and success
        self.cluster = predictions
        self.kmeans_complete = True

        return predictions

    def get_plot_data(self):
        print("Running PCA...")

        if self.pca_complete:
            print("PCA already run.")
            return 
        pca = PCA(n_components=2)

        two_dims = pca.fit_transform(self.tfdata.todense())

        self.pca_complete = True
        self.plotdata = two_dims

        return two_dims

    def create_plot(self):
        print("Creating plot...")

        if not self.pca_complete or not self.kmeans_complete:
            print("Prequisite data not complete.")
            return 

        # create a scatter plot
        plt.scatter(self.plotdata[:,0], self.plotdata[:,1], c=self.cluster)
        plt.show()
    

        

def main():
    youtubers = {
        "Kurzgesagt": 'UCsXVk37bltHxD1rDPwtNM8Q',
        "Mark Rober": "UCY1kMZp36IQSyNx_9h4mpCg",
        #"Marques Brownlee":'UUBJycsmduvYEL83R_U4JriQ',
        "Joma Tech": 'UCV0qA-eDDICsRR9rPcnG7tw',
        # "Linus Tech Tips": 'UCXuqSBlHAE6Xw-yeJA0Tunw',
        # "Hacksmith Industries": 'UCjgpFI5dU-D1-kh9H1muoxQ',
        # "Jayz Two Cents": "UCkWQ0gDrqOCarmUKmppD7GQ",
        # "Lofi Girl": "UCSJ4gkVC6NrvII8umztf0Ow",
        # "Dani Game Dev": "UCIabPXjvT5BVTxRDPCBBOOQ",
        # "Matt Lowne": "UCiW7-IEQCTqS9l7223whHZA",
        # "Seth Everman": "UCoNRSwYHJdy-yV1b82ZdHfQ",
        # "VICE": "UCn8zNIfYAQNdrFRrr8oibKw",
        # "Smarter Every Day": "UC6107grRI4m0o2-emgoDnAA"
    }
    

    #for name, id in youtubers.items():
        # ch = channel(youtubers[yt])
        # print(ch.get_uploads_id())
        # plist = playlist(ch.get_uploads_id())
        # vid_data = plist.get_data('snippet')
        # vid_data = [(x['title'], x['description']) for x in vid_data]
        # lens += [len(vid_data)]

    ch = channel(youtubers['Kurzgesagt'])

    df = ch.get_all_data()
    df = df[['title', 'description','tags']]
    df['tags'] = df['tags'].map(lambda x: " ".join(x))
    df = df.loc[df['tags'] != '']

    print("Running NLP on tags...")
    tag_nlp = nlp(df['tags'].squeeze())

    tag_nlp.get_kmeans_clusters()
    tag_nlp.get_plot_data()
    tag_nlp.create_plot()


    print("Running NLP on combined text data...")
    all_df = df['combined'] = df['title'] + " " + df['description'] + " " + df['tags']
    all_nlp = nlp(df['combined'].squeeze())

    all_nlp.get_kmeans_clusters()
    all_nlp.get_plot_data()
    all_nlp.create_plot()

    #df['cluster'] = results
    # metrics = [(vid['viewCount'], vid['likeCount'], vid['commentCount']) for vid in vid_data]
    

#%%
if __name__ == '__main__':
    main()

# %%
