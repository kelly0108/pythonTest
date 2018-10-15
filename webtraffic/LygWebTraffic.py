import types
import urllib.request
import urllib.error
import json
import http.cookiejar
from xlutils.copy import copy;

import xlrd

duan = "--------------------------"  # 在控制台断行区别的


class LlData():
    pass
provinceNameList=['广东省','北京市','山东省','河南省','福建省','河北省','江苏省','浙江省','四川省','江西省','湖南省','安徽省','云南省','湖北省',
                  '辽宁省','广西壮族自治区','山西省','上海市','天津市','黑龙江省','重庆市','内蒙古自治区','陕西省',
                  '贵州省','吉林省','甘肃省','海南省','台湾省','宁夏回族自治区','青海省','新疆维吾尔自治区','香港特别行政区','西藏自治区','澳门特别行政区']

# 获取网站流量数据
def wangzhanLLUrl(stDate, etDate, siteId, phpSessionId):
    try:
        url = "https://web.umeng.com/main.php?c=flow&a=trend&ajax=module%3Dsummary%7Cmodule%3DfluxList_currentPage%3D1_pageType%3D30&siteid=" + siteId + "&st=" + stDate + "&et=" + etDate + "&_=1537838326729"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        headers = {"User-Agent": user_agent, "cookie": "PHPSESSID=" + phpSessionId}

        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req).read()
        return data
    except Exception as e:
        print(e)


# 解析网站流量
def praserWangzhanJsonFile(jsonData):
    value = json.loads(jsonData)
    summaryObj = value['data']["summary"]['items']
    rv = LlData();
    rv.pv = summaryObj["pv"]
    rv.uv = summaryObj["uv"]
    rv.ip = summaryObj["ip"]
    rv.session = summaryObj["session"]  # 访问次数
    rv.outper = summaryObj['outper']  # 跳出率
    rv.averagepv = summaryObj["averageupv"]  # 人均浏览页数
    return rv;


# 获取网站流量数据
def outerPerUrl(stDate, etDate, siteId, phpSessionId):
    try:
        url = "https://web.umeng.com/main.php?c=flow&a=trend&ajax=module%3Dsummary%7Cmodule%3DfluxList_currentPage%3D1_pageType%3D30&siteid=" + siteId + "&st=" + stDate + "&et=" + etDate + "&_=1537838326729"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        headers = {"User-Agent": user_agent, "cookie": "PHPSESSID=" + phpSessionId}
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req).read()
        return data
    except Exception as e:
        print(e)


# 解析网站流量
def praserOuterJsonFile(jsonData, rv):
    value = json.loads(jsonData)
    summaryObj = value['data']["summary"]['items']
    rv.averagestime = summaryObj["averagestime"]  # 平均访问时长


# 获取M站数据
def getMWebData(rv, stDate, etDate, siteId, phpSessionId):
    try:
        url = "https://web.umeng.com/main.php?c=cont&a=domain&ajax=module=summary|module=safeinfo|module=statistics_orderBy=pv_orderType=-1_currentPage=1_pageType=30&siteid=" + siteId + "&st=" + stDate + "&et=" + etDate + "&domaintype=&condtype=&condname=&condvalue="
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        headers = {"User-Agent": user_agent, "cookie": "PHPSESSID=" + phpSessionId}
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req).read().decode("utf8")
        value = json.loads(data)
        summaryObj = value['data']["statistics"]['items'][1]
        rv.mpv = summaryObj["pv"]
        rv.muv = summaryObj["uv"]
        rv.mip = summaryObj["ip"]
    except Exception as e:
        print(e)


