"""
This script automates the process of retrieving dynamic URLs and detailed book information
from an online bookstore using asynchronous tasks.

The script consists of two main asynchronous functions:

1. isbn_automation: Automates the search for dynamic book URLs using ISBN numbers and stores
   the results for further processing.

2. book_info_automation: Uses the dynamic URLs obtained from the previous step to scrape
   detailed information about each book, such as the title, author, price, and other metadata.

The script utilizes asyncio for concurrent execution, allowing efficient handling of multiple requests by
batching them and introducing delays to prevent overloading the server.

Key Parameters:
- batches: The number of concurrent requests to handle in each batch. You can increase the batch size for a faster
  process but it may overload system resources such as RAM because it will open multiple browser instances in Chrome.

- delay: The delay (in seconds) between each batch to control the request rate. Increase the delay to provide more
  interval between each request and avoid overloading the server.

- headless: Boolean flag to determine whether the browser should run in headless mode (without GUI).

Execution Timing:
The script measures and prints the total execution time for the entire scraping process to provide insights
into its efficiency and performance.

Usage:
To run the script, simply execute it as a standalone Python program.
"""

from concurrency import isbn_automation, book_info_automation
import asyncio
import time

async def main():
    # Configuration for the scraping tasks
    batches = 10  # Number of requests to process concurrently in a batch.
    delay = 2  # Delay between each batch of requests.
    headless = True  # Run the browser in headless mode (without GUI).

    print("Initiating ISBN automation and getting dynamic URLs\n")
    await asyncio.sleep(2)  # Brief pause for the user before starting the process

    # Perform the ISBN search automation to get dynamic URLs:
    await isbn_automation(batches, delay, headless)
    # The script first automates the retrieval of dynamic URLs by searching for each ISBN provided. Once this process is complete and all URLs are gathered, it proceeds to scrape detailed content from the retrieved book URLs.

    print("Finished processing dynamic URLs via ISBN search automation. Now initiating the scraping of book info.\n")
    await asyncio.sleep(2)  # Another brief pause before starting the next process

    # Perform the book info scraping automation
    await book_info_automation(batches, delay, headless)

if __name__ == "__main__":
    start_time = time.time()  # Record the start time of the execution

    # Run the main asynchronous function
    asyncio.run(main())

    end_time = time.time()  # Record the end time of the execution
    execution_time = round(end_time - start_time, 2)  # Calculate the total execution time

    # Print the total time taken for the scraping process
    print(f"Took {execution_time} seconds | {round(execution_time / 60, 2)} minutes.")

