from googleapiclient.discovery import build
import sys
import re 
from datetime import timedelta
import pandas as pd 
import numpy as np
import pprint
import json
import objectpath  

class playlist:
    api_key = 'AIzaSyD2PTenp7crZSbhf-C3_UgvL6-A8Wsobsc'

    vid_fields = ['contentDetails','statistics', 'snippet']

    vid_subfields = [
        ['publishedAt', 'title', 'description', 'channelTitle', 'tags', 'categoryId'],
        ['duration', 'definition', 'caption', 'projection'],
        ['viewCount', 'likeCount', 'commentCount']
    ]

    field_dict = {field : subfield for field, subfield in zip(vid_fields, vid_subfields)}
    
    # Create the API client
    youtube = build('youtube','v3', developerKey=api_key)

    hreg = re.compile("(\d+)H")
    mreg = re.compile("(\d+)M")
    sreg = re.compile("(\d+)S")



    def __init__(self, playlist_id):

        self.responses = []
        self.numitems = 0
        self.video_ids = []

        nextPageToken = None

        while True: 
            # Compile and execute the playlist query 
            pl_response = self.youtube.playlistItems().list(
                    part = 'contentDetails',
                    #channelId = 'UCXvNSR_szKxiAc_eGkmh9cQ'
                    playlistId = playlist_id,
                    maxResults=50, 
                    pageToken = nextPageToken
                ).execute()

            # Retrieve all video ids 
            vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]
            
            self.video_ids += vid_ids
            self.numitems += len(vid_ids)

            # Compile and execute the video query 
            vid_query = self.youtube.videos().list(
                part=",".join(self.vid_fields),
                id=",".join(vid_ids)
                )
            res = vid_query.execute()
            self.responses.append(res)

            ## break out of the infinite loop 
            ## once there are no more pages left to query 
            nextPageToken = pl_response.get("nextPageToken")

            if not nextPageToken:
                break

    ## Private helper method to parse the text duration to integer
    def __get_duration(self, text):
        if not isinstance(text, str):
            return timedelta(0)
        hours = self.hreg.search(text)
        minutes = self.mreg.search(text)
        seconds = self.sreg.search(text)
        
        hours = int(hours.group(1)) if hours else 0 
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        return timedelta(hours = hours, minutes=minutes, seconds=seconds)
    
    def num_videos(self):
        return self.responses[0]

    ## Calculates the total time duration of a playlist 
    def total_duration(self):
        total_time = 0

        for response in self.responses:
            for vid_item in response['items']: 
                print(vid_item['contentDetails'])
                duration = vid_item['contentDetails']['duration']
                total_time += self.__get_duration(duration).total_seconds()

        total_time = timedelta(seconds=total_time)
        #print(total_time.total_seconds())
        return total_time
    
    def get_data(self, field, stat_type=None):
        entries = []
        
        for response in self.responses:
            for vid_item in response['items']: 
                if field == 'statistics' and stat_type:
                    entries.append(vid_item[field][stat_type])
                else:
                    entries.append(vid_item[field])

        return entries

    def get_vid_data(self):
        entries = []

        output_cols = ["videoId"] + sum(self.vid_subfields,[])
        
        # Level: per API reponse 
        for response in self.responses:

            # Level: per video
            for vid_item in response['items']: 

                # Instantiate as json object then as objectpath.Tree object
                json_vid = json.loads(json.dumps(vid_item))
                tree = objectpath.Tree(json_vid)
                vid_entry = []                
                vid_entry.append(vid_item['id'])
                
                # Level: per data entry
                for sf in sum(self.vid_subfields,[]):
                    result = list(tree.execute(f'$..{sf}'))
                    # Found to be relatively fast based on https://nelsonslog.wordpress.com/2016/04/06/python3-no-len-for-iterators/
                    if sf == 'tags':
                        vid_entry.append(result)
                    elif not result:
                        vid_entry.append(np.nan)
                    else:
                        vid_entry.append(result[0])
                    #vid_entry.append(query if sf == "tags" else query[0])

                entries.append(vid_entry)
                # Did this in one line for fun; did not use because less readable
                # [list(tree.execute(f'$..{x}'))[0] if len(list(tree.execute(f'$..{x}'))) == 1 else list(tree.execute(f'$..{x}')) for x in sum(self.vid_subfields,[])]
                # entries.append([vid_item['id']] + [vid_item[field][sf] if sf in vid_item[field].keys() else np.nan for sf in subfields])
        
        result = pd.DataFrame(entries, columns=output_cols)
        
        # Call helper function to clean certain columns before returning 
        result = self.__clean_data(result)
        return result

    # Helper function used to clean the data frame before returning
    def __clean_data(self, df):
        df['duration'] = df['duration'].map(self.__get_duration)
        df['publishedAt'] = pd.to_datetime(df['publishedAt'], format='%Y-%m-%dT%H:%M:%SZ')
        df['description'] = df['description'].str.replace("\n|\r"," ")
        df['description'] = df['description'].str.replace("\d+:\d+","")
        
        counts = ['viewCount', 'likeCount','commentCount']
        df[counts] = df[counts].astype(float)
        newcols = ['log_views', 'log_likes', 'log_comments']
        df[newcols] = df[counts].transform(lambda x: np.log10(x))
        #print(df.dtypes)
        return df

    def get_total_stats(self):
        total_views = 0
        total_likes = 0
        total_comments = 0

        for response in self.responses:
            for item in response['items']: 
                #print(item['statistics'].keys())
                total_views += int(item['statistics']['viewCount'])  if 'viewCount' in item['statistics'] else 0
                total_likes += int(item['statistics']['likeCount']) if 'likeCount' in item['statistics'] else 0
                total_comments += int(item['statistics']['commentCount'])  if 'commentCount' in item['statistics'] else 0
        
        return total_views, total_likes, total_comments


if __name__ == '__main__':
    
    #playlist_id = 'UUBJycsmduvYEL83R_U4JriQ'
    playlist_id = 'PLOshmNuxibvKR1GQ7rXnujPMOIXhXRJ7O'
    pl = playlist(playlist_id)
    print("START:")
    #print(pl.total_duration())
    print(pl.get_vid_data())
    
