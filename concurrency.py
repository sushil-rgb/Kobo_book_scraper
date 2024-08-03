"""
This module uses concurrency to perform efficient web scraping operations.

The script defines two main asynchronous functions:
1. isbn_automation: Reads a list of ISBNs from a CSV file, scrapes URLs associated with those ISBNs, and exports the results to a spreadsheet.
2. book_info_automation: Reads a list of book URLs from an Excel file, retrieves detailed book information, and exports the data to a spreadsheet.

Both functions utilize a concurrency module to manage multiple asynchronous scraping tasks, improving performance and efficiency.
"""

from tools import concurrent_scraping, logging_debugging, export_sheet, make_dir
from scraper import get_url_by_isbn, book_info
import pandas as pd
import logging


async def isbn_automation(batches, delay, headless):
    print(f"Initiating concurrent scraping for isbn_automation: Crawling {batches} urls per concurrency. Please wait...")
    # Read and process ISBNs from a Excel file to generate dynamic URLs.
    isbn_lists = pd.read_csv("ISBN13_Kobo - ISBN13_Kobo.csv")['isbn13'].values.tolist()

    dir_name = 'dynamic url datasets'
    file_name = 'isbn13 url datasets'

    # Log the start of the scraping process.
    await logging_debugging()

    # Create a directory before extraction
    await make_dir(dir_name)

    # Perform concurrent scraping to get URLs by ISBN.
    results = await concurrent_scraping(isbn_lists, get_url_by_isbn, batches, delay, headless)

    # Export the results to a spreadsheet.
    return await export_sheet(dir_name, file_name, results)


async def book_info_automation(batches, delay, headless):
    print(f"Initiating concurrent scraping for book_info_automation: Crawling {batches} urls per concurrency. Please wait...")
    # Read and process URLs from an Excel file to retrieve book information.
    book_urls = pd.read_csv("dynamic url datasets//isbn13 url datasets.csv")['url'].values.tolist()
    # Filter the invalid ISBN
    filtered_book_urls = [url for url in book_urls if not 'query' in book_urls]

    dir_name = 'isbn13 datasets'
    file_name = 'isbn13 book datasets'

    # Log the start of the scraping process.
    await logging_debugging()

    # Create a directory before extraction
    await make_dir(dir_name)

    # Perform concurrent scraping to retrieve book information from URLs.
    results = await concurrent_scraping(filtered_book_urls, book_info, batches, delay, headless)

     # Export the results to a spreadsheet.
    return await export_sheet(dir_name, file_name, results)

