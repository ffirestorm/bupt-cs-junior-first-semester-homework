import requests
import json
from shapely.geometry import shape
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch


def query_server(geojson):
    url = "http://localhost:8000/population"
    data = {"geojson":geojson}
    headers = {"Content-Type": "application/json"}
    server_res = requests.post(url, data=json.dumps(data), headers=headers)
    if not server_res.status_code == 200:
        print("Error:", server_res.status_code)
        return None, None
    
    res_data = server_res.json()
    print(res_data)
    population = res_data["total_population"]
    data_list = res_data["data"] 
    data_dtype = np.dtype(res_data["dtype"])
    data_shape = res_data["shape"]
    data = np.array(data_list, dtype=data_dtype).reshape(data_shape)
    
    return data, population


def draw_map_scatter(data, polygon, total_population):
    min_lon, min_lat, max_lon, max_lat = polygon.bounds

    polygon_path = Path(np.array(polygon.exterior.coords))
    
    # 绘制地图
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 获取散点坐标
    lon, lat = np.meshgrid(np.linspace(min_lon, max_lon, data.shape[1]), np.linspace(min_lat, max_lat, data.shape[0])[::-1])


    # 将数据展平为一维数组
    data_flat = data.flatten()
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    # 使用Scatter散点图
    sc = ax.scatter(lon.flatten(), lat.flatten(), c=data_flat, cmap='coolwarm', norm=LogNorm(), s=3, edgecolors='none')
    
    # 使用 PathPatch 绘制多边形并设置为透明
    patch = PathPatch(polygon_path, facecolor='none')
    ax.add_patch(patch)

    # 设置多边形内部为透明
    sc.set_clip_path(patch)
    
    # 添加颜色条
    plt.colorbar(sc, ax=ax, label='Population', ticks=[10, 100, 1000, 10000, 100000], format='%.0f')

    ax.set_title('Population Distribution: {:.0f}'.format(total_population))
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.axis('equal')
    ax.grid(True)

    plt.show()


if __name__ == "__main__":
    geojson_polygon_1 = {
        "type": "Polygon",
        "coordinates": [
            [[30.0, 25.0], [40.0, 55.0], [20.0, 65.0], [10.0, 55.0], [30.0, 25.0]]
        ]
    }
    
    geojson_polygon_2 = {
        "type": "Polygon",
        "coordinates": [
            [[-157.6, 56.8], [-103.5, 40.0], [-120.2, 30.7]]
        ]
    }

    geojson_polygon_3 = {
        "type": "Polygon",
        "coordinates": [
            [[80.0, 80.0], [-179.0, 0.0], [80.0, -80.0], [179.0, 0.0]]
        ]
    }

    geojson_polygon_4 = {
        "type": "Polygon",
        "coordinates": [
            [[105.3, 40.0], [122.0, 40.0], [121.0, 23.5]]
        ]
    }

    geojson_polygon_5 = {
        "type": "Polygon",
        "coordinates": [
            [[90.0, 45.0], [122.0, 40.0], [121.0, 23.5],[101.5, 30.0], [95.0, 38.5]]
        ]
    }

    geojson_polygon_6 = {
        "type": "Polygon",
        "coordinates": [
            [[-70.0, 20.0], [-90.0, 0.0], [-70.0, -55.0],[-50.0, -45.0], [-30.0, -10.0]]
        ]        
    }

    geojson_polygon_7 = {
        "type": "Polygon",
        "coordinates": [
            [[-179.0, 89.0], [-179.0, -89.0], [179.0, -89.0]]
        ]
    }

    geojson_polygon_8 = {
        "type": "Polygon",
        "coordinates": [
            [[-179.0, 89.0], [-179.0, -89.0], [179.0, -89.0], [179.0, 89.0]]
        ]
    }
    geojson_polygon_9 = {
        "type":"Polygon",
        "coordinates":[
            [[30.0,10.0],[40.0,10.0],[40.0,40.0],[30.0,40.0],[30.0,10.0]]
        ]
    }
    geojson_polygon = geojson_polygon_8
    polygon = shape(geojson_polygon)
    data, population = query_server(geojson=geojson_polygon)

    draw_map_scatter(data, polygon, population)




def draw_map(data, polygon, total_population):
    min_lon, min_lat, max_lon, max_lat = polygon.bounds

    polygon_path = Path(np.array(polygon.exterior.coords))
    # 绘制地图
    fig, ax = plt.subplots(figsize=(10, 5))
    colormap = plt.cm.jet
    colormap.set_bad(color='white')
    # 使用 imshow 绘制底部的图层
    im = ax.imshow(data, extent=(min_lon, max_lon, min_lat, max_lat), cmap=colormap ,norm=LogNorm())

    # 使用 PathPatch 绘制多边形并设置为透明
    patch = PathPatch(polygon_path, facecolor='none')
    ax.add_patch(patch)

    # 设置多边形内部为透明
    im.set_clip_path(patch)

    # 添加颜色条
    plt.colorbar(im, ax=ax, label='Population', ticks=[0, 10, 100, 1000, 10000, 100000], format='%.0f')

    ax.set_title('Population Distribution: {:.0f}'.format(total_population))
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True)

    plt.show()