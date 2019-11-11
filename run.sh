#!/bin/bash

cd /root/beep_crawler

pyenv activate beep_crawler

# 币世界

scrapy crawl bishijie  -s JOBDIR=jobs/bishijie-1

