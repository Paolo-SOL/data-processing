import re
import pandas as pd


def data_cleaning(path):
    # 数据清洗，保存到 csv 文件。
    Dta_File = open(path)
    DtaList = Dta_File.readlines()
    item = []
    for i in DtaList:
        Ip = re.search(r"\d+.\d+.\d+.\d", i).group()
        Date = re.search(r"\d+/\w+/\d+:", i).group()[:-1]
        Time = re.search(r"\d+:\d+:\d+\s\+", i).group()[:-2]
        Method = re.search(r"\"\w{3,}\s", i).group()[1:-1]
        Req = re.search(r"\s/\w*/\w*.*HTTP", i).group()[1:-5]
        Http = re.search(r"HTTP/1.1", i).group()
        Status = re.search(r"\s\d{3}", i).group()[1:]
        Page = re.search(r"\d{5,}", i)
        if (Page == None):
            Page = "NaN"
        else:
            Page = Page.group()
        Ua = re.search(r"\w{6,}/\d\.\d.*\"", i).group()[:-1]
        Array = [Ip, Date, Time, Method, Req, Http, Status, Page, Ua]
        item.append(Array)
    df = pd.DataFrame(item, columns=["Ip", "Date", "Time", "Method", "Req", "Http", "Status", "Page", "Ua"])
    Date = df['Date']
    file_name = str(pd.to_datetime(Date)[0])[:-9]
    df.to_csv(file_name + ".csv", index=False)
    # 查重步骤
    Tab_file = pd.read_csv(file_name + ".csv")
    df = pd.DataFrame(Tab_file)
    user_agent_list = [
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)',
        'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'Mozilla/5.0 (compatible; Neevabot/1.0; +https://neeva.com/neevabot)',
        'Mozilla/5.0 (compatible; BLEXBot/1.0; +http://webmeup-crawler.com/)',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; DataForSeoBot/1.0; +https://dataforseo.com/dataforseo-bot)',
        'Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)',
        'spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
        'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 '
        'Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/94.0.4606.71 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/69.0.3497.81 YisouSpider/5.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 '
        'Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/94.0.4606.81 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/69.0.3497.81 YisouSpider/5.0 Safari/537.36',
    ]
    spider_list = []
    userIP_list = []
    x = 0
    for x in range(int(df.shape[0])):
        if spider_list == []:
            if df['Ua'][x] in user_agent_list:
                spider_list.append(item[x])
            else:
                userIP_list.append(item[x])
        else:
            if df['Ua'][x] in spider_list or df['Ua'][x] in userIP_list:
                continue
            else:
                if df['Ua'][x] in user_agent_list:
                    spider_list.append(item[x])
                else:
                    userIP_list.append(item[x])
    sl = pd.Series(spider_list)
    ul = pd.Series(userIP_list)
    # 使用len_course 来获数组的个数
    len_course=range(0,len(ul))
    # 使用一个空数组承载我们的去重之后的用户IP
    # 通过 i 让其在 规定范围循环获取所需数组位置
    len_ip=[]
    for i in len_course:
        if i not in len_ip:
            len_ip.append(ul[i][0])
    # 获取不重复的数组
    LI=list(set(len_ip))
    # 使用 udd 将数组排列
    udd=pd.Series(LI)
    udd.to_csv(file_name+'用户代理IP去重表格.csv')
    sl.to_csv(file_name + "爬虫代理表格.csv")
    ul.to_csv(file_name + "用户代理表格.csv")
    print("用户代理去 Ua 重后个数:")
    print(df['Ua'].value_counts().count())
    print("爬虫代理个数:")
    print(sl.count())
    print('用户代理 IP 去重后个数：')
    print(len(udd))
    print("用户代理个数:")
    print(ul.count())
    print("数据已经成功清洗.")
def data_work():
    print("请选择您要进行的操作：")
    print("0:数据清洗；1：退出")
    cnt = int(input())
    if cnt == 0:
        print("请输入您要清洗的文件：")
        data_cleaning(path=input())
    else:
        print("结束操作！")
if __name__ == '__main__':
    data_work()
