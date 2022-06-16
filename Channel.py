from googleapiclient.discovery import build
import sys
import re 
from datetime import timedelta
from Playlist import playlist
from collections import defaultdict

class channel:
    api_key = 'AIzaSyD2PTenp7crZSbhf-C3_UgvL6-A8Wsobsc'
    

    def __init__(self, channel_id):
        # Create the API client
        youtube = build('youtube','v3', developerKey=self.api_key)

        ch_response = youtube.channels().list(
            part = 'contentDetails,statistics,snippet',
            #channelId = 'UCXvNSR_szKxiAc_eGkmh9cQ'
            id = channel_id,
            maxResults=5
        ).execute()

        # if ch_response['pageInfo']['totalResults'] != 1:
        #     print("ERROR: Multiple results found.")
            
        self.data = ch_response['items'][0]
        self.uploads_id = self.data['contentDetails']['relatedPlaylists']['uploads']
        self.uploads = playlist(self.uploads_id)
    
    # Retrieves data from a specified field
    def get_data(self, field):
        if field in self.data.keys():
            return self.data[field]
        return None

    # Retrieves the ID for all channel uploads
    def get_uploads_id(self):
        return self.data['contentDetails']['relatedPlaylists']['uploads']

    # Retrieves all playlist data by calling the playlist object
    def get_all_data(self):
        return self.uploads.get_vid_data()



# --- TESTING ---
# if __name__ == '__main__':
#     id = 'UCY1kMZp36IQSyNx_9h4mpCg'
#     ch = channel(id)

#     print(ch.get_data('statistics'))
#     print(ch.get_playlist())