# 教师iphone新增用户数
def getAppNewUserData(rv, stDate, etDate, relatedId, ummo_ss):
    try:
        url = "https://mobile.umeng.com/ht/api/v3/app/retention/trend?relatedId=" + relatedId
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        headers = {"User-Agent": user_agent,
                   "content-type": "application/json;charset=UTF-8",
                   "cookie": "ummo_ss=" + ummo_ss}
        raw = {
            "relatedId": relatedId,
            "fromDate": stDate,
            "toDate": etDate,
            "version": [],
            "channel": [],
            "timeUnit": "day",
            "index": 0,
            "view": "retentionTrend",
            "type": "newUser"
        }
        postdata = json.dumps(raw)
        postdata = bytes(postdata, 'utf8')
        req = urllib.request.Request(url, postdata, headers=headers)
        rvdata = urllib.request.urlopen(req).read().decode("utf8")
        value = json.loads(rvdata)
        return value['data']["items"][0]['data'][0]
    except Exception as e:
        print(e)


# 教师活跃用户数  {"timeUnit": "week", "view": "activeUserWeek"}周活
def getAppActiveUserData(stDate, etDate, relatedId, ummo_ss, umplus_uc_token, timeUnit, view):
    try:
        url = " https://mobile.umeng.com/ht/api/v3/app/user/active/detail?relatedId=" + relatedId
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        headers = {"User-Agent": user_agent,
                   "content-type": "application/json;charset=UTF-8",
                   "cookie": "ummo_ss=" + ummo_ss + ";umplus_uc_token=" + umplus_uc_token}
        raw = {
            "page": 1,
            "pageSize": 30,
            "relatedId": relatedId,
            "fromDate": stDate,
            "toDate": etDate,
            "version": [],
            "channel": [],
            "timeUnit": timeUnit,
            "view": view
        }

        postdata = json.dumps(raw)
        postdata = bytes(postdata, 'utf8')
        req = urllib.request.Request(url, postdata, headers=headers)
        rvdata = urllib.request.urlopen(req).read().decode("utf8")
        value = json.loads(rvdata)
        return value['data']["items"][0]
    except Exception as e:
        print(e)


# 周设备来源数据
def getAppEquipData(stDate, etDate, appId, ummo_ss, umplus_uc_token):
    try:
        url = "https://mobile.umeng.com/apps/" + appId + "/reports/load_table_data?page=1&per_page=30&start_date=" + stDate + "&end_date=" + etDate + "&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=daily&stats=devices_devices"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        headers = {"User-Agent": user_agent,
                   "content-type": "application/json;charset=UTF-8",
                   "cookie": "ummo_ss=" + ummo_ss + ";umplus_uc_token=" + umplus_uc_token}

        req = urllib.request.Request(url, headers=headers)
        rvdata = urllib.request.urlopen(req).read().decode("utf8")
        value = json.loads(rvdata)["stats"]
        for index in range(0, 10):
            print(value[index]["date"] + "\t" + str(
                value[index]["install_rate"]) + "%\t" + "week\t" + stDate + "\t" + etDate + "\t")
        # return value['data']["items"][0]
    except Exception as e:
        print(e)


def getProvinceLLData(stDate, etDate, siteId, phpSessionId):
    try:
        url = "https://web.umeng.com/main.php?c=visitor&a=districtnet&ajax=module%3Dsummary%7Cmodule%3DprovinceList_orderBy%3Dpv_orderType%3D-1_currentPage%3D1_pageType%3D90&siteid=" + siteId + "&st=" + stDate + "&et=" + etDate +"&_=1539567642079"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        headers = {"User-Agent": user_agent, "cookie": "PHPSESSID=" + phpSessionId}

        req = urllib.request.Request(url, headers=headers)
        rvdata = urllib.request.urlopen(req).read().decode("utf8")
        value = json.loads(rvdata)["data"]["provinceList"]["items"]
        counts = 0;
        for provinceName,provinceData in value.items():
            if provinceName in provinceNameList:
                counts=counts+1
                print(provinceName + "\t" + str(provinceData["pv"]) + "\t" + "week\t" + stDate + "\t" + etDate)
            if counts==34:
                break;

    except Exception as e:
        print(e)


