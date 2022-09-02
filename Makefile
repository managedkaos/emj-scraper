scraper:
	python ./scraper.py > ./public/index.html

all: requirements lint scraper

requirements:
	pip install -U pip
	pip install --requirement requirements.txt

lint:
	flake8 --ignore=E124,E128,E501

open:
	open ./public/index.html

.PHONY: scraper all requirements lint open
