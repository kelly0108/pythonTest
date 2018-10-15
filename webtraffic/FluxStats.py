# -*- coding: utf-8 -*-

import requests;
import json;
import xlrd, xlwt;
from xlutils.copy import copy;

# 获取流量数据
def flux_stast(self,st,et,siteid,phpsessid,umplus_uc_token,ism):
    url = "https://web.umeng.com/main.php?c=flow&a=trend&ajax=module%3Dsummary%7Cmodule%3DfluxList_currentPage%3D1_pageType%3D30&siteid=%d&st=%s&et=%s&_=1539154064131";
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'cookie' : 'PHPSESSID=%s;umplus_uc_token=%s;'%(phpsessid,umplus_uc_token)
    }
    resp = requests.get(url%(siteid,st,et),headers);
    content = json.loads(resp.content);
    res = {}
    if st == et :
        item = content["data"]["summary"]["item"]
        if ism :
            da = [item["pv"], item["uv"], item["ip"]];
        else:
            da = [item["pv"], item["uv"], item["ip"], item["averageupv"], item["session"], item["averagestime"],
                  item["outper"]];
        res = {item["st"]:da};
    else:
        items = content["data"]["fluxList"]["item"]
        for item in items :
            if ism :
                da = [item["pv"], item["uv"], item["ip"]];
            else:
                da = [item["pv"], item["uv"], item["ip"], item["averageupv"], item["session"], item["averagestime"],
                      item["outper"]];
            res[item["key"]] = da;
    return res;

def edit_excel01(items):
    wb = xlrd.open_workbook("C:\\Users\\huatu\\Desktop\\神策\\流量统计_腰果公考.xlsx");
    wbn = copy(wb);
    ws = wbn.get_sheet(0)

    ws.write(1, 6, items["pv"])
    ws.write(2, 6, items["uv"])
    ws.write(3, 6, items["ip"])
    ws.write(4, 6, items["averageupv"])
    ws.write(5, 6, items["session"])
    ws.write(6, 6, items["averagestime"])
    ws.write(7, 6, items["outper"])


arr = []
arr.append(1)

print(arr)