def export_excel(rv):
    wb = xlrd.open_workbook("D:\\Kelly_work\\bigdata\\华图教师网数据统计\\新建文件夹\\流量统计_华图教师.xlsx");
    wbn = copy(wb);
    ws = wbn.get_sheet(0)
    ws.write(1, 6, rv.pv)
    ws.write(2, 6, rv.uv)
    ws.write(3, 6, rv.ip)
    ws.write(4, 6, rv.averagepv)
    ws.write(5, 6, rv.session)
    ws.write(6, 6, rv.averagestime)
    ws.write(7, 6, rv.outper)
    ws.write(8, 6, rv.iphoneNewUser)
    ws.write(9, 6, rv.androidNewUser)
    ws.write(10, 6, rv.mpv)
    ws.write(11, 6, rv.muv)
    ws.write(12, 6, rv.mip)
    wbn.save("D:\\Kelly_work\\bigdata\\华图教师网数据统计\\新建文件夹\\流量统计_华图教师_201810101.xlsx");


if __name__ == "__main__":
    phpSessionId = "hbqk96rts6eh0lv8io5qvfs8f0"  # CNZZ登录标识
    # 友盟APP统计的Sesssion
    ummo_ss = "BAh7CUkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjoGRVRbCEkiCVVzZXIGOwBGWwZvOhNCU09OOjpPYmplY3RJZAY6CkBkYXRhWxFpWWlBaQHdaQH%2BaQH9aQGYaQHFaQxpdWkIaRppIEkiGVoxZ1o0d2hVYnlhbE1OUDI5MTV1BjsAVEkiFHVtcGx1c191Y190b2tlbgY7AEYiPTFQMFRyNEx2VjNVZE5KRU5Gajc4eUVRXzliNWEzNGY0NjBiMjQ4NWViNDlmOTdlMjVjMDZlNzQ5SSIQX2NzcmZfdG9rZW4GOwBGSSIxOG1sN3lqK3JLaEFyZC92Ty9ERHZSajdRUXVwSVdUYklWUWZkRXdrTU9hWT0GOwBGSSIPc2Vzc2lvbl9pZAY7AFRJIiUyZDhkZTM2OTA3MzIxYmE2MDQ2NTFkZjAxODA1MzQ5NgY7AEY%3D--a07f445eeb0957b3596b005c7cfad1c91666ddbd"
    umplus_uc_token = "1P0Tr4LvV3UdNJENFj78yEQ_9b5a34f460b2485eb49f97e25c06e749"  # 周活月活时需要

    searchPerDates = ['2018-10-12','2018-10-13','2018-10-14']
    searchWeekDates = {'stDate': '2018-10-07', 'etDate': '2018-10-14','etDateForEquip': '2018-10-13'}  # 'stDate': '2018-09-30', 'etDate': '2018-10-07','etDateForEquip': '2018-10-06' etDateForEquip必须是7天的最后一天
    searchMonthDates = {}  # 'stDate':'2018-09-01','etDate':'2018-10-01'

    iphoneRelateId = "545097ebfd98c5d599014f43"
    androidRelateId = "54645278fd98c565730006bc"
    iphoneAppId = "34f410995d5c89dfbe790545"
    androidAppId = "cb600037565c89df87254645"
    siteId = "580664"

    it = iter(searchPerDates)  # 创建迭代器对象
    # 每日流量统计
    print("-----------日统计---------------")
    for stDate in it:
        et = stDate
        # 网站流量数据
        data = wangzhanLLUrl(stDate, stDate, siteId, phpSessionId)
        rv = praserWangzhanJsonFile(data)
        # 网站跳出率
        outerdata = outerPerUrl(stDate, et, siteId, phpSessionId).decode("utf8")
        praserOuterJsonFile(outerdata, rv)
        # M站数据
        getMWebData(rv, stDate, et, siteId, phpSessionId)
        # 登录友盟APP，自动记住cookie
        #  cj = http.cookiejar.CookieJar()
        #  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        #   r = opener.open(req)
        # 教师iphone新增用户数
        rv.iphoneNewUser = getAppNewUserData(rv, stDate, et, iphoneRelateId, ummo_ss)

        # 教师Android新增用户数
        rv.androidNewUser = getAppNewUserData(rv, stDate, et, androidRelateId, ummo_ss)
        # export_excel(rv) #导出到Excel中
        print("pv\t" + rv.pv + "\t" + stDate)
        print("uv\t" + rv.uv + "\t" + stDate)
        print("ip\t" + rv.ip + "\t" + stDate)
        print("人均浏览页数\t" + rv.averagepv + "\t" + stDate)
        print("访问次数\t" + rv.session + "\t" + stDate)
        print("平均访问时长\t" + rv.averagestime + "\t" + stDate)
        print("跳出率\t" + rv.outper + "\t" + stDate)
        print("新增用户\t" + str(rv.iphoneNewUser) + "\t" + stDate)
        print("新增用户\t" + str(rv.androidNewUser) + "\t" + stDate)
        print("pv\t" + rv.mpv + "\t" + stDate)
        print("uv\t" + rv.muv + "\t" + stDate)
        print("ip\t" + rv.mip + "\t" + stDate)

