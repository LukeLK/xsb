# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XsbccItem(scrapy.Item):
    def class_name(self):
        return 'XsbccItem'
    url = scrapy.Field()
    time = scrapy.Field()
    # 序号
    serial_number = scrapy.Field()
    # 证券代码
    securities_code = scrapy.Field()
    # 证券简称
    securities_abbr = scrapy.Field()
    # 转让方式
    transfer_mode = scrapy.Field()
    # 前收盘价（元/股）
    previous_price = scrapy.Field()
    # 最近成交价（元/股）
    recent_price = scrapy.Field()
    # 成交金额(万元)
    turnover_million = scrapy.Field()
    # 成交量(万股)
    volume_million = scrapy.Field()
    # 涨跌
    amount_change = scrapy.Field()
    # 涨跌幅
    rate_change = scrapy.Field()
    # 市盈率
    PE_ratio = scrapy.Field()
    # 挂牌时间
    listing_time = scrapy.Field()
    # 行业
    industry = scrapy.Field()
    # 地区
    area = scrapy.Field()
    # 券商
    broker = scrapy.Field()
    # 看路演人数
    numbersOfPer = scrapy.Field()


# 公司概况
class CompanyProfile(scrapy.Item):
    def class_name(self):
        return 'CompanyProfile'
    url = scrapy.Field()
    time = scrapy.Field()
    # 证券代码
    securities_code = scrapy.Field()
    # 公司全称
    company_name = scrapy.Field()
    # 英文名称
    english_name = scrapy.Field()
    # 注册地址
    registered_address = scrapy.Field()
    # 法人代表
    legal_representative = scrapy.Field()
    # 公司董秘
    company_secretaries = scrapy.Field()
    # 注册资本(万元)
    registered_capital = scrapy.Field()
    # 行业分类
    industry_classification = scrapy.Field()
    # 挂牌日期
    listing_date = scrapy.Field()
    # 公司网址
    company_website = scrapy.Field()
    # 转让方式
    transfer_mode = scrapy.Field()
    # 主办券商
    sponsor_broker = scrapy.Field()


# 高管人员
class SeniorExecutive(scrapy.Item):
    def class_name(self):
        return 'SeniorExecutive'
    url = scrapy.Field()
    time = scrapy.Field()
    # 证券代码
    securities_code = scrapy.Field()
    # 姓名
    name = scrapy.Field()
    # 职务
    post = scrapy.Field()
    # 出生年份
    year_birth = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # 学历
    education = scrapy.Field()
    # 职称
    title = scrapy.Field()
    # 年薪
    annual_salary = scrapy.Field()
    # 所持股数
    shares = scrapy.Field()


# 历史沿革
class HistoricalEvolution(scrapy.Item):
    def class_name(self):
        return 'HistoricalEvolution'
    url = scrapy.Field()
    time = scrapy.Field()
    # 证券代码
    securities_code = scrapy.Field()
    info = scrapy.Field()


# 股本状况
class EquityStatus(scrapy.Item):
    def class_name(self):
        return 'EquityStatus'
    url = scrapy.Field()
    time = scrapy.Field()
    # 证券代码
    securities_code = scrapy.Field()
    # 时间
    date = scrapy.Field()
    # 总股本
    general_capital = scrapy.Field()
    # 可转让A股
    transferable_A_shares = scrapy.Field()
    # 国家股
    national_unit = scrapy.Field()
    # 法人股
    corporate_stock = scrapy.Field()
    # 内部职工股
    internal_staff_shares = scrapy.Field()
    # 转配股
    transfer_rights = scrapy.Field()
    # B股
    B_Share = scrapy.Field()
    # H股
    H_share = scrapy.Field()


# 财务指标
class FinancialIndex(scrapy.Item):
    def class_name(self):
        return 'FinancialIndex'
    url = scrapy.Field()
    time = scrapy.Field()
    # 证券代码
    securities_code = scrapy.Field()
    # 年份
    year = scrapy.Field()
    # 基本每股收益(元)
    basic_earnings_per_share = scrapy.Field()
    # 净利润(万元)
    net_profit = scrapy.Field()
    # 净利润同比增长率 = scrapy.Field()
    net_profit_growth_rate = scrapy.Field()
    # 营业总收入(万元)
    total_revenue = scrapy.Field()
    # 营业总收入同比增长率
    total_revenue_growth_rate = scrapy.Field()
    # 每股净资产(元)
    net_assets_per_share = scrapy.Field()
    # 净资产收益率
    ROE = scrapy.Field()
    # 净资产收益率-摊薄
    ROE_diluted = scrapy.Field()
    # 资产负债比率
    asset_liability_ratio = scrapy.Field()
    # 每股资本公积金(元)
    per_share_capital_fund = scrapy.Field()
    # 每股未分配利润(元)
    non_distribution_of_profit_per_share = scrapy.Field()
    # 每股经营现金流(元)
    operating_cash_flow_per_share = scrapy.Field()
    # 销售毛利率
    gross_margin_sales = scrapy.Field()
    # 存货周转率
    inventory_turnover_rate = scrapy.Field()


class CompanyItem(scrapy.Item):
    Company_profile = scrapy.Field()
    Declare_price = scrapy.Field()
    Day_trend = scrapy.Field()
    Historical_trend = scrapy.Field()
    Company_news = scrapy.Field()
    Historical_evolution = scrapy.Field()
    Senior_Executive = scrapy.Field()
    Equity_position = scrapy.Field()
    Ten_major_shareholders = scrapy.Field()
    Financial_index = scrapy.Field()
    Company_announcement = scrapy.Field()
    Stock_Research_Report = scrapy.Field()
    # 公司概况
    # 申报价格
    # 当日走势
    # 历史走势
    # 公司新闻
    # 历史沿革
    # 高管人员
    # 股本状况
    # 十大股东
    # 财务指标
    # 公司公告
    # 个股研报