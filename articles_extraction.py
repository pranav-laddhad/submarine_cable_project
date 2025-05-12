
##############
# this script extracts the articles from Subtleforum website.
# it gives as output as csv file in which the title, date, tags, url or article are present


import requests  
from bs4 import BeautifulSoup  
import pandas as pd  
import time  


# Base URL for the first page
BASE_URL = "https://subtelforum.com/category/cable-faults-maintenance/"

def get_all_articles():
    page_url = BASE_URL  
    articles_data = []

    while page_url:
        print(f"Scraping: {page_url}")
        response = requests.get(page_url)

        if response.status_code != 200:
            print(f"Failed to retrieve {page_url}. Status code: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article")

        for article in articles:
            # Extract Title
            title_tag = article.find("h2", class_="entry-title")
            title = title_tag.text.strip() if title_tag else "No title"

            # Extract Date
            date_span = article.find("span", class_="updated rich-snippet-hidden")
            date = date_span.text.strip() if date_span else "No date found"

            # Extract Tags
            tags_span = article.find("span", class_="meta-tags")
            tags = [tag.text.strip() for tag in tags_span.find_all("a")] if tags_span else ["No tags"]

            # Extract URL
            link_tag = title_tag.find("a") if title_tag else None
            url = link_tag["href"] if link_tag else "No URL"

            articles_data.append({
                "Title": title,
                "Date": date,
                "Tags": ", ".join(tags),
                "URL": url
            })

        next_page_span = soup.find("span", class_="page-next")
        next_page = next_page_span.find_parent("a") if next_page_span else None
        page_url = next_page["href"] if next_page else None

        time.sleep(2) 

    return articles_data

all_articles = get_all_articles()

df = pd.DataFrame(all_articles)
df.to_csv("article_cable_faults.csv", index=False)

print(f"Scraping completed! {len(all_articles)} articles saved to 'article_cable_faults.csv'")
