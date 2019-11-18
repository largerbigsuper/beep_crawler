#!/bin/bash

cd /root/beep_crawler 

# pyenv 不能在shell中激活【问题】
# pyenv activate beep_crawler && 

scrapy crawl bishijie  -s JOBDIR=jobs/bishijie-1
scrapy crawl jinse  -s JOBDIR=jobs/jinse-1

# 币世界



