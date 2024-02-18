#!/bin/sh
docker build . -t rss_crawler
docker run --name rss_crawler -v ./sqlite3.sql:/code/sqlite3.sql -v ./RssParser:/code/RssParser -v ./log:/code/log rss_crawler
