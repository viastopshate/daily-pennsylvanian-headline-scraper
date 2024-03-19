# Scraping the News Headline

Code: 
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
