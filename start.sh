#!/bin/sh
docker run --rm -d --name rss_crawler -v ./sqlite3.sql:/code/sqlite3.sql -v ./log:/code/log rss_crawler:slim
