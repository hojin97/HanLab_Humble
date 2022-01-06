import matplotlib.pylab as plt
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def copy_dimesion_2_list(input_list):
    output_list = []
    for row in input_list:
        output_list.append(row.copy())
    return output_list

def input_file(file_list, data_type):
    each_result_data = []
    merge_result_data = []
    rms_data_set = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    ang_data_set = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    for file_name in file_list:
        with open('./' + data_type + '/' + file_name) as file:
            each_row = [[],[],[]]
            count = 0
            for line in file:
                if line == '\n':
                    break
                sp = line.split()
                each_row[0].append(float(sp[0]))    # 시간
                each_row[1].append(float(sp[1]))    # RMS
                each_row[2].append(float(sp[2]))    # ANGLE
                rms_data_set[count].append(float(sp[1]))
                ang_data_set[count].append(float(sp[2]))
                count += 1
            each_row = copy_dimesion_2_list(each_row)
            each_result_data.append(each_row)
    rms_data_set = np.array(rms_data_set.copy())
    ang_data_set = np.array(ang_data_set.copy())
    merge_result_data.append(rms_data_set)
    merge_result_data.append(ang_data_set)

    return each_result_data, merge_result_data

# X = time 축
# merge_data[0] 은 RMS 값
# merge_data[1] 은 ANG 값
def print_graph(each_datas, merge_data, type, title):
    X = each_datas[0][0]
    if type == 'rms':
        y = merge_data[0]
    elif type == 'ang':
        y = merge_data[1]

    for i, data in enumerate(y):
        plt.plot([X[i] for v in range(len(data))], data, 'b. ')

    t_X = np.array(each_datas[0][0])
    y = np.array(y)
    t_size = y.shape[1]

    X = []
    for x_data in t_X:
        X.extend([x_data for i in range(t_size)])
    X = np.array(X)
    X = X.reshape((-1, 1))
    y = y.reshape((-1, 1))

    poly_features = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly_features.fit_transform(X)

    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, y)

    plt.plot(X, lin_reg.predict(X_poly), 'r-')
    plt.axis('auto')
    plt.grid()
    plt.title(f"{title} : {type}")
    plt.show()

def output_data(each_data_1, merge_data, type, title):
    t_X = np.array(each_data_1[0][0])

    if type == 'rms':
        y = np.array(merge_data[0])
    elif type == 'ang':
        y = np.array(merge_data[1])

    size = y.shape[1]

    X = []
    for x_data in t_X:
        X.extend([x_data for i in range(size)])
    X = np.array(X)
    X = X.reshape((-1, 1))
    y = y.reshape((-1, 1))

    # -- Linear regression
    poly_features = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly_features.fit_transform(X)

    lin_reg = LinearRegression()

    lin_reg.fit(X_poly, y)

    #t_X = t_X.reshape((-1, 1))
    #print(lin_reg.predict(X_poly))


    file = open(f"./output_regression/{title}_{type}.txt", 'w')
    data_range = lin_reg.predict(X_poly)
    prev = [-100]
    for data in data_range:
        if prev == data:
            continue
        prev = data
        file.write(f"{data[0]}\n")
    file.close()


    #print(lin_reg.predict(X_poly))


def main():
    path_dir1 = 'C:/Users/Hojin/Desktop/Prj.HomePT/pyunicorn/data_2do'
    path_dir2 = 'C:/Users/Hojin/Desktop/Prj.HomePT/pyunicorn/data_3do'
    file_list1 = os.listdir(path_dir1)
    file_list2 = os.listdir(path_dir2)

    each_data_1, merge_data_1 = input_file(file_list1, 'data_2do')
    each_data_2, merge_data_2 = input_file(file_list2, 'data_3do')


    output_data(each_data_1, merge_data_1, 'rms', '2do')
    output_data(each_data_1, merge_data_1, 'ang', '2do')
    output_data(each_data_2, merge_data_2, 'rms', '3do')
    output_data(each_data_2, merge_data_2, 'ang', '3do')

    '''
    print_graph(each_data_1, merge_data_1, 'rms', 'Biceps')
    print_graph(each_data_1, merge_data_1, 'ang', 'Biceps')
    print_graph(each_data_2, merge_data_2, 'rms', 'Triceps')
    print_graph(each_data_2, merge_data_2, 'ang', 'Triceps')
    '''

main()

