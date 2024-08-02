# Rakuted KOBO Scraper

## Overview

This project automates the process of retrieving dynamic URLs and detailed book information from an online bookstore using asynchronous tasks. The script performs two main functions:

1. **ISBN Automation**: Searches for book URLs using ISBN numbers and stores the results for further processing.
2. **Book Info Automation**: Uses the dynamic URLs obtained from the previous step to scrape detailed information about each book, including title, author, price, and other metadata.

The script leverages Python's `asyncio` library to handle multiple requests concurrently, making the process efficient while preventing server overload.

## Key Features

- **Concurrent Requests**: Handles multiple requests in parallel to speed up the scraping process.
- **Dynamic URL Retrieval**: Fetches dynamic URLs based on ISBN numbers.
- **Detailed Book Information**: Scrapes comprehensive book details including title, author, price, and other relevant metadata.
- **Asynchronous Execution**: Utilizes `asyncio` for non-blocking operations, improving performance.

## Setup and Configuration

### Parameters

- **`batches`**: Number of requests to process concurrently in each batch. Increasing the batch size can speed up the process but may require more system resources (e.g., RAM) as it opens multiple browser instances.
- **`delay`**: Delay (in seconds) between each batch of requests. Adjust this parameter to control the request rate and avoid overloading the server.
- **`headless`**: Boolean flag to run the browser in headless mode (without GUI). Set to `True` for a more efficient execution.

### Dependencies

Ensure you install the necessary requirements:

```bash
pip install -r requirements.txt
