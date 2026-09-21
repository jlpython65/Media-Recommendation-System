import json

#May need to update due to youtube changing their website structure

def find_video_ids(obj, video_ids):
    """
    Recursively search for every occurrence of a 'videoId' key.
    """
    # Recursively go down each level until you find 
    # video id. If you do add it to the video_ids
    if isinstance(obj, dict):
        for key, value in obj.items():

            if key == "videoId" and isinstance(value, str):
                video_ids.append(value)

            find_video_ids(value, video_ids)

    elif isinstance(obj, list):
        for item in obj:
            find_video_ids(item, video_ids)


def main():

    with open("outputs/ytInitialData.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    video_ids = []
    find_video_ids(data, video_ids)

    # Remove duplicates while preserving order
    # A dictionary prevents duplicate keys from 
    # being added
    unique_ids = list(dict.fromkeys(video_ids))

    print(f"Found {len(unique_ids)} unique video IDs.")

    # Save as a JSON array
    with open("outputs/video_ids.json", "w", encoding="utf-8") as f:
        json.dump(unique_ids, f, indent=4)

    print("Saved to video_ids.json")


if __name__ == "__main__":
    main()