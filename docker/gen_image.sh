#!/bin/sh
cd ..
docker rmi rss_crawler:slim
docker build . -t rss_crawler:slim
#docker save rss_crawler:slim -o rss_crawler_slim.tar
docker run --rm -d --name rss_crawler -v ./sqlite3.sql:/code/sqlite3.sql -v ./log:/code/log rss_crawler:slim
