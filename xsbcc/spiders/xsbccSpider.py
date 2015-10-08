# -*- coding: utf-8 -*-
import re
import scrapy
from xsbcc.items import XsbccItem, CompanyProfile, EquityStatus, SeniorExecutive, HistoricalEvolution, FinancialIndex


class XsbccSpider(scrapy.Spider):
    name = "xsbcc"
    allowed_domains = ["www.xsbcc.com"]
    start_urls = ['http://www.xsbcc.com/common/company.htm?' \
                  'ru=&uid=&hy=&addr=&quan=&tm1=&tm2=&se=&tp=0&tz=&gao=' \
                  '&phoneemail=13621241872&od=txtno%20desc&pn='+str(i+1) for i in range(180)]

    def parse(self, response):
        domain = 'http://www.xsbcc.com'
        xsb = XsbccItem()
        divs = response.xpath('//tr')
        time = response.headers['Date']
        for div in divs:
            items = div.xpath('./td/text()').extract()
            # 序号
            xsb['time'] = time
            xsb['serial_number'] = items[0]
            # 证券代码
            xsb['securities_code'] = div.xpath('./td/a/text()').extract()
            # 证券简称
            xsb['securities_abbr'] = items[1]
            # 转让方式
            xsb['transfer_mode'] = items[2]
            # 前收盘价（元/股）
            xsb['previous_price'] = items[3]
            # 最近成交价（元/股）
            xsb['recent_price'] = items[4]
            # 成交金额(万元)
            xsb['turnover_million'] = items[5]
            # 成交量(万股)
            xsb['volume_million'] = items[6]
            # 涨跌
            xsb['amount_change'] = items[7]
            # 涨跌幅
            xsb['rate_change'] = items[8]
            # 市盈率
            xsb['PE_ratio'] = items[9]
            # 挂牌时间
            xsb['listing_time'] = items[10]
            # 行业
            xsb['industry'] = items[11]
            # 地区
            xsb['area'] = items[12]
            # 券商
            xsb['broker'] = items[13]
            # 看路演人数
            xsb['numbersOfPer'] = items[14]
            yield xsb

        for url in response.xpath('//tr/td/a/@href').extract():
            code = re.compile('\d+').findall(url)[0]
            yield scrapy.Request(domain+url, \
                                 callback=self.parse_companyProfile, meta={'securities_code': code})
            yield scrapy.Request(domain+url.replace('/company/', '/company/gg'), \
                                 callback=self.parse_seniorExecutive, meta={'securities_code': code})
            yield scrapy.Request(domain+url.replace('/company/', '/company/ls'), \
                                 callback=self.parse_historicalEvolution, meta={'securities_code': code})
            yield scrapy.Request(domain+url.replace('/company/', '/company/gb'), \
                                 callback=self.parse_equityStatus, meta={'securities_code': code})
            yield scrapy.Request(domain+url.replace('/company/', '/company/cw'), \
                                 callback=self.parse_financialIndex, meta={'securities_code': code})

    def parse_companyProfile(self, response):
        compro = CompanyProfile()
        div = response.xpath('//div[@class="rcon"]')
        compro['url'] = response.url
        compro['time'] = response.headers['Date']
        # 证券代码
        compro['securities_code'] = response.meta['securities_code']
        # 公司全称
        compro['company_name'] = div.re(u'(?<=<strong>公司全称：</strong>).*?(?=<br>)')
        # 英文名称
        compro['english_name'] = div.re(u'(?<=<strong>英文名称：</strong>).*?(?=<br>)')
        # 注册地址
        compro['registered_address'] = div.re(u'(?<=<strong>注册地址：</strong>).*?(?=<br>)')
        # 法人代表
        compro['legal_representative'] = div.re(u'(?<=<strong>法人代表：</strong>).*?(?=<br>)')
        # 公司董秘
        compro['company_secretaries'] = div.re(u'(?<=<strong>公司董秘：</strong>).*?(?=<br>)')
        # 注册资本(万元)
        compro['registered_capital'] = div.re(u'(?<=<strong>注册资本(万元)：</strong>).*?(?=<br>)')
        # 行业分类
        compro['industry_classification'] = div.re(u'(?<=<strong>行业分类：</strong>).*?(?=<br>)')
        # 挂牌日期
        compro['listing_date'] = div.re(u'(?<=<strong>挂牌日期：</strong>).*?(?=<br>)')
        # 公司网址
        compro['company_website'] = div.re(u'(?<=<strong>公司网址：</strong>).*?(?=<br>)')
        # 转让方式
        compro['transfer_mode'] = div.re(u'(?<=<strong>转让方式：</strong>).*?(?=<br>)')
        # 主办券商
        compro['sponsor_broker'] = div.re(u'(?<=<strong>主办券商：</strong>).*?(?=<br>)')
        return compro

    def parse_seniorExecutive(self, response):
        divs = response.xpath('//div[@class="rcon"]/table/tr')
        for div in divs:
            senior_list = div.xpath('./td').re('(?<=<td>).*?(?=</td>)')
            if u'<strong>姓名' in senior_list[0]:
                continue
            senior = SeniorExecutive()
            senior['url'] = response.url
            senior['time'] = response.headers['Date']
            senior['securities_code'] = response.meta['securities_code']
            # 姓名
            senior['name'] = senior_list[0]
            # 职务
            senior['post'] = senior_list[1]
            # 出生年份
            senior['year_birth'] = senior_list[2]
            # 性别
            senior['gender'] = senior_list[3]
            # 学历
            senior['education'] = senior_list[4]
            # 职称
            senior['title'] = senior_list[5]
            # 年薪
            senior['annual_salary'] = senior_list[6]
            # 所持股数
            senior['shares'] = senior_list[7]
            yield senior

    def parse_historicalEvolution(self, response):
        histEvo = HistoricalEvolution()
        histEvo['url'] = response.url
        histEvo['time'] = response.headers['Date']
        histEvo['securities_code'] = response.meta['securities_code']
        histEvo['info'] = response.xpath('//div[@class="rcon"]/text()').extract()
        return histEvo

    def parse_equityStatus(self, response):
        for div in response.xpath('//div[@class="rcon"]/table/tr'):
            equSta_list = div.xpath('./td/text()').extract()
            if not equSta_list:
                continue
            equSta = EquityStatus()
            equSta['url'] = response.url
            equSta['time'] = response.headers['Date']
            # 证券代码
            equSta['securities_code'] = response.meta['securities_code']
            # 日期
            equSta['date'] = equSta_list[0]
            # 总股本
            equSta['general_capital'] = equSta_list[1]
            # 可转让A股
            equSta['transferable_A_shares'] = equSta_list[2]
            # 国家股
            equSta['national_unit'] = equSta_list[3]
            # 法人股
            equSta['corporate_stock'] = equSta_list[4]
            # 内部职工股
            equSta['internal_staff_shares'] = equSta_list[5]
            # 转配股
            equSta['transfer_rights'] = equSta_list[6]
            # B股
            equSta['B_Share'] = equSta_list[7]
            # H股
            equSta['H_share'] = equSta_list[8]
            yield equSta

    def parse_financialIndex(self, response):
        for div in response.xpath('//div[@class="rcon"]/table'):
            finInd = FinancialIndex()
            finInd['url'] = response.url  
            finInd['time'] = response.headers['Date']
            # 证券代码
            finInd['securities_code'] = response.meta['securities_code']
            # 年份
            finInd['year'] = div.re(u'(?<=<table class=").*?(?=>)')
            # 基本每股收益(元)
            finInd['basic_earnings_per_share'] = div.re(u'(?<=<td>基本每股收益\(元\)</td><td>).*?(?=</td>)')
            # 净利润(万元)
            finInd['net_profit'] = div.re(u'(?<=<td>净利润\(万元\)</td><td>).*?(?=</td>)')
            # 净利润同比增长率
            finInd['net_profit_growth_rate'] = div.re(u'(?<=<td>净利润同比增长率\(%\)</td><td>).*?(?=</td>)')
            # 营业总收入(万元)
            finInd['total_revenue'] = div.re(u'(?<=<td>营业总收入\(万元\)</td><td>).*?(?=</td>)')
            # 营业总收入同比增长率
            finInd['total_revenue_growth_rate'] = div.re(u'(?<=<td>营业总收入同比增长率\(%\)</td><td>).*?(?=</td>)')
            # 每股净资产(元)
            finInd['net_assets_per_share'] = div.re(u'(?<=<td>每股净资产\(元\)</td><td>).*?(?=</td>)')
            # 净资产收益率
            finInd['ROE'] = div.re(u'(?<=<td>净资产收益率\(%\)</td><td>).*?(?=</td>)')
            # 净资产收益率-摊薄
            finInd['ROE_diluted'] = div.re(u'(?<=<td>净资产收益率-摊薄\(%\)</td><td>).*?(?=</td>)')
            # 资产负债比率
            finInd['asset_liability_ratio'] = div.re(u'(?<=<td>资产负债比率\(%\)</td><td>).*?(?=</td>)')
            # 每股资本公积金(元)
            finInd['per_share_capital_fund'] = div.re(u'(?<=<td>每股资本公积金\(元\)</td><td>).*?(?=</td>)')
            # 每股未分配利润(元)
            finInd['non_distribution_of_profit_per_share'] = div.re(u'(?<=<td>每股未分配利润\(元\)</td><td>).*?(?=</td>)')
            # 每股经营现金流(元)
            finInd['operating_cash_flow_per_share'] = div.re(u'(?<=<td>每股经营现金流\(元\)</td><td>).*?(?=</td>)')
            # 销售毛利率
            finInd['gross_margin_sales'] = div.re(u'(?<=<td>销售毛利率\(%\)</td><td>).*?(?=</td>)')
            # 存货周转率
            finInd['inventory_turnover_rate'] = div.re(u'(?<=<td>存货周转率</td><td>).*?(?=</td>)')
            yield finInd



