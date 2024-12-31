import requests
import openpyxl as xl

with open('access_token', 'r') as file:
    access_token = file.read()

API = "https://graph.instagram.com/v21.0"
ACCESS = f"access_token={access_token}"
media_fields = ['id', 'caption','media_product_type','media_type','permalink','timestamp','like_count', 'comments_count']

def create_xl(name):
    workbook = xl.Workbook()
    sheet = workbook.active
    sheet.title = "Posts"
    sheet.append(media_fields)
    for column in sheet.columns:
        sheet.column_dimensions[column[0].column_letter].width = max(10, len(str(column[0].value)) + 2)
    workbook.save(f'{name}.xlsx')
    return workbook

def edit_margins(workbook):
    sheet = workbook.active
    for column in sheet.columns:
        sheet.column_dimensions[column[0].column_letter].width = 20

def open_xl(filename):
    workbook = xl.load_workbook(filename)
    return workbook

def add_all_media(media_list, workbook):
    for media in media_list:
        data = get_media_info(media['id'])
        sheet = workbook.active
        row = [data[key] for key in media_fields]
        sheet.append(row)

def get_username():
    url = f"{API}/me?fields=user_id,username&{ACCESS}"
    username = requests.get(url)
    return username.json()["user_id"]

def get_post_count(ig_user_id):
    url = f"{API}/{ig_user_id}?fields=media_count&{ACCESS}"
    return requests.get(url).json()["media_count"]

# Step 1: Fetch media
def get_media_ids(ig_user_id):
    data = []
    url = f"{API}/{ig_user_id}/media?{ACCESS}"
    response = requests.get(url)
    json = response.json()
    data += json['data']
    while 'next' in json['paging']:
        response = requests.get(json['paging']['next'])
        json = response.json()
        data += json['data']
    return data

# Step 2: Fetch comments for a specific media ID
def get_comments(media_id):
    url = f"{API}/{media_id}/comments?fields=id,text,username,timestamp&{ACCESS}"

    response = requests.get(url)
    return response.json()

def get_media_info(media_id):
    fields = ",".join(media_fields)
    url = f"{API}/{media_id}/?fields={fields}&{ACCESS}"
    response = requests.get(url)
    return response.json()

# Example Usage
# media = get_media(INSTAGRAM_USER_ID, ACCESS_TOKEN)
# print("Media:", media)

# if "data" in media and media["data"]:
    # first_media_id = media["data"][0]["id"]  # Fetch the first media ID
    # comments = get_comments(first_media_id, ACCESS_TOKEN)
    # print("Comments:", comments)

user_id = get_username()
total_posts = get_post_count(user_id)
medias = get_media_ids(user_id)
#create_xl("InstagramSummary")
sheets = open_xl("InstagramSummary.xlsx")
#edit_margins(sheets)
add_all_media(medias, sheets)
sheets.save("InstagramSummary.xlsx")
