# -*- coding:utf-8 -*-

import scrapy
from scrapy.http import Request, FormRequest


class GzSpider(scrapy.Spider):
    name = "gz"
    start_urls = [
        'https://hr.travelsky.net/hr/xinzi_guanli/',
        # /gongzi_chaxun.jsp?batch=******&staff_serial=****',
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/57.0"
    }

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    # 生成cookie
    def start_requests(self):
        return [Request("https://hr.travelsky.net/hr/",  # 登录页面
                        meta={'cookiejar': 1}, callback=self.post_login)]  # 向回调函数post_login传递cookie标识

    def post_login(self, response):
        print 'Preparing login'
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数，如果url跟Request页面的一样就省略掉
        return [FormRequest.from_response(response,
                                          url='https://hr.travelsky.net/hr/',
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.headers,  # 注意此处的headers
                                          formdata={
                                              "act": "login",
                                              "staff_num": "",  # 工号
                                              "pass": "",  # 密码
                                          },
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]

    # after_login方法将 start_urls中的网址依次迭代递交请求，带着cookie
    def after_login(self, response):
        print 'after_login'
        print response.url
        for url in self.start_urls:
            yield FormRequest(url,
                              meta={'cookiejar': response.meta['cookiejar']},
                              headers=self.headers,
                              callback=self.parse_gzym,
                              )
            # Request(url, meta={'cookiejar': response.meta['cookiejar']})

    # def parse(self, response):
        # We want to inspect one specific response.
        # 用shell调试
        # if "xinzi_guanli" in response.url:
        #    from scrapy.shell import inspect_response
        #    inspect_response(response, self)

        # 调试页面下载
        # page = response.url.split("/")[-2]
        # filename = 'gz_login_gzym-%s.html' % page
        # with open(filename, 'wb') as f:
        #    f.write(response.body)

    def parse_gzym(self, response):
        # follow links to gzym pages
        # /hr/xinzi_guanli/.*[^"]
        # /hr/xinzi_guanli/temp.*[^")]
        for href in response.css('a::attr(href)').re(r'/hr/xinzi_guanli/gongzi_chaxun.*[^")]'):
            yield response.follow(href, callback=self.parse_old, meta={'cookiejar': response.meta['cookiejar']})
        for href in response.css('a::attr(href)').re(r'/hr/xinzi_guanli/temp.*[^")]'):
            yield response.follow(href, callback=self.parse, meta={'cookiejar': response.meta['cookiejar']})

    def parse_old(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()
        yield {
            '日期': response.xpath('body/div/div/table[1]/tr/td/font/text()').re('\d+.\d+.\d+ - \d+.\d+.\d+'),
            '应发工资合计': response.xpath('body/div/div/table[4]/tr/td/b/font/text()').re('\d+.\d+'),
            '扣款合计': response.xpath('body/div/div/table[6]/tr/td/b/font/text()').re('\d+.\d+'),
            '实发工资合计': response.xpath('body/div/div/table[7]/tr/td/b/font/text()').re('\d+.\d+'),
            '工资税额': extract_with_xpath('body/div/div/table[5]/tr[6]/td[2]/font/font/text()'),
            '基本工资':   extract_with_xpath('body/div/div/table[3]/tr[1]/td[2]/font/text()'),
            '绩效工资':   extract_with_xpath('body/div/div/table[3]/tr[2]/td[2]/font/font/text()'),
            '半年奖':       extract_with_xpath('body/div/div/table[3]/tr[3]/td[2]/font/font/text()'),
            '年终奖':       extract_with_xpath('body/div/div/table[3]/tr[4]/td[2]/font/font/text()'),
            '补工资':       extract_with_xpath('body/div/div/table[3]/tr[5]/td[2]/font/font/text()'),
            '驻外补贴':     extract_with_xpath('body/div/div/table[3]/tr[1]/td[4]/font/text()'),
            '法定节假日补贴': extract_with_xpath('body/div/div/table[3]/tr[2]/td[4]/font/font/text()'),
            '延时工作补贴':   extract_with_xpath('body/div/div/table[3]/tr[3]/td[4]/font/font/text()'),
            '夜班补贴':     extract_with_xpath('body/div/div/table[3]/tr[4]/td[4]/font/font/text()'),
            '住房补贴':     extract_with_xpath('body/div/div/table[3]/tr[5]/td[4]/font/text()'),
            '稿费':         extract_with_xpath('body/div/div/table[3]/tr[5]/td[4]/font/text()'),
            '其它发放一（骨干津贴）':   extract_with_xpath('body/div/div/table[3]/tr[1]/td[6]/font/text()'),
            '其它发放二（地下津贴）':   extract_with_xpath('body/div/div/table[3]/tr[2]/td[6]/font/font/text()'),
            '其它发放三（导师津贴）':   extract_with_xpath('body/div/div/table[3]/tr[3]/td[6]/font/font/text()'),
            '其它发放四（科技创新津贴）':   extract_with_xpath('body/div/div/table[3]/tr[4]/td[6]/font/font/text()'),
            '其它发放五':   extract_with_xpath('body/div/div/table[3]/tr[5]/td[6]/font/font/text()'),
            '其它发放六':   extract_with_xpath('body/div/div/table[3]/tr[6]/td[6]/font/font/text()'),
            '其它发放七':   extract_with_xpath('body/div/div/table[3]/tr[7]/td[6]/font/font/text()'),
            '其它发放八':   extract_with_xpath('body/div/div/table[3]/tr[8]/td[6]/font/font/text()'),
            '养老保险个人缴费': extract_with_xpath('body/div/div/table[5]/tr[1]/td[2]/font/text()'),
            '医疗保险个人缴费': extract_with_xpath('body/div/div/table[5]/tr[2]/td[2]/font/font/text()'),
            '失业保险个人缴费': extract_with_xpath('body/div/div/table[5]/tr[3]/td[2]/font/font/text()'),
            '住房公积金个人缴费': extract_with_xpath('body/div/div/table[5]/tr[4]/td[2]/font/font/text()'),
            '企业年金个人缴费': extract_with_xpath('body/div/div/table[5]/tr[5]/td[2]/font/font/text()'),
            '补缴养老保险个人': extract_with_xpath('body/div/div/table[5]/tr[1]/td[4]/font/text()'),
            '补缴医疗保险个人': extract_with_xpath('body/div/div/table[5]/tr[2]/td[4]/font/font/text()'),
            '补缴失业保险个人': extract_with_xpath('body/div/div/table[5]/tr[3]/td[4]/font/font/text()'),
            '补缴公积金个人': extract_with_xpath('body/div/div/table[5]/tr[4]/td[4]/font/font/text()'),
            '补缴企业年金个人':   extract_with_xpath('body/div/div/table[5]/tr[5]/td[4]/font/font/text()'),
            '其它扣款一': extract_with_xpath('body/div/div/table[5]/tr[1]/td[6]/font/text()'),
            '其它扣款二': extract_with_xpath('body/div/div/table[5]/tr[2]/td[6]/font/text()'),
            '养老保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[1]/td[2]/font/text()'),
            '医疗保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[2]/td[2]/font/font/text()'),
            '失业保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[3]/td[2]/font/font/text()'),
            '工伤保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[4]/td[2]/font/font/text()'),
            '生育保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[5]/td[2]/font/font/text()'),
            '住房公积金公司缴费': extract_with_xpath('body/div/div/table[8]/tr[6]/td[2]/font/font/text()'),
            '企业年金公司缴费': extract_with_xpath('body/div/div/table[8]/tr[7]/td[2]/font/font/text()'),
            '补缴养老保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[1]/td[4]/font/text()'),
            '补缴医疗保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[2]/td[4]/font/font/text()'),
            '补缴失业保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[3]/td[4]/font/font/text()'),
            '补缴工伤保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[4]/td[4]/font/font/text()'),
            '补缴生育保险公司缴费': extract_with_xpath('body/div/div/table[8]/tr[5]/td[4]/font/font/text()'),
            '补缴公积金公司缴费': extract_with_xpath('body/div/div/table[8]/tr[6]/td[4]/font/font/text()'),
            '企业年金公司补缴': extract_with_xpath('body/div/div/table[8]/tr[7]/td[4]/font/font/text()'),
            '公司缴费合计': response.xpath('body/div/div/table[9]/tr/td/b/font/text()').re('\d+.\d+'),
        }

    def parse(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()
        yield {
            '日期':              response.xpath('body/div/table/tr[1]/td/text()').re('\d+.\d+.\d+'),
            '应发工资合计':     extract_with_xpath('body/div/table/tr[46]/td[2]/text()'),
            '扣款合计':         extract_with_xpath('body/div/table/tr[47]/td[2]/text()'),
            '实发工资合计':     extract_with_xpath('body/div/table/tr[48]/td[2]/text()'),
            '工资税额':         extract_with_xpath('body/div/table/tr[26]/td[2]/text()'),
            '基本工资':           extract_with_xpath('body/div/table/tr[4]/td[2]/text()'),
            '绩效工资':           extract_with_xpath('body/div/table/tr[5]/td[2]/text()'),
            '半年奖':               extract_with_xpath('body/div/table/tr[6]/td[2]/text()'),
            '年终奖':               extract_with_xpath('body/div/table/tr[7]/td[2]/text()'),
            '补工资':               extract_with_xpath('body/div/table/tr[8]/td[2]/text()'),
            '驻外补贴':             extract_with_xpath('body/div/table/tr[9]/td[2]/text()'),
            '法定节假日补贴':       extract_with_xpath('body/div/table/tr[10]/td[2]/text()'),
            '延时工作补贴':         extract_with_xpath('body/div/table/tr[11]/td[2]/text()'),
            '夜班补贴':             extract_with_xpath('body/div/table/tr[12]/td[2]/text()'),
            '其它发放一（骨干津贴）': extract_with_xpath('body/div/table/tr[13]/td[2]/text()'),
            '其它发放二（地下津贴）': extract_with_xpath('body/div/table/tr[14]/td[2]/text()'),
            '其它发放三（导师津贴）': extract_with_xpath('body/div/table/tr[15]/td[2]/text()'),
            '其它发放四（科技创新津贴）': extract_with_xpath('body/div/table/tr[16]/td[2]/text()'),
            '其它发放五':           extract_with_xpath('body/div/table/tr[17]/td[2]/text()'),
            '其它发放六':           extract_with_xpath('body/div/table/tr[18]/td[2]/text()'),
            '其它发放七':           extract_with_xpath('body/div/table/tr[19]/td[2]/text()'),
            '其它发放八':           extract_with_xpath('body/div/table/tr[20]/td[2]/text()'),
            '养老保险个人缴费':     extract_with_xpath('body/div/table/tr[21]/td[2]/text()'),
            '医疗保险个人缴费':     extract_with_xpath('body/div/table/tr[22]/td[2]/text()'),
            '失业保险个人缴费':     extract_with_xpath('body/div/table/tr[23]/td[2]/text()'),
            '住房公积金个人缴费':   extract_with_xpath('body/div/table/tr[24]/td[2]/text()'),
            '企业年金个人缴费':     extract_with_xpath('body/div/table/tr[25]/td[2]/text()'),
            '补缴养老保险个人':     extract_with_xpath('body/div/table/tr[27]/td[2]/text()'),
            '补缴医疗保险个人':     extract_with_xpath('body/div/table/tr[28]/td[2]/text()'),
            '补缴失业保险个人':     extract_with_xpath('body/div/table/tr[29]/td[2]/text()'),
            '补缴公积金个人':       extract_with_xpath('body/div/table/tr[30]/td[2]/text()'),
            '补缴企业年金个人':     extract_with_xpath('body/div/table/tr[31]/td[2]/text()'),
            '养老保险公司缴费':     extract_with_xpath('body/div/table/tr[32]/td[2]/text()'),
            '医疗保险公司缴费':     extract_with_xpath('body/div/table/tr[33]/td[2]/text()'),
            '失业保险公司缴费':     extract_with_xpath('body/div/table/tr[34]/td[2]/text()'),
            '工伤保险公司缴费':     extract_with_xpath('body/div/table/tr[35]/td[2]/text()'),
            '生育保险公司缴费':     extract_with_xpath('body/div/table/tr[36]/td[2]/text()'),
            '住房公积金公司缴费':   extract_with_xpath('body/div/table/tr[37]/td[2]/text()'),
            '企业年金公司缴费':     extract_with_xpath('body/div/table/tr[38]/td[2]/text()'),
            '补缴养老保险公司缴费': extract_with_xpath('body/div/table/tr[39]/td[2]/text()'),
            '补缴医疗保险公司缴费': extract_with_xpath('body/div/table/tr[40]/td[2]/text()'),
            '补缴生育保险公司缴费': extract_with_xpath('body/div/table/tr[41]/td[2]/text()'),
            '补缴失业保险公司缴费': extract_with_xpath('body/div/table/tr[42]/td[2]/text()'),
            '补缴工伤保险公司缴费': extract_with_xpath('body/div/table/tr[43]/td[2]/text()'),
            '补缴公积金公司缴费':   extract_with_xpath('body/div/table/tr[44]/td[2]/text()'),
            '企业年金公司补缴':     extract_with_xpath('body/div/table/tr[45]/td[2]/text()'), }