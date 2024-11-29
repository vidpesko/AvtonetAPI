#!/bin/bash

# Run spider
cd /Users/vidpesko/Documents/Learning/Projects/AvtonetAPI/src/Scraper/Scraper
if [ -z "$2" ]; then
    scrapy crawl $1
else
    scrapy crawl $1 -a $2 --nolog
fi