import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Указываем путь к JSON-файлу с ключами
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', scope)
client = gspread.authorize(credentials)

# Открываем таблицу по названию
sheet = client.open("Название вашей таблицы").sheet1