scraper:
	python ./scraper.py > ./public/index.html

all: requirements lint scraper

requirements:
	pip install -U pip
	pip install --requirement requirements.txt

lint:
	echo 'Linting coming soon! :D'

open:
	open ./public/index.html

.PHONY: scraper all requirements lint open
