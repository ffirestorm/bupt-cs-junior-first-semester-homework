from sanic import Sanic, response
import pandas as pd
import xml.etree.ElementTree as ET
app = Sanic(__name__)

# 读取数据文件
data_file = "graph.txt"
df = pd.read_csv(data_file, sep="\s+", comment="#", names=["Year", "No_Smoothing", "Lowess(5)"])

# 定义路由处理器
@app.route("/")
async def query_data(request):
    # 获取查询参数
    start_year = int(request.args.get("start_year", 1880))
    end_year = int(request.args.get("end_year", 2022))
    sort_by = request.args.get("sort_by", "year")  # 默认按年份排序
    order = request.args.get("order", "asc")    # 默认升序

    # 进行数据过滤和排序
    filtered_data = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    if sort_by == "temperature":
        filtered_data = filtered_data.sort_values(by='No_Smoothing', ascending=(order == 'asc'))
    else:
        filtered_data = filtered_data.sort_values(by='Year' if order == "asc" else '-Year')

    # 获取查询结果
    result_format = request.args.get("format", "json")

    if result_format == "json":
        result = filtered_data.to_dict(orient="records")
        return response.json(result)
    
    elif result_format == "xml":
        # 生成XML格式的文本响应
        xml_result = "<result>\n"
        for index, row in filtered_data.iterrows():
            year = int(row['Year'])
            no_smoothing = row['No_Smoothing']
            lowess = row['Lowess(5)']
            xml_result += f"\t<entry>\n\t\t<Year>{year}</Year>\n\t\t<No_Smoothing>{no_smoothing:.2f}</No_Smoothing>\n\t\t<Lowess(5)>{lowess:.2f}</Lowess(5)>\n\t</entry>\n"
        xml_result += "</result>"
        return response.text(xml_result, content_type="text/plain")

    elif result_format == "csv":
        # result = filtered_data.to_csv(index=False)
        # return response.text(result, content_type="text/csv")
        text_result = ""
        for index, row in filtered_data.iterrows():
            year = int(row['Year'])
            text_result += f"{year},{row['No_Smoothing']:.2f},{row['Lowess(5)']:.2f}\n"
        return response.text(text_result, content_type="text/plain")

    return response.text("Invalid format requested", status=400)

if __name__ == "__main__":
    app.run(port=8000)