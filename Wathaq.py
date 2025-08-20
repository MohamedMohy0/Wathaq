import os
import requests
import gspread
from google.oauth2.service_account import Credentials
from google.auth.exceptions import RefreshError
from gspread.exceptions import APIError


SERVICE_ACCOUNT_FILE = 'Config.json'

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    gc = gspread.authorize(credentials)

    sheet_male = os.environ.get("MALE")
    sh_m = gc.open_by_url(sheet_male)
    worksheet = sh_m.sheet1

    male_values = worksheet.get_all_values()
    num_male = len(male_values)


    sheet_female = os.environ.get("FEMALE")
    sh_fem = gc.open_by_url(sheet_male)
    worksheet = sh_fem.sheet1

    female_values = worksheet.get_all_values()
    num_female = len(female_values)


    prev_num_sheet_url = 'https://docs.google.com/spreadsheets/d/1DVTXQjnrjO3NlFrtUuDIvnTdsn9kRvGxwzvopEAYLlQ/edit?gid=0#gid=0'
    prev_num_sheet = gc.open_by_url(prev_num_sheet_url)
    prev_ws = prev_num_sheet.sheet1

    prev_num_male = prev_ws.acell('A1').value
    prev_male = int(prev_num_male) if prev_num_male else 0

    prev_num_female = prev_ws.acell('B1').value
    prev_female = int(prev_num_female) if prev_num_female else 0

    if num_male > prev_male:
        try:
            prev_ws.update('A1', [[str(num_male)]])
            print("تم تحديث عدد الصفوف في الجدول الثاني.")

            # إرسال رسالة تيليجرام
            bot_token = os.environ.get('BOT_TOKEN')
            chat_id = os.environ.get('MOHY_ID')
            message = f'There is a new Data has arived'
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("Message sent successfully!")
        except:
            print("خطأ في تحديث الجدول:", e)
    elif num_female > prev_female:
        try:
            prev_ws.update('B1', [[str(num_female)]])
            print("تم تحديث عدد الصفوف في الجدول الثاني.")

            # إرسال رسالة تيليجرام
            bot_token = os.environ.get('BOT_TOKEN')
            chat_id = os.environ.get('SAHAD_ID')
            message = f'There is a new Data has arived'
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print(f"Failed to send message: {response.text}")

        except:
            print("خطأ في تحديث الجدول:", e)
except Exception as e:
    bot_token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('MOHY_ID')
    message = f'There is an Error go to check it {e} '
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
            'chat_id': chat_id,
            'text': message
        }
    response = requests.post(url, data=payload)
