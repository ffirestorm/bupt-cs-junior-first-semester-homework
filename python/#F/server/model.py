from shapely.geometry import Polygon, shape
import numpy as np
import matplotlib.pyplot as plt
import read_file as rd
from matplotlib.colors import LogNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch
def get_population_in_polygon(data, polygon):
    # Step 1: 将 GeoJSON 多边形坐标转换为网格坐标
    min_lon, min_lat, max_lon, max_lat = polygon.bounds
    print(polygon.bounds)
    # 假设每行包含1/15个经度范围的数据
    cellsize = 1.0 / 15.0

    min_col = int((min_lon + 180) / cellsize)
    max_col = int((max_lon + 180) / cellsize)
    min_row = int((90 - max_lat) / cellsize)
    max_row = int((90 - min_lat) / cellsize)

    print(min_col)
    print(max_col)
    print(min_row)
    print(max_col)
    # Step 2: 遍历多边形所包含的所有网格
    total_population = 0

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            # 计算网格与多边形相交部分的面积
            grid_coords = (row, col)
            grid_polygon = get_polygon_from_grid_coords(grid_coords, cellsize, cellsize)
            intersection_area = grid_polygon.intersection(polygon).area

            # Step 3: 根据网格列表获取相应的人口数据
            grid_population = data[row, col]

            # Step 4: 根据面积比例调整人口数据
            adjusted_population = grid_population * (intersection_area / grid_polygon.area)
            
            total_population += adjusted_population

    return total_population

def get_polygon_from_grid_coords(grid_coords, cellsize_lon, cellsize_lat):
    row, col = grid_coords
    min_lon = col * cellsize_lon - 180
    max_lon = (col + 1) * cellsize_lon - 180
    min_lat = 90 - (row + 1) * cellsize_lat
    max_lat = 90 - row * cellsize_lat

    polygon = Polygon([
        (min_lon, min_lat),
        (max_lon, min_lat),
        (max_lon, max_lat),
        (min_lon, max_lat),
        (min_lon, min_lat)
    ])

    return polygon

def plot_population_distribution(data, polygon):
    # 创建一个网格用于绘制人口分布图
    lon_grid = np.linspace(-180, 180, data.shape[1] + 1)
    lat_grid = np.linspace(90, -90, data.shape[0] + 1)

    # 绘制地图
    plt.figure(figsize=(10, 5))

    # 使用 LogNorm 进行颜色归一化，以更好地显示不同数量级的人口
    plt.imshow(data, extent=[lon_grid[0], lon_grid[-1], lat_grid[-1], lat_grid[0]], cmap='viridis', origin='upper', norm=LogNorm())

    # 绘制查询的多边形区域
    polygon_coords = np.array(polygon.exterior.xy).T
    plt.plot(polygon_coords[:, 0], polygon_coords[:, 1], color='red', linestyle='--', linewidth=2)

    # 添加颜色条
    plt.colorbar(label='Population', ticks=[1, 10, 100, 1000], format='%.0e')

    plt.title('Population Distribution')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()

def draw_map(data, polygon):
    min_lon, min_lat, max_lon, max_lat = polygon.bounds

    cellsize = 1.0 / 15.0

    min_col = int((min_lon + 180) / cellsize)
    max_col = int((max_lon + 180) / cellsize)
    min_row = int((90 - max_lat) / cellsize)
    max_row = int((90 - min_lat) / cellsize)
    
    data = data[min_row:max_row+1, min_col:max_col+1]
    polygon_path = Path(np.array(polygon.exterior.coords))
    # 绘制地图
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 创建画笔
    colormap = plt.cm.jet
    colormap.set_bad(color='white')
    # 使用 imshow 绘制底部的图层
    im = ax.imshow(data, extent=(min_lon, max_lon, min_lat, max_lat), cmap=colormap, norm=LogNorm())
    # 使用 PathPatch 绘制多边形并设置为透明
    patch = PathPatch(polygon_path, facecolor='none')
    ax.add_patch(patch)

    # 设置多边形内部为透明
    im.set_clip_path(patch)

    # 添加颜色条
    plt.colorbar(im, ax=ax, label='Population', ticks=[1, 10, 100, 1000], format='%.0f')

    ax.set_title('Population Distribution')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True)

    # 显示图例
    ax.legend().set_visible(False)

    plt.show()


geojson_polygon_1 = {
    "type": "Polygon",
    "coordinates": [
        [[30.0, 10.0], [40.0, 40.0], [20.0, 40.0], [10.0, 20.0], [30.0, 10.0]]
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
        [[90.0, 90.0], [-180.0, 0.0], [90.0, -90.0], [180.0, 0.0]]
    ]
}

geojson_polygon_4 = {
    "type": "Polygon",
    "coordinates": [
        [[105.3, 40.0], [122.0, 40.0], [121.0, 23.5]]
    ]
}

polygon_2 = shape(geojson_polygon_4)


data = rd.get_data()
print(data.shape)
population_in_polygon = get_population_in_polygon(data, polygon_2)
print("人口分布总数:", population_in_polygon)

draw_map(data, polygon_2)
# print(get_population_in_polygon(data, polygon_2))