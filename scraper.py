'''
A BS scraper for Engineering Management Journal on https://www.tandfonline.com
'''
from bs4 import BeautifulSoup
from datetime import date, datetime

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
    'Proceedings Reviews',
    '2016 Reviewer Thank You',
    '2014 Engineering Management Dissertation Review',
    'Acknowledgement',
    'Editorial Board EOV',
    'Editor’s Introduction for the March 2022 Issue',
    'From the Special Issue Editors',
    'From the Editors and Special Issue Editors',
    'Reviewer Thank You']

# loop over the range for the volume ID
for volume in range(first_volume, last_volume + 1):

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
        log.warning(f"\tFound {len(articles)} articles...")
        article_counter = 0

        # get all the article publish dates
        tocEPubDate = soup.find_all('div', {'class': 'tocEPubDate'})
        log.warning(f"\tFound {len(tocEPubDate)} tocEPubDates...")

        # get the href and text of each article div
        for i, article in enumerate(articles[0:len(tocEPubDate)]):
            links = article.findChildren("a", href=True)

            # clean up the article date
            date_soup = BeautifulSoup(str(tocEPubDate[i]), features="html.parser")
            date_span = date_soup.find("span", {"class": "date"})
            article_date = datetime.strptime(date_span.text.strip(), '%d %b %Y').date()

            for link in links:
                article_title = link.text
                article_url = f"https://www.tandfonline.com{link['href']}"
                article_counter = article_counter + 1

                log.warning(f"\t{article_counter}: {article_title}")

            # skip any article titles that are uninteresting
            if article_title in skip:
                log.warning(f"\tSkipping {article_title}")
                continue

            # skip any article that is already in the list
            if next((existing for existing in article_list if existing['url'] == article_url), None):
                log.warning(f"\tSkipping {article_title}")
                continue

            article_list.extend(
                [{'url': article_url,
                'title': article_title,
                'date': article_date,
                'issue_url': issue_url,
                'issue_title': issue_title
            }])

# open text file in read mode
environment = jinja2.Environment()
template = environment.from_string(open("index.j2", "r").read())
rendered_template = template.render(article_list=article_list,
    title="EMJ Articles", date=date.today().strftime('%A, %B  %d, %Y'))

print(rendered_template)
