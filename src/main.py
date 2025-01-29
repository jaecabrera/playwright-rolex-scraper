import asyncio
import json
from playwright.async_api import async_playwright, Playwright
import pandas as pd
from util import Pipe, insert_datetime
from logger.log import scrape_logger


# Change save path accordingly.
SAVE_PATH = f'rolex-{insert_datetime()}.csv'


class NextButtonException(Exception):
    """Exception for no next navigation found in page."""
    pass


async def run(playwright: Playwright):
    """"
    Run Scraper for the Page Chrono24.com
    """

    # Empty Dataframe to store output data.
    empty_df = pd.DataFrame(columns=['date', 'name', 'price', 'url'])

    try:
        # Launch Browser
        firefox = playwright.firefox
        browser = await firefox.launch()

        # Create new awaited page and go to Website.
        page = await browser.new_page()
        await page.goto("https://www.chrono24.com/rolex/index.htm?man=rolex&showpage=")

        # Locate paging element from the website and get the link for the next page.
        # link_locator = page.locator("a.paging-next")
        link_locator = page.get_by_role("link", name="Next", exact=True).first
        next_page_link = await link_locator.get_attribute('href')

        # Page counter variable for logging
        page_counter = 1

        # Pagination
        while next_page_link:
            try:

                # Product Scraper: Get JSON data inside the <script>.
                script_content = await page\
                    .locator('script[type = "application/ld+json"]')\
                    .text_content()

                # If script is found in the page.
                if script_content:

                    # Parse the JSON content
                    data = json.loads(script_content)

                    # Start cleaning data with our own utility script.
                    p = Pipe(data)
                    dataframe = p.run()
                    empty_df = pd.concat([empty_df, dataframe], axis=0)

                else:

                    print("No JSON-LD content found")

                # Pagination Block
                await page.goto(next_page_link)
                scrape_logger.debug(msg=f'Item data in {page_counter} added to dataframe.')
                page_counter += 1

                # Go to next page.
                next_page_link = await link_locator.get_attribute('href')

            except Exception as e:
                print(f'Error: {e}')
                break

    except NextButtonException as e:
        print(e)

    finally:
        await browser.close()

    empty_df.to_csv(SAVE_PATH)
    scrape_logger.debug(msg=f'Scrape session success.')


async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