if 'stDate' in searchWeekDates:  # 有周活开始时间，需要查询周活、周设备来源数据
    print("-----------周统计---------------")
    print("-----------省份---------------")
    getProvinceLLData(searchWeekDates['stDate'], searchWeekDates['etDateForEquip'], siteId, phpSessionId)
    print("-----------------设备来源----------------------")
    getAppEquipData(searchWeekDates['stDate'], searchWeekDates['etDateForEquip'], iphoneAppId, ummo_ss, umplus_uc_token)
    getAppEquipData(searchWeekDates['stDate'], searchWeekDates['etDateForEquip'], androidAppId, ummo_ss,
                    umplus_uc_token)

    # 教师iphonem周活
    iphoneWeekActiveUser = getAppActiveUserData(searchWeekDates['stDate'], searchWeekDates['etDate'], iphoneRelateId,
                                                ummo_ss, umplus_uc_token, "week", "activeUserWeek")
    # 教师Android用活
    androidWeekActiveUser = getAppActiveUserData(searchWeekDates['stDate'], searchWeekDates['etDate'], androidRelateId,
                                                 ummo_ss, umplus_uc_token, "week", "activeUserWeek")
    print("-----------------周活----------------------")
    print(str(iphoneWeekActiveUser["activeUser"]) + "\tweek\t" + iphoneWeekActiveUser["date"].split("~")[0].replace("/","-") + "\t" +
          iphoneWeekActiveUser["date"].split("~")[1].replace("/", "-"))
    print(
        str(androidWeekActiveUser["activeUser"]) + "\tweek\t" + androidWeekActiveUser["date"].split("~")[0].replace("/","-") + "\t" +
        androidWeekActiveUser["date"].split("~")[1].replace("/", "-"))

if 'stDate' in searchMonthDates:  # 有月活开始时间，需要查询周活数据
    # 教师iphonem周活
    iphoneMonthActiveUser = getAppActiveUserData( searchMonthDates['stDate'], searchMonthDates['etDate'],
                                                 iphoneRelateId, ummo_ss, umplus_uc_token, "month", "activeUserMonth")
    # 教师Android用活
    androidMonthActiveUser = getAppActiveUserData(searchMonthDates['stDate'], searchMonthDates['etDate'],
                                                  androidRelateId, ummo_ss, umplus_uc_token, "month", "activeUserMonth")
    print("-----------------月活----------------------")
    print(str(iphoneMonthActiveUser["activeUser"]) + "\tmonth\t" + iphoneMonthActiveUser["date"].split("~")[0].replace(
        "/", "-") + "\t" + iphoneMonthActiveUser["date"].split("~")[1].replace("/", "-"))
    print(
        str(androidMonthActiveUser["activeUser"]) + "\tmonth\t" + androidMonthActiveUser["date"].split("~")[0].replace(
            "/", "-") + "\t" + androidMonthActiveUser["date"].split("~")[1].replace("/", "-"))
