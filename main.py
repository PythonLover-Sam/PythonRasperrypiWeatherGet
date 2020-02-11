import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

token = "aG0cHYX2rbeVwaKl"  # 彩云天气令牌
regionData1 = pd.read_csv('globalcities.csv')
regionData2 = pd.read_csv('cityidloc-20180625.csv')


"""初始化城市数据字典"""
cities_loc_list = []
# 添加国际城市
for i in range(len(regionData1['城市名中文'].values)):
    cities_loc_list.append((regionData1['城市名英文'].values[i], (regionData1['城市名中文'].values[i], regionData1['经度'].values[i], regionData1['纬度'].values[i])))
# 添加国内城市 注意：检索方式为输入行政区号
for i in range(len(regionData2['行政区编号'].values)):
    cities_loc_list.append((str(regionData2['行政区编号'].values[i]), (regionData2['一级'].values[i], regionData2['二级'].values[i], regionData2['三级'].values[i], regionData2['经度'].values[i], regionData2['纬度'].values[i])))
cities_loc_dict = dict(cities_loc_list)


def get_city_loc(city, city_dict):
    if city in city_dict.keys():
        return city_dict[city]
    else:
        return "No such city is found!"

def get_weather_data(location, result_list, mode):
    """联网模块，获取传入参数的天气数据"""
    if location == "No such city is found!":
        return "Argument error!"
    else:
        url_1 = "https://api.caiyunapp.com/v2/{}/{}/{}.json".format(token, str(location[-2])+','+str(location[-1]), mode)
        webpage = requests.get(url_1)
        soup = BeautifulSoup(webpage.text, 'lxml')
        data = json.loads(soup.p.get_text())
        print(data)



if __name__ == '__main__':

    location = get_city_loc('London', cities_loc_dict)  # 在此处修改第一个参数为想要查询地点的字符串，国际城市为英语单词，国内城市为区域编号
    get_weather_data(location, None, 'hourly')

