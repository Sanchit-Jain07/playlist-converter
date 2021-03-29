from googleapiclient.discovery import build
import json
import re
import youtube_dl

api_key = 'AIzaSyBnRsp-ibDeFAhfLY8SU2zD_V6Rh5GaUpk'

youtube = build('youtube', 'v3', developerKey=api_key)



hours_pattern =  re.compile(r'(\d+)H')
minutes_pattern =  re.compile(r'(\d+)M')
seconds_pattern =  re.compile(r'(\d+)S')

def get_playlist_songs(id):
    titles=[]
    nextPageToken = None
    while True:
        pl_name = youtube.playlists().list(
            part='snippet',
            id=id
        )
        pl_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=id,
            maxResults=50,
            pageToken=nextPageToken
        )

        response = pl_request.execute()
        name_response = pl_name.execute()
        name = name_response['items'][0]['snippet']['title']
        vid_ids = []
        # print(json.dumps(name, indent=2))
        for item in response['items']:
            # titles.append(item['snippet']['title'])
            youtube_url = 'https://www.youtube.com/watch?v=' + item['snippet']['resourceId']['videoId']
            try:
                video = youtube_dl.YoutubeDL({}).extract_info(
                    youtube_url, download=False)

                song_name = video['track']
                artist = video['artist']

                titles.append(song_name + '-' + artist)
            except:
                titles.append(item['snippet']['title'])
        #     vid_ids.append(item['contentDetails']['videoId'])

        # vid_request = youtube.videos().list(
        #     part='contentDetails',
        #     id=','.join(vid_ids)
        # )

        # vid_response = vid_request.execute()


        # for item in vid_response['items']:
        #     print(json.dumps(item, indent=2))
            # duration = item['contentDetails']['duration']
            # hours = hours_pattern.search(duration)
            # minutes = minutes_pattern.search(duration)
            # seconds = seconds_pattern.search(duration)

            # hours = int(hours.group(1)) if hours else 0
            # minutes = int(minutes.group(1)) if minutes else 0
            # seconds = int(seconds.group(1)) if seconds else 0
            
            # print(hours, minutes, seconds)
        
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    
    return titles,name

# print(titles)
# print('\n'.join(titles))
# get_playlist_songs('PL9tY0BWXOZFtynbPGh-GPxTsCGAW35GgW')
# get_playlist_songs('PL9tY0BWXOZFtynbPGh-GPxTsCGAW35GgW')