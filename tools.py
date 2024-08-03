"""
This module provides various utilities to aid the web scraping process.

It includes functionalities such as:

1. Logging setup to capture debugging information and errors.
2. Checking server response status codes for given URLs.
3. Mechanisms to handle missing or null values when extracting data.
4. Exporting extracted data to a CSV file.
5. Rotating user agents for each request to mimic different browsers and prevent blocking.
6. Loading CSS selectors from configuration files for easy maintenance.
7. Concurrently scraping multiple URLs with controlled batching and delays.

The module utilizes libraries such as aiohttp for asynchronous HTTP requests, pandas for data manipulation,
and PyYAML for configuration management.
"""


from fake_useragent import UserAgent
import pandas as pd
import logging
import aiohttp
import asyncio
import yaml
import os


# Setup logging for debugging purposes
async def logging_debugging(name, level = logging.DEBUG):
    logging.basicConfig(
        level = level,
        format = "%(asctime)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(f"{name}.log"),
            logging.StreamHandler()
        ]
    )


# Check the status code of a response from the server
async def response(base_url):
    async with aiohttp.ClientSession() as session:
        headers = {'User-Agent': await userAgents()}
        async with session.get(base_url, headers = headers) as resp:
            status_code = resp.status
            return status_code


# Mechanism to handle missing or null values in extracted data
class TryExcept:
    async def text(self, element):
        try:
            elements = element.text.strip()
        except AttributeError:
            elements = "N/A"
        return elements

    async def attributes(self, element, attr):
        try:
            elements = element.get(attr)
        except AttributeError:
            elements = "N/A"
        return elements


# Create a directory before extraction:
async def make_dir(directory_name):
    # Create a directory before saving the spreadsheet if it doesn't exist
    path_directory = os.path.join(os.getcwd(), directory_name)

    if os.path.exists(path_directory):
        pass
    else:
        os.mkdir(path_directory)


# Save extracted data into a CSV file
async def export_sheet(directory_name, file_name, dicts):
    df = pd.DataFrame(data = dicts)
    df.to_csv(f"{directory_name}//{file_name}.csv", index = False)


# Rotate user-agents for each request to avoid detection
async def userAgents():
    agents = UserAgent()
    return agents.random


# Load CSS selectors from a configuration file
async def load_selectors(selectors):
    with open(f"{selectors}.yaml") as file:
        sel = yaml.load(file, Loader=yaml.SafeLoader)
        return sel


# Concurrently scrape multiple URLs with batching and delay
async def concurrent_scraping(url_lists, scraping_functions, batch_sizes, delay_between_batches, headless):
    print(f"Initiating concurrent scraping: Crawling {batch_sizes} url per concurrency. Please wait...")
    dfs = []
    for idx in range(0, len(url_lists), batch_sizes):
        batch_urls = url_lists[idx:idx + batch_sizes]
        coroutines = [scraping_functions(url, headless) for url in batch_urls]
        batch_urls_results = await asyncio.gather(*coroutines)

        batch_dataframes = [pd.DataFrame(batch_url_result) for batch_url_result in batch_urls_results]
        dfs.extend(batch_dataframes)

        # Introduce a delay between batches to manage server load
        await asyncio.sleep(delay_between_batches)

    # Concatenate all dataframes from batches into a final dataframe
    final_dataframe = pd.concat(dfs)
    return final_dataframe

