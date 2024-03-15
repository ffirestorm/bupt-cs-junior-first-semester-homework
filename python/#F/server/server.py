from sanic import Sanic
import read_file as rf
from sanic.response import json
from shapely.geometry import Polygon, shape

app = Sanic(__name__)
data = rf.get_data()
cellsize = 1.0/7.5
@app.post("/population")
async def query_population(request):
    try:
        print(request)
        req = request.json
        print(req)
        geojson_data = req['geojson']
        req_polygon = shape(geojson_data)

        # 执行查询
        total_population, min_col, max_col, min_row, max_row = get_population_in_polygon(data, req_polygon)
        ret_data = data[min_row:max_row+1, min_col:max_col+1]

        return json({
                "total_population": total_population,
                "dtype" : str(ret_data.dtype),
                "data": ret_data.tolist(),  
                "shape": ret_data.shape
        })
    except Exception as e:
        return json({"error": str(e)})
    

def get_population_in_polygon(data, polygon):
    # Step 1: 将 GeoJSON 多边形坐标转换为网格坐标
    min_lon, min_lat, max_lon, max_lat = polygon.bounds

    min_col = int((min_lon + 180) / cellsize)
    max_col = int((max_lon + 180) / cellsize)
    min_row = int((90 - max_lat) / cellsize)
    max_row = int((90 - min_lat) / cellsize)

    # Step 2: 遍历多边形所包含的所有网格
    total_population = 0

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            # 计算网格与多边形相交部分的面积
            grid_coords = (row, col)
            grid_polygon = get_polygon_from_grid_coords(grid_coords, cellsize)
            intersection_area = grid_polygon.intersection(polygon).area

            # 根据网格列表获取相应的人口数据
            grid_population = data[row, col]

            # 根据面积比例调整人口数据
            adjusted_population = grid_population * (intersection_area / grid_polygon.area)
            
            total_population += adjusted_population

    return total_population, min_col, max_col, min_row, max_row


def get_polygon_from_grid_coords(grid_coords, cellsize):
    row, col = grid_coords
    min_lon = col * cellsize - 180
    max_lon = (col + 1) * cellsize - 180
    min_lat = 90 - (row + 1) * cellsize
    max_lat = 90 - row * cellsize

    polygon = Polygon([
        (min_lon, min_lat),
        (max_lon, min_lat),
        (max_lon, max_lat),
        (min_lon, max_lat),
        (min_lon, min_lat)
    ])

    return polygon

if __name__ == "__main__":
    app.run(host="localhost", port=8000)