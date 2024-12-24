import requests

ACCESS_TOKEN = 'your_access_token'
INSTAGRAM_USER_ID = 'your_instagram_user_id'

# Step 1: Fetch media
def get_media(ig_user_id, access_token):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media?fields=id,caption&access_token={access_token}"
    response = requests.get(url)
    return response.json()

# Step 2: Fetch comments for a specific media ID
def get_comments(media_id, access_token):
    url = f"https://graph.facebook.com/v17.0/{media_id}/comments?fields=id,text,username,timestamp&access_token={access_token}"
    response = requests.get(url)
    return response.json()

# Example Usage
media = get_media(INSTAGRAM_USER_ID, ACCESS_TOKEN)
print("Media:", media)

if "data" in media and media["data"]:
    first_media_id = media["data"][0]["id"]  # Fetch the first media ID
    comments = get_comments(first_media_id, ACCESS_TOKEN)
    print("Comments:", comments)
