import os
import numpy as np
import dtw

def copy_dimension_2_list(input_list):
    output_list = []
    for row in input_list:
        output_list.append(row.copy())
    return output_list

def input_file(path_dir, file_list):
    for file_name in file_list:
        with open(path_dir+'/'+file_name) as file:
            tmp_data = []
            for data in file:
                data = data.split()
                tmp_data.append(float(data[0]))
            if '2do' in file_name and 'rms' in file_name :
                ex_2do_rms = tmp_data.copy()
            elif '2do' in file_name and 'ang' in file_name :
                ex_2do_ang = tmp_data.copy()
            elif '3do' in file_name and 'rms' in file_name :
                ex_3do_rms = tmp_data.copy()
            elif '3do' in file_name and 'ang' in file_name :
                ex_3do_ang = tmp_data.copy()

    return ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang

def create_folder(filepath, folder_name):
    try:
        if not os.path.exists(filepath):
            os.makedirs(folder_name)
    except OSError:
        print('Error')

def input_dynamic_file(file_name, data_type):
    rms = []
    angle = []
    with open(data_type + '/' + file_name) as file:
        for line in file:
            line = line.split()
            if line == []:
                continue
            rms.append(float(line[1]))
            angle.append(float(line[2]))

    return rms, angle

def start_dtw(file_name, excercise_data, type1, type2, type3 = 10):
    c_rms, c_angle = input_dynamic_file(file_name, type1)
    ground_truth = excercise_data.copy()

    if type2 == 'rms':
        dynamic_data = c_rms.copy()
    elif type2 == 'ang':
        dynamic_data = c_angle.copy()

    alignment = dtw.dtw(ground_truth, dynamic_data, keep_internals=True)
    if type3 == 0:
        alignment.plot('twoway')
    #print(alignment.distance)
    return alignment.distance, len(c_rms)

def print_dtw_begin(file_type, ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang):
    path_dir = './'+file_type
    file_list = os.listdir(path_dir)

    print()
    print("*" * 30)
    print(f"{file_type} -> Biceps_rms")
    print("*" * 30)
    print()

    for file_name in file_list:
        start_dtw(file_name, ex_2do_rms, file_type, 'rms')

    print()
    print("*" * 30)
    print(f"{file_type} -> Biceps_ang")
    print("*" * 30)
    print()

    for file_name in file_list:
        start_dtw(file_name, ex_2do_ang, file_type, 'ang')

    print()
    print("*" * 30)
    print(f"{file_type} -> Triceps_rms")
    print("*" * 30)
    print()

    for file_name in file_list:
        start_dtw(file_name, ex_3do_rms, file_type, 'rms')

    print()
    print("*" * 30)
    print(f"{file_type} -> Triceps_ang")
    print("*" * 30)
    print()

    for file_name in file_list:
        start_dtw(file_name, ex_3do_ang, file_type, 'ang')

def dtw_begin(file_type, ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang):
    file_list = os.listdir(file_type)

    data_medoid = [[], 0, [], 0]

    for file_name in file_list:
        t_data, _ = start_dtw(file_name, ex_2do_rms, file_type, 'rms')
        data_medoid[0].append(t_data)

    for file_name in file_list:
        t_data, _ = start_dtw(file_name, ex_2do_ang, file_type, 'ang')
        data_medoid[1] += t_data

    for file_name in file_list:
        t_data, _ = start_dtw(file_name, ex_3do_rms, file_type, 'rms')
        data_medoid[2].append(t_data)

    for file_name in file_list:
        t_data, _ = start_dtw(file_name, ex_3do_ang, file_type, 'ang')
        data_medoid[3] += t_data

    # 1, 3 : ang, 0, 2 : rms
    data_medoid[0] = min(data_medoid[0])
    data_medoid[1] = data_medoid[1] / len(file_list)
    data_medoid[2] = min(data_medoid[2])
    data_medoid[3] = data_medoid[3] / len(file_list)

    return data_medoid

def predict_data(input_data_folder, input_data_file, data_2do_medoid, data_3do_medoid, ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang):
    label = ['Biceps', 'Triceps', 'Unknown']

    c_rms, _ = input_dynamic_file(input_data_file, input_data_folder)

    compare_point = [0, 0]
    compare_point[0], _ = start_dtw(input_data_file, ex_2do_ang, input_data_folder, 'ang')
    compare_point[1], _ = start_dtw(input_data_file, ex_3do_ang, input_data_folder, 'ang')

    # check 1 : Biceps
    check_point1 = [0, 0]
    check_point1[0] = abs(compare_point[0] - data_2do_medoid[1])
    check_point1[1] = abs(compare_point[1] - data_2do_medoid[3])

    # check 2 : Triceps
    check_point2 = [0, 0]
    check_point2[0] = abs(compare_point[0] - data_3do_medoid[1])
    check_point2[1] = abs(compare_point[1] - data_3do_medoid[3])

    # power threshold, count threshold
    ch_th = 0
    if sum(check_point1) < sum(check_point2) and abs(sum(check_point1) - sum(check_point2)) > 400:
        pw_th = 15
        cnt_th = 5
        for rms in c_rms:
            if rms < min(ex_2do_rms)-pw_th:
                ch_th += 1
        if ch_th >= cnt_th:
            return label[2]
        else:
            return label[0]

    elif sum(check_point1) > sum(check_point2) and abs(sum(check_point1) - sum(check_point2)) > 400:
        pw_th = 20
        cnt_th = 8
        for rms in c_rms:
            if rms < min(ex_3do_rms) - pw_th:
                ch_th += 1
        if ch_th >= cnt_th:
            return label[2]
        else:
            return label[1]

    else :
        return label[2]

def main():
    path_dir = 'C:/Users/Neurorobotics/Desktop/Prj.HomePT/pyunicorn/output_regression'
    file_list = os.listdir(path_dir)
    ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang = input_file(path_dir, file_list)
    data_2do_medoid = dtw_begin('C:/Users/Neurorobotics/Desktop/Prj.HomePT/pyunicorn/dynamic_2do', ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang)
    data_3do_medoid = dtw_begin('C:/Users/Neurorobotics/Desktop/Prj.HomePT/pyunicorn/dynamic_3do', ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang)

    input_data_folder = 'C:/Users/Neurorobotics/Desktop/Prj.HomePT/Project_File/HumbleData'
    input_data_file = os.listdir(input_data_folder).pop()

    pre_res = predict_data(input_data_folder, input_data_file, data_2do_medoid, data_3do_medoid, ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang)
    #print(pre_res)

    file = open('C:/Users/Neurorobotics/Desktop/Prj.HomePT/pyunicorn/predict.txt', 'w')
    file.write(pre_res)
    file.close()
    #print_dtw_begin('dynamic_2do', ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang)
    #print_dtw_begin('dynamic_3do', ex_2do_rms, ex_2do_ang, ex_3do_rms, ex_3do_ang)

    #time_stamp = [float(i / 10) for i in range(1, 21)]

if __name__ == '__main__':
    main()

