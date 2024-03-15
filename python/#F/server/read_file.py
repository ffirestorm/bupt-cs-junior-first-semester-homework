import numpy as np
from shapely.geometry import shape, Polygon

def pool_file(file_path, file_type="txt"):
    invalid_value = -9999
    if file_type == 'txt':
        input_array = np.loadtxt(file_path, skiprows=6)
    elif file_type == 'npy':
        input_array = np.load(file_path)
    input_array [input_array == invalid_value] = np.nan
        # 池化，四变一
    result_array = np.zeros((input_array.shape[0] // 2, input_array.shape[1] // 2))

    # 横纵步长为1，提取特征
    for i in range(0, input_array.shape[0], 2):
        for j in range(0, input_array.shape[1], 2):
            block = input_array[i:i+2, j:j+2]
            # 计算均值时忽略 NaN 值
            if np.any(~np.isnan(block)):
                result_array[i // 2, j // 2] = np.nanmean(block)
    return result_array


def convert_file():
    base_path = "D:\下载/gpw-v4-population-count-rev11_2020_30_sec_asc/"
    for i in range(1, 9):
        file_path = base_path+"gpw_v4_population_count_rev11_2020_30_sec_"+str(i)+".asc"
        result_data = pool_file(file_path)
        np.save("./data/pool_1_"+str(i)+".npy", result_data)
        print("{} ok".format(i))
        for j in range(1, 3):
            input_path = "./data/pool_"+str(j)+"_"+str(i)+".npy"
            pool_data = pool_file(input_path,"npy")
            output_path = "./data/pool_"+str(j+1)+"_"+str(i)+".npy"
            np.save(output_path, pool_data)
            print("{}, {}".format(i, j))


def read_data(file_path):
    ret_array = np.load(file_path)
    return ret_array

def get_data():
    data_list = []
    for i in range(1, 9):
        file_path = "../dataset/pool_4_"+str(i)+".npy"
        data_list.append(read_data(file_path))
    
    return np.concatenate([np.concatenate(data_list[:4], axis=1), np.concatenate(data_list[4:], axis=1)], axis=0)

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

# convert_file()