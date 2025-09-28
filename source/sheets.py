# Google sheet test

import datetime as dt
import gspread
from google.oauth2.service_account import Credentials


if __name__ == "__main__":
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    
    sheet_id = "1w-x0LixyleudwIxJlqzFFqg_BWGZ0_FQiQ19KQRObFk"
    sheet = client.open_by_key(sheet_id)

    values_list = sheet.sheet1.row_values(1)
    print(values_list)
