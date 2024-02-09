#!/bin/sh
cd ..
docker rmi rss_crawler:slim
docker build . -t rss_crawler:slim
docker save rss_crawler:slim -o rss_crawler_slim.tar