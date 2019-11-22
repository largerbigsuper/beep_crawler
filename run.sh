#!/bin/bash
export PYENV_ROOT="/root/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

cd /root/beep_crawler

# pyenv 不能在shell中激活【问题】
pyenv activate beep_crawler && scrapy crawl bishijie  -s JOBDIR=jobs/bishijie-1
pyenv activate beep_crawler && scrapy crawl jinse  -s JOBDIR=jobs/jinse-1
pyenv activate beep_crawler && scrapy crawl odaily  -s JOBDIR=jobs/odaily-1
# pyenv activate beep_crawler && scrapy crawl shenliancaijing  -s JOBDIR=jobs/shenliancaijing-1
pyenv activate beep_crawler && scrapy crawl chainnews  -s JOBDIR=jobs/chainnews-1

# 币世界
