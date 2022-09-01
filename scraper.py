'''
A BS scraper for Engineering Management Journal on https://www.tandfonline.com
'''
from bs4 import BeautifulSoup
from datetime import date
import lxml.html

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
        tree = lxml.html.fromstring(response.content)
        issue_titles = tree.xpath('//div[@title="toc-title"]/text()')
        log.warning(issue_titles)

        continue

        # Get the title of the issue (only one is needed)
        issue_titles = soup.find_all("div", {"class": "toc-title"})
        issue_title = issue_titles[0].get_text()

        # get all the articles in the issue
        articles = soup.find_all('div', {'class': 'tocArticleEntry'})
        log.warning(f"Found {len(articles)} articles...")
        article_counter = 0
        article_list.extend(articles)

# open text file in read mode
#environment = jinja2.Environment()
#template = environment.from_string(open("index.j2", "r").read())
#rendered_template = template.render(articles=articles,
#    title="EMJ", date=date.today().strftime('%A, %B  %d, %Y at %X %Z'))

#print(rendered_template)
