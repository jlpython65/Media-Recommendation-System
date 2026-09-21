import json
import os

from googleapiclient.discovery import build
from dotenv import load_dotenv


# 1. Load id json
# 2. Build a request for a list of videos
# 3. Input ids into request
# 4. Execute request
# 5. Filter out metadata from response
# 6. Write metadata into JSON


#Can we not get metadata from the ytinitialData json itself?
#1 The json file does not have the engagement metrics
#2 I rather not run a recursive search for each attribute 

load_dotenv()
API_KEY = os.environ["YOUTUBE_API_KEY"]

#Configure youtube api
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


def load_video_ids():
    with open("outputs/video_ids.json", "r", encoding="utf-8") as f:
        return json.load(f)



#https://developers.google.com/youtube/v3/docs/videos/list

def lookup_videos(video_ids):
    request = youtube.videos().list(
        # part is a parameter of the list method 
        # it returns the objects for each video id 

        #In this example, we're asking for the snippet, 
        # contentDetails, and statistics objects for each video in 
        # the ids
        part="snippet,contentDetails,statistics",
        # id=",".join(video_ids[:10])      # Only first 10

        #The id parameter value is a comma-separated list of YouTube 
        # video IDs. 

        #Look up all ids by giving the entire video_ids array
        id=",".join(video_ids)
    )

    #video_objects is the json that's returned after executing a request
    video_objects = request.execute()
    
    video_metadata = []

    #video_objects body has an items field which is where the video resources are stored

    for item in video_objects["items"]:
        #Access to video_objects item field allows you to look at the 
        #parts you requested earlier snippet, content, and stats
        video_metadata.append({
            "videoId": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "publishedAt": item["snippet"]["publishedAt"],
            "description": item["snippet"]["description"],
            "duration": item["contentDetails"]["duration"],
            "views": item["statistics"].get("viewCount"),
            "likes": item["statistics"].get("likeCount"),
            "commentCount": item["statistics"].get("commentCount")
        })

    return video_metadata


def main():

    #open video json as read and return the json file to ids
    ids = load_video_ids()

    print(f"Looking up {len(ids)} videos...")

    #look up all ids
    video_metadata = lookup_videos(ids)

    #write all video data from videos in to videos.json
    with open("outputs/videos.json", "w", encoding="utf-8") as f:
        json.dump(video_metadata, f, indent=4)

    print("Saved videos.json")


if __name__ == "__main__":
    main()