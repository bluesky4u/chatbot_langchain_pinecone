import os
import datetime
from get_filings.admin_stuff import extract_filings, combine_filings, upload
import dotenv

dotenv.load_dotenv()
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

SEC_API_KEY = os.environ.get('SERPAPI_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

extract_filings(ticker, SEC_API_KEY, amount, start_date, end_date)
combine_filings(ticker)
input("Press anything to continue and upload files to Pinecone")
upload(OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_API_ENV, ticker)
