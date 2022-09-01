all: scraper

scraper:
	python ./scraper.py

requirements:
	pip install -U pip
	pip install --requirement requirements.txt

.PHONY: all scraper pages requirements
