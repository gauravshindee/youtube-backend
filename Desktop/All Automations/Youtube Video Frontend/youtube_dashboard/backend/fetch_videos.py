import sqlite3
import pandas as pd
import googleapiclient.discovery
import itertools
import time
from datetime import datetime, timedelta, timezone

# List of API keys to distribute requests
api_keys = ["AIzaSyBPaHfzgR5WjjFRsleNLy3jaEkeMKC5oCw", "AIzaSyDABj0SyfncEo2Ivfzipa05QHntgS3ckXQ", "AIzaSyD1ldfQ0FABISwOg34TG7aLS1uSthKMgJI", "AIzaSyDmj5VuzBeMbhEnMn19fekgm5CkRK4vRPU", "AIzaSyAt9mqKMTuP55dHak2ino1uQoetPA9Cw50", "AIzaSyAiOIzFKIUWFTiwMhNrRcXE5M8zz6rwDuQ"]
api_key_iterator = itertools.cycle(api_keys)

def build_youtube_client():
    api_key = next(api_key_iterator)
    return googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

youtube = build_youtube_client()

brand_channels = {
    "Samsung UK": "UC9KAEEmWnKkiBeskVPDYCZA",
    "Sony Philippines": "UCHd7ya8j4qw27zb2gOhg6dA",
    "Philco Brasil": "UCP2AYtTUq1vowl3MDm0B46Q",
"Reusch": "UCmSFup7i7EkqadgC_8w2I1g",
"LENOXX® Oficial": "UC1SE4aZDz95sTWDmUEY7-NQ",
"Cambridge Audio": "UClrzM8Vc1ecjoGxsFqHsMmQ",
"Mondial Eletrodomésticos": "UCrCG_0FjETX43_IMuuqaZDA",
"Solo Stove": "UCVztOJ7K9JaNTuhyHFsZz1w",
"Weber Grills": "UCEBG5mwkD55WseNJryLdDSw",
"Enders Germany": "UCNAD2vqPaqaTg9zojDmwpOA",
"Sunset BBQ": "UCbbO59yZVmMUHtqUWVY0UYw",
"Samsung Philippines": "UCMVrFdXvbLLPziDG2EClOBQ",
"TCL MEA": "UCp2xjQtNp-3yDo8ilEyf91Q",
"ZTE | nubia Perú": "UC-8rIgT-5mXZ4-H7Qxt0H8Q",
"Samsung South Africa": "UCNHPnm8RtlOecbQvNoBSxZw",
"vivo Colombia": "UCeq_EGGRAmS-Dy6WZdZkPSA",
"realme Malaysia": "UCGTzNXK7ll44XcJWBzs1efA",
"HOKA India": "UCJ3URGL2AD3gZ_HiCiQkQFA",
"Voigtländer": "UCYPLM7nlOAm9jyKBfCiS0iQ",
"foto fantazia": "UCn6XKbGxrsKjoO9AP8ZooYQ",
"Daitsu España": "UCsDfVq9RCx1XdNvSW-9oUvw",
"AEG Australia & New Zealand": "UCtR_ju_-uw-7jmzQrS-cTCQ",
"HMD": "UC8ZbLfj2ByWKkafT6N2hapw",
"LG USA Support": "UCp481MCNVXV3CfmmI_oUq8w",
"Sparkworld Ltd": "UC0wiUStlUYqAkjFAAg1WU4A",
"ECOVACS APAC": "UCNw6_DCBIQQEb1KejCu2BIQ",
"Benelli Bhaktapur": "UCdEYtvL3dCYCd5PF9A_biIw",
"ASUS Singapore": "UCYfADoql3w6SvodxP4b_SNQ",
"CASO Design": "UCxRDnn7gsDdW7NWQ5XGLmmg",
"FRITZ!Box": "UC0YAfafei2jsZ-aPQOCDZZg",
"Netflix Brasil": "UCc1l5mTmAv2GC_PXrBpqyKQ",
"Thonet & Vander": "UCHsoK9VqW8_X1_VGTEFWTbw",
"Braun India": "UCRpQxx4hUh7yyvr2Up1LHYQ",
"SIGMA UK": "UC6WsaehNvjlUTEYJsDj227w",
"ZHIYUN-TECH": "UCeeYm4DCcKiN6hmKBspX8Ig",
"TefalFrance": "UCBjBXQFWikARBT75dyupQ7w",
"Duracell Arabia": "UCuYQXd96FxjyUKvfxNyZKfg",
"VDS-Online": "UCQVqMobKn3iKjwsi_WXmFRA",
"ASUS ROG ES": "UCwgKaTf4XpP0sFOpM_-RHTQ",
"Google": "UCK8sQmJBp8GCxrOtXWBpyEA",
"Tubesca-Comabi": "UCiiudWOV9mAvU9c7VkV4kmA",
"Sudio": "UCWf5NCzMk7GI0XNNJ6tTS5w",
"Goecker since 1862": "UCe-Iya5cAIYOyEM_uKAWWIA",
"Wahlpro": "UCPBKHu3r9javZyytxn5M-yg",
"XIAOMI Israel": "UCGte2E8p7R8_XWqDxe8aVGQ",
"Blaupunkt Car Multimedia & Foldable E-Bikes": "UCYh9kKvLTy5Qyj7Nx8Qs3_A",
"NiloxOfficial": "UCrMlWG9bjqy19MvYYf1otmw",
"TCL Indonesia": "UCRsYMObeP7bM17y77Y9hctQ",
"Video ad upload channel for 297-293-3472": "UCYr04ZUh_Hjjrbhlp18qNrg",
"PlayStation Europe": "UCg_JwOXFtu3iEtbr4ttXm9g",
"JBL Professional": "UCMp9a9-_jAvxVj1caBHbSzw",
"Kärcher México": "UC5KNyIKw94Whb9XvhJpAs-A",
"Sony Philippines": "UCHd7ya8j4qw27zb2gOhg6dA",
"2TTOYS: LEGO, PLAYMOBIL & COBI": "UCuvXd5X-18szDPlV0APoSGQ"
    
    
}

DB_FILE = "youtube_videos.db"

def fetch_videos(channel_id):
    try:
        youtube = build_youtube_client()
        last_24_hours = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=5,
            order="date",
            type="video",
            publishedAfter=last_24_hours
        )
        response = request.execute()
        return response.get('items', [])
    except Exception as e:
        print(f"Error fetching videos for {channel_id}: {e}")
        return []

def store_videos(videos, brand):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for video in videos:
        video_id = video['id']['videoId']
        title = video['snippet']['title']
        url = f"https://www.youtube.com/watch?v={video_id}"
        published_at = video['snippet']['publishedAt']

        cursor.execute("INSERT OR IGNORE INTO videos VALUES (?, ?, ?, ?, ?, ?)",
                       (video_id, brand, title, url, published_at, "Not Reviewed"))

    conn.commit()
    conn.close()

for brand, channel_id in brand_channels.items():
    videos = fetch_videos(channel_id)
    if videos:
        store_videos(videos, brand)
