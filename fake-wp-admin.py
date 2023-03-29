import os
import datetime
from get_filings.admin_stuff import extract_filings, combine_filings, upload

ticker = input("Ticker (LOWERCASE ONLY): ")
start_date = input("Start date (YYYY-MM-DD) or 'today': ")

if start_date.lower() == "today" or start_date == "":
    start_date = datetime.datetime.today().strftime("%Y-%m-%d")
    print(f"Start date set to {start_date}")

while True:
    try:
        years_ago = int(input(f"How many years before {start_date} to start from: "))
        end_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") - datetime.timedelta(days=years_ago*365)
        end_date = end_date.strftime("%Y-%m-%d")
        break
    except ValueError:
        print("Please enter a valid number of years")

amount = input("Amount of filings per filing type: ")

SEC_API_KEY = "5c7fdaf04888df062770427f16fe8f1b7e3d6c7265e685cda696d24500c3de06"
OPENAI_API_KEY = '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'
PINECONE_API_KEY = '64a2192e-42ae-466b-a79c-b9e0a2e73d87'
PINECONE_API_ENV = 'us-east1-gcp'

extract_filings(ticker, SEC_API_KEY, amount, start_date, end_date)
combine_filings(ticker)
input("Press anything to continue and upload files to Pinecone")
upload(OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_API_ENV, ticker)
