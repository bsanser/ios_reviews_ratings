import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from datetime import datetime
import logging


WORKSHEET_NAME = 'Elvie'
SHEET_KEY = '1JVASU7_q7INztsT3Rd9KlmA1nBTzHcsWNw1_9EvvNEo'


def save_to_gsheets(df):
  try:
    gc = gspread.service_account(filename='ios-reviews-416220-843253c160dc.json')
    spreadsheet = gc.open_by_key(SHEET_KEY)
    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    set_with_dataframe(worksheet, df)
    worksheet.update('I1', 'Last updated on:')
    worksheet.update('I2', [[datetime.now().strftime('%Y-%m-%d %H:%M:%S')]])
  except Exception as e:  
    print(f'Worksheet not found. Check that the name in worksheet_name is correct: {e}')

def update_gsheets(new_df):   
  try:
    gc = gspread.service_account(filename='ios-reviews-416220-843253c160dc.json')
    spreadsheet = gc.open_by_key(SHEET_KEY)
    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    existing_df = get_as_dataframe(worksheet)
    combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['title', 'body']).sort_values(by='date', ascending=False)
    cols = ['date', 'country', 'user_rating', 'title', 'body', 'vote_sum', 'vote_count', 'app_version']
    set_with_dataframe(worksheet, combined_df[cols], include_index=False, include_column_header=True, resize=True)
    worksheet.update('I2', [[datetime.now().strftime('%Y-%m-%d %H:%M:%S')]])
    logging.info(f"Script executed successfully at {datetime.datetime.now()}")

    print(f'End time: {datetime.now()}')

  except Exception as e:  
    logging.error(f"Error encountered: {e}")
    print(f'Something happened: {e}')

  