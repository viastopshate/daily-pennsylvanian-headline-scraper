"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_data_point():
    """
    Scrapes the main headline from The Daily Pennsylvanian home page.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    # Step 1: Get the URL of the News section
    home_page_url = "https://www.thedp.com"
    req = requests.get(home_page_url)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    sports_section_url = ""
    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        # Find all 'div' elements with class 'col-sm-3' under the 'div' with class 'section-list'
        # and select the second one for the Sports section
        col_sm_3_divs = soup.find('div', class_='section-list').find_all('div', class_='col-sm-3')
        if len(col_sm_3_divs) > 1:  # Ensure there are at least two such divs
            sports_link = col_sm_3_divs[1].find('a')  # Select the second 'div' for Sports
            if sports_link and sports_link.has_attr('href'):
                sports_section_url = sports_link['href']
                loguru.logger.info(f"Sports section URL: {sports_section_url}")
            else:
                return "Sports section URL not found."
        else:
            return "Insufficient 'col-sm-3' divs found."

    # Step 2: Scrape the first title from the Sports section
    if sports_section_url:
        req_sports = requests.get(sports_section_url)
        loguru.logger.info(f"Sports section request URL: {req_sports.url}")
        loguru.logger.info(f"Sports section request status code: {req_sports.status_code}")

        if req_sports.ok:
            soup_sports = bs4.BeautifulSoup(req_sports.text, "html.parser")
            # The structure to find the title remains the same as described for the News section
            title_h3 = soup_sports.select_one('div.row.section-article div.col-md-8 h3.standard-link')
            if title_h3:
                data_point = title_h3.text.strip()
                loguru.logger.info(f"Data point: {data_point}")
                return data_point
            else:
                return "Article title not found."
        else:
            return "Failed to retrieve the Sports section."
    else:
        return "Failed to determine the Sports section URL."


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
