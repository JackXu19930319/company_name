from requests_html import HTMLSession
import time
import sys

session = HTMLSession()


def request(method, url, **kwargs):
    for i in range(3):
        try:
            res = session.request(method, url, **kwargs)
            time.sleep(0.5)
            return res
        except:
            time.sleep(1)
            continue
    sys.exit('request error')


def get_area_list():
    res = request('get', 'https://104.cht.com.tw/WebAP/Query.aspx')
    area_list = []
    for area in res.html.find('area'):
        area_list.append({'code': area.attrs['code'], 'area': area.attrs['alt']})
    return area_list


def get_params():
    res = request('get', 'https://104.cht.com.tw/WebAP/Query.aspx')
    __VIEWSTATE = res.html.find('#__VIEWSTATE', first=True).attrs['value']
    __VIEWSTATEGENERATOR = res.html.find('#__VIEWSTATEGENERATOR', first=True).attrs['value']
    return __VIEWSTATE, __VIEWSTATEGENERATOR


def main(keyword):
    area_list = get_area_list()
    url = "https://104.cht.com.tw/WebAP/Query.aspx"
    for area in area_list:
        __VIEWSTATE, __VIEWSTATEGENERATOR = get_params()
        payload = {
            'oneScriptManager': 'oneScriptManager|btnSend',
            '__VIEWSTATEENCRYPTED': '',
            '__ASYNCPOST': 'true',
            'btnSend': '搜尋',
            'txtName': keyword,
            'cityList': area['area'],
            'ddlarea': area['code'],
            'hidcode': area['code'],
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__VIEWSTATE': __VIEWSTATE,
        }
        search_page = request('post', url, data=payload)
        for i in search_page.html.find('td'):
            Name = i.find('div.Name', first=True)
            Phone = i.find('div.Phone', first=True)
            if Name and Phone:
                print(area['area'], Name.text, Phone.attrs['all'])
                return area['area'], Name.text, Phone.attrs['all']


if __name__ == '__main__':
    main('創新通信公司')
