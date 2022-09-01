'''
A BS scraper for Engineering Management Journal on https://www.tandfonline.com
'''
from bs4 import BeautifulSoup
from datetime import date

import pandas as pd
import requests
import logging
import jinja2


# configure logging
logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

# Variables for the first and last volume to consider
first_volume = 34
last_volume = 34

article_list = []

# A list of TOC entries that are not interesting
skip = [
    'Editorial Board',
    'From the Editor',
    'From the Editors',
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
        log.warning(f"Processing: Volume {volume}, Issue {issue}")

        # create a URL for the volume and issue
        issue_url = f"https://www.tandfonline.com/toc/uemj20/{volume}/{issue}"

        # get the content for the issue URL
        response = requests.get(issue_url)

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
        log.warning(f"Found {len(articles)} articles...")
        article_counter = 0

        # get the href and text of each article div
        for article in articles:
            links = article.findChildren("a", href=True)

            for link in links:
                article_title = link.text
                article_url = f"https://www.tandfonline.com{link['href']}"
                article_counter = article_counter + 1
                log.warning(f"{article_counter}: {article_title}")

            # skip any article titles that are uninteresting
            if article_title in skip:
                continue

            if next((sub for sub in article_list if sub['url'] == article_url), None):
                log.warning(f"Skipping {article_title}")
                continue

            article_list.extend(
                [{'url': article_url,
                'title': article_title,
                'issue_url': issue_url,
                'issue_title': issue_title
            }])

            # Add the article title and URL to the dataframe
            df.loc[len(df)] = [
                f"<a href='{article_url}' target='_blank'>{article_title}</a>",
                f"<a href='{issue_url}' target='_blank'>{issue_title}</a>"]

# print the dataframe as HTML
# print(df.to_html(escape=False))

# open text file in read mode
environment = jinja2.Environment()
template = environment.from_string(open("index.j2", "r").read())
rendered_template = template.render(article_list=article_list,
    title="EMJ", date=date.today().strftime('%A, %B  %d, %Y at %X %Z'))

print(rendered_template)
