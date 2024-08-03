"""
This module provides asynchronous web scraping functionalities to retrieve book information from the Kobo website.

It contains two primary functions:

1. get_url_by_isbn: Searches for a book on Kobo using its ISBN and retrieves the URL of the book's page.
2. book_info: Extracts detailed information from a Kobo book page, including title, author, price, and other metadata.

The module utilizes the Playwright library to automate browser interactions and BeautifulSoup for parsing HTML content.
It includes error handling and logging to capture and report any issues encountered during the scraping process.
"""


from tools import TryExcept, load_selectors, userAgents
from playwright.async_api import async_playwright
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re


# Function to search for a book URL on Kobo using an ISBN number
async def get_url_by_isbn(isbn, headless):
    infos = []
    css_selector = await load_selectors("html_selectors")

    # Initiating the Playwright automation:
    async with async_playwright() as play:
        browser = await play.chromium.launch(headless=headless)
        context = await browser.new_context(user_agent=await userAgents())
        page = await context.new_page()

        try:
            logging.info(f"Navigating to Kobo page for ISBN: {str(isbn)}")
            await page.goto("https://www.kobo.com/us/en", wait_until = "domcontentloaded", timeout = 120 * 10000)

            # Attempt to close any pop-up that might appear
            try:
                close_button = page.locator(css_selector['close_button'])
                await close_button.click()
                logging.info("Closed pop-up window.")
            except Exception as e:
                logging.warning("Close button not found or click failed:", e)

            # Find and click the search box to enter the ISBN
            await page.wait_for_selector(css_selector['search_box'], timeout= 60 * 10000)
            # Select the first search box element on the page using the specified CSS selector
            search_box = page.locator(css_selector['search_box']).nth(0)
            await search_box.click()
            logging.info("Clicked on the search box.")

            # Type the ISBN into the search box and submit the search
            await page.keyboard.type(str(isbn))
            submit_button = page.locator(css_selector['submit_button'])
            await submit_button.wait_for(state="visible")
            await submit_button.click()
            logging.info(f"Submitted search for ISBN: {isbn}")

            # Get the current URL
            new_url = page.url
            print(isbn, new_url)

            # Store the results
            datas = {
                'isbn': isbn,
                'url': new_url
            }
            infos.append(datas)
        except Exception as e:
            logging.error(f"Error processing ISBN {isbn}: {str(e)}")
        finally:
            # Ensure the browser context is closed
            await context.close()
            await browser.close()

        return infos


# Function to scrape detailed book information from a Kobo book page
async def book_info(url, headless):
    info = []
    current_timestamp = datetime.now()

    # Format the current timestamp for logging purposes
    formatted_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    css_selector = await load_selectors("html_selectors")

    # Initiating the Playwright automation:
    async with async_playwright() as play:
        browser = await play.firefox.launch(headless = headless)
        context = await browser.new_context(user_agent = await userAgents(),
                                            viewport={'width': 1920, 'height': 1080},
            )
        page = await context.new_page()

        try:
            await page.goto(url, wait_until = 'domcontentloaded', timeout = 120 * 10000)

            # Attempt to close any pop-up that might appear
            try:
                await (await page.query_selector(css_selector['close_button'])).click()
            except Exception as e:
                logging.warning(f"No close button found: {str(e)}")

            # Explicitly wait for the ratings element to ensure it is loaded, as rendering can be slow at times
            await page.wait_for_selector(css_selector['ratings'], timeout = 15 * 10000)

            # Retrieve and parse the page content using BeautifulSoup
            page_content = await page.content()
            soup = BeautifulSoup(page_content, 'lxml')

            catch_exception = TryExcept()

            book_title = soup.select_one(css_selector['book_title']).text.strip()
            logging.info(f"Processing book: {book_title}")

            book_details = soup.select(css_selector['book_details'])
            about_this_book = soup.select(css_selector['about_this_book'])

            # Handle cases where certain book details may be missing
            try:
                number_of_pages = about_this_book[0].text.strip()
            except IndexError:
                number_of_pages = "N/A"
            try:
                hours_to_read = about_this_book[1].text.strip()
            except IndexError:
                hours_to_read = "N/A"
            try:
                total_words = about_this_book[2].text.strip()
            except IndexError:
                total_words = "N/A"

            # Regex pattern to clean up category rankings
            category_rankings_pattern = r'r\\n|\s+'

            # Collect all book information in a dictionary
            datas = {
                'region': 'US',
                'retailer': 'Kobo US',
                'asin': '',
                'isbn13': book_details[3].text.strip().replace("ISBN: ", ''),
                'title_name': book_title,
                'authors': soup.select_one(css_selector['authors']).text.strip(),
                'sales_rank': '',
                'list_price': await catch_exception.text(soup.select_one(css_selector['was_price'])),
                'print_list_price': '',
                'price': await catch_exception.text(soup.select_one(css_selector['is_price'])),
                'currency': 'USD',
                'timestamp': formatted_timestamp,
                'synopsis': soup.select_one(css_selector['synopsis']).text.strip(),
                'imprint_i': book_details[0].text.strip(),
                'release_date': book_details[1].text.strip().replace("Release Date: ", ''),
                'imprint_ii': book_details[2].text.strip().replace("Imprint: ", ''),
                'language': book_details[4].text.strip().replace("Language: ", ''),
                'download_options': book_details[5].text.strip().replace("Download options: ", ''),
                'number_of_pages': number_of_pages,
                'hours_to_read': hours_to_read,
                'total_words': total_words,
                'rating': soup.select_one(css_selector['ratings']).get('aria-label'),
                'category_rankings': re.sub(category_rankings_pattern, ' ', soup.select_one(css_selector['category_rankings']).text.strip()),
                'image': urljoin(url, soup.select_one(css_selector['img_url']).get('src')),
                'url': url,

            }
            info.append(datas)
            return info
        except Exception as e:
            logging.error(f"Error processing url {url}: {str(e)}")
        finally:
            # Ensure the browser context is closed
            try:
                await context.close()
            except Exception as e:
                logging.error(f"Error closing context {url}: {str(e)}")
            try:
                await browser.close()
            except Exception as e:
                logging.error(f"Error closing browser {url}: {str(e)}")

