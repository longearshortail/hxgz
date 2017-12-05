# -*- coding: utf-8 -*-

# Scrapy settings for hxgz project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'hxgz'

SPIDER_MODULES = ['hxgz.spiders']
NEWSPIDER_MODULE = 'hxgz.spiders'

FEED_EXPORTERS = {
    'csv': 'hxgz.spiders.csv_item_exporter.MyProjectCsvItemExporter',
}  # hxgz为工程名

FIELDS_TO_EXPORT = [
    '日期',
    '应发工资合计',
    '扣款合计',
    '实发工资合计',
    '工资税额',
    '基本工资',
    '绩效工资',
    '半年奖',
    '年终奖',
    '补工资',
    '驻外补贴',
    '法定节假日补贴',
    '延时工作补贴',
    '夜班补贴',
    '其它发放一（骨干津贴）',
    '其它发放二（地下津贴）',
    '其它发放三（导师津贴）',
    '其它发放四（科技创新津贴）',
    '其它发放五',
    '其它发放六',
    '其它发放七',
    '其它发放八',
    '养老保险个人缴费',
    '医疗保险个人缴费',
    '失业保险个人缴费',
    '住房公积金个人缴费',
    '企业年金个人缴费',
    '补缴养老保险个人',
    '补缴医疗保险个人',
    '补缴失业保险个人',
    '补缴公积金个人',
    '补缴企业年金个人',
    '养老保险公司缴费',
    '医疗保险公司缴费',
    '失业保险公司缴费',
    '工伤保险公司缴费',
    '生育保险公司缴费',
    '住房公积金公司缴费',
    '企业年金公司缴费',
    '补缴养老保险公司缴费',
    '补缴医疗保险公司缴费',
    '补缴生育保险公司缴费',
    '补缴失业保险公司缴费',
    '补缴工伤保险公司缴费',
    '补缴公积金公司缴费',
    '企业年金公司补缴',
    '其它扣款一',
    '其它扣款二',
    '公司缴费合计'
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hxgz (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'hxgz.middlewares.HxgzSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'hxgz.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'hxgz.pipelines.HxgzPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
