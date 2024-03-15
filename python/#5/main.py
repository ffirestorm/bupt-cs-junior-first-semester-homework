import aiohttp
import asyncio
import json
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np

async def fetch_data(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.text()

def convert_json_to_text(json_data):
    # 转换JSON为TEXT格式
    data = json.loads(json_data)
    text_result = ""
    for entry in data:
        text_result += " ".join([str(value) for value in entry.values()]) + "\n"
    return text_result

def convert_xml_to_text(xml_data):
    text_result = ""
    lines = xml_data.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("<Year>"):
            line = line.replace("<Year>", "").replace("</Year>", "")
            text_result += f"{line} "
        elif line.startswith("<No_Smoothing>"):
            line = line.replace("<No_Smoothing>", "").replace("</No_Smoothing>", "")
            text_result += f"{line} "
        elif line.startswith("<Lowess(5)>"):
            line = line.replace("<Lowess(5)>", "").replace("</Lowess(5)>", "")
            text_result += f"{line}\n"

    return text_result


def get_request():
    start_year = input("起始年份:")
    end_year = input("结束年份:")
    sort_by = input("按照year还是temperature排序? :")
    order = input("升序asc还是降序desc?: ")
    result_format = input("格式是json 还是 xml 还是 csv? : ")
    
    params = {
        'start_year': int(start_year),
        'end_year': int(end_year),
        'sort_by': sort_by,
        'order': order,
        'format':result_format
    }

    return params

def calculate_lowess(data, fraction = 0.2):
    years = [entry['Year'] for entry in data]
    no_smoothing = [entry['No_Smoothing'] for entry in data]

    lowess = sm.nonparametric.lowess(no_smoothing, years, frac=fraction)

    return lowess[:, 1]


async def main():
    url = 'http://localhost:8000'  # 你的服务端地址

    # 获取用户输入的查询参数
    params = get_request()
    data = ""
    # 获取JSON数据并转换为TEXT格式
    if params['format'] == 'json':
        json_data = await fetch_data(url, params)
        print("\nJSON数据 转成 TEXT:")
        text_json = convert_json_to_text(json_data)
        data = text_json
        print(text_json)

    # 获取XML数据并转换为TEXT格式
    elif params['format'] == 'xml':
        xml_data = await fetch_data(url, params)
        print(xml_data)
        text_xml = convert_xml_to_text(xml_data)
        print("\nXML数据 转成 TEXT:")
        print(text_xml)
        data = text_xml

    # 获取CSV数据并转换为TEXT格式
    elif params['format'] == 'csv':
        csv_data = await fetch_data(url, params)
        print("\nCSV数据:")
        text_csv = csv_data.replace(","," ")
        print(text_csv)
        data = text_csv

    # 作业4 计算lowess
    data_list = [line.split(" ") for line in data.split("\n")]
    year_list = []
    no_smoothing_list = []
    lowess_list = []
    for entry in data_list:
        if len(entry) == 3:
            year_list.append(int(entry[0]))
            no_smoothing_list.append(float(entry[1]))
            lowess_list.append(float(entry[2]))
    lowess = sm.nonparametric.lowess(no_smoothing_list, year_list, frac= 10/len(year_list))
    print("年份\t\t数据本身\t程序计算")
    for i in range(len(lowess)):
        print("{}:\t\t{}\t\t{:.2f}".format(year_list[i], lowess_list[i], lowess[i][1]))

    # 作业5
    # 将数据转换成numpy
    year_array = np.array(year_list)
    no_smoothing_array = np.array(no_smoothing_list)
    lowess_array = np.array(lowess_list)

    plt.plot(year_array, no_smoothing_array, label='No_Smoothing', marker='o', mec = 'gray', markerfacecolor='w', linestyle='-', color='gray')
    plt.plot(year_array, lowess_array, label='Lowess', color='k')
    plt.xlabel('YEAR')
    plt.ylabel('Temperature Anomaly(C)')
    font1 = {'family':'serif', 'color':'gray', 'size':10}
    plt.title("Source: climate.nasa.gov", fontdict=font1)
    plt.grid(True)
    plt.show()



if __name__ == '__main__':
    asyncio.run(main())