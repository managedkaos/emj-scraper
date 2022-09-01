'''
A BS scraper for Engineering Management Journal on https://www.tandfonline.com
'''
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Variables for the first and last volume to consider
first_volume = 1
last_volume = 34

# A list of TOC entries that are not interesting
skip = [
    'Editorial Board',
    'From the Editor',
    'Announcements',
    'Book Review',
    'Book Reviews',
    'Proceedings Review'
    'Instructions for Authors',
    'Dissertation Review',
    'Dissertation Reviews',
    'Special Thanks',
    'Proceedings Review',
    'Proceedings Reviews']

# A dataframe to hold the results
df = pd.DataFrame(columns=['Article', 'Issue'])

# loop over the range for the volume ID
for volume in range(first_volume, last_volume+1):

    # loop over each issue in each volume (at most, there are four issues)
    for issue in range(1, 5):
        print(f"Processing: Volume {volume}, Issue {issue}")

        # create a URL for the volume and issue
        url = f"https://www.tandfonline.com/toc/uemj20/{volume}/{issue}"

        # get the content for the issue URL
        response = requests.get(url)

        # skip any URLs that don't come back with a `200`
        if response.status_code != 200:
            continue

        # get the HTML text from the response
        html = response.text

        # parse the HTML into soup
        soup = BeautifulSoup(html, features="html.parser")

        # Get the title of the issue (only one is needed)
        issue_titles = soup.find_all("div", {"class": "toc-title"})
        issue_title = issue_titles[0].get_text()

        # get all the articles in the issue
        articles = soup.find_all('div', {'class': 'art_title'})

        # get the href and text of each article div
        for article in articles:
            links = article.findChildren("a", href=True)
            for link in links:
                article_title = link.text
                article_url = f"https://www.tandfonline.com{link['href']}"

            # skip any article titles that are uninteresting
            if article_title in skip:
                continue

            df.loc[len(df)] = [f"[{article_title}]({article_url})", issue_title]

print(df.to_markdown())