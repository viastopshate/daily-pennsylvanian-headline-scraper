# Webscraper

## Scraping the News Headline

    # Step 1: Get the URL of the News section
    home_page_url = "https://www.thedp.com"
    req = requests.get(home_page_url)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    news_section_url = ""
    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        # Assuming the structure to find the news section URL (adjust as necessary)
        news_link = soup.find('div', class_='col-sm-10').find('div', class_='section-list').find('div', class_='col-sm-3').find('a')
        if news_link and news_link.has_attr('href'):
            news_section_url = news_link['href']
            loguru.logger.info(f"News section URL: {news_section_url}")
        else:
            return "News section URL not found."

    # Step 2: Scrape the first title from the News section
    if news_section_url:
        req_news = requests.get(news_section_url)
        loguru.logger.info(f"News section request URL: {req_news.url}")
        loguru.logger.info(f"News section request status code: {req_news.status_code}")
        
        if news_section_url:
            req_news = requests.get(news_section_url)
            loguru.logger.info(f"News section request URL: {req_news.url}")
            loguru.logger.info(f"News section request status code: {req_news.status_code}")

        if req_news.ok:
            soup_news = bs4.BeautifulSoup(req_news.text, "html.parser")
            # Directly access the title using the known structure
            title_h3 = soup_news.select_one('div.row.section-article div.col-md-8 h3.standard-link')
            if title_h3:
                data_point = title_h3.text.strip()
                loguru.logger.info(f"Data point: {data_point}")
                return data_point
            else:
                return "Article title not found."
        else:
            return "Failed to retrieve the News section."
    else:
        return "Failed to determine the News section URL."

Explanation: 
The scraper is designed to fetch the first headline from the "News" section of The Daily Pennsylvanian's website. Initially, it accesses the homepage to locate and extract the URL specific to the "News" section, utilizing the structure of HTML elements to navigate through the site's layout. Upon identifying this URL, the scraper then proceeds to request the "News" section page, where it directly targets and extracts the text of the leading headline based on its placement within the HTML structure. This process emphasizes efficient navigation through the website's architecture to pinpoint and retrieve the desired content, showcasing the scraper's capability to adapt and extract specific information by understanding and leveraging the underlying structure of the web page.

## Scraping the Sports Headline

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

Explanation: 

n transitioning from scraping the "News" section to the "Sports" section, the primary alteration involved adjusting the scraper to target the second div with the class col-sm-3 under the section-list div on The Daily Pennsylvanian's homepage, instead of the first. This modification was crucial for pinpointing the URL specific to the "Sports" section accurately. After successfully obtaining this URL, the process of extracting the first headline from the "Sports" section remained consistent with the previous approach, employing a precise navigation through the HTML structure to locate and retrieve the headline text. This change demonstrates the scraper's flexibility in adapting to different sections of the website by simply shifting the focus within the same overarching HTML framework.