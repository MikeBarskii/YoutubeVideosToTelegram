import os

import googleapiclient.discovery


def send_request(channel_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ.get("YOUTUBE_DEVELOPER_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY, cache_discovery=False)

    request = youtube.activities().list(
        part="contentDetails",
        channelId=channel_id,
        maxResults=1
    )
    return request.execute()


def get_last_video():
    eliseev_channel_id = "UCSdSBG3MRqhiZv4S1wO39SQ"

    response = send_request(eliseev_channel_id)

    activity = response['items'][0]
    content_info = activity['contentDetails']

    if "upload" in content_info:
        video_id = content_info['upload']['videoId']
        main_part = "https://www.youtube.com/watch?v="

        return main_part + video_id
