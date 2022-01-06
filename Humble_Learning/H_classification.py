import numpy as np
from sklearn.linear_model import LogisticRegression
import time

Data = dict()
def get_input_data(filename):
    input_file = open(filename, 'r', encoding='UTF8')
    Exercise=[]

    for line in input_file:
        tmp = []
        line = line.replace('\n','')
        line = line.replace('\t'," ")
        line = line.split(" ")

        #print(line)
        for sig in line:
            tmp.append(float(sig))

        Exercise.append(tmp.copy())

    return Exercise

def TrainData() :

    curl = get_input_data("덤벨컬_학습용.txt")
    Data["Curl"] = curl

    kickBack = get_input_data("덤벨킥백_학습용.txt")
    Data["kickBack"] = kickBack

    return Data

def ValidateData() :

    curl = get_input_data("덤벨컬_검증용.txt")
    Data["Curl_V"] = curl

    kickBack = get_input_data("덤벨킥백_검증용.txt")
    Data["kickBack_V"] = kickBack

    return Data

def TestData() :

    curl = get_input_data("덤벨컬_테스트용.txt")
    Data["Curl_T"] = curl

    kickBack = get_input_data("덤벨킥백_테스트용.txt")
    Data["kickBack_T"] = kickBack

    return Data

def GenerateTrDataForm(data):
    c = "Curl"
    k = "kickBack"
    npDataC = np.array(data[c]).reshape(len(data[c]), 2)
    npDataK = np.array(data[k]).reshape(len(data[k]), 2)

    inData=np.concatenate((npDataC, npDataK), axis=0)

    #random.shuffle(inData)

    y_label=[]
    for i in range(0,len(data[c])):
        x='Dumbbell curl'
        y_label.append(x)


    for i in range(0,len(data[k])):
        x='Dumbbell kickBack'
        y_label.append(x)

    #random.shuffle(y_label)

    print(np.unique(y_label, return_counts=True))

    return inData, y_label

def GenerateVDataForm(data):
    c="Curl_V"
    k="kickBack_V"
    npDataC = np.array(data[c]).reshape(len(data[c]), 2)
    npDataK = np.array(data[k]).reshape(len(data[k]), 2)

    inData=np.concatenate((npDataC, npDataK),axis=0)

    #random.shuffle(inData)

    y_label=[]
    for i in range(0,len(data[c])):
        x='Dumbbell curl'
        y_label.append(x)


    for i in range(0,len(data[k])):
        x='Dumbbell kickBack'
        y_label.append(x)

    #random.shuffle(y_label)

    print(np.unique(y_label, return_counts=True))

    return inData, y_label

def GenerateTDataForm(data):
    c = "Curl_T"
    k = "kickBack_T"
    npDataC = np.array(data[c]).reshape(len(data[c]), 2)
    npDataK = np.array(data[k]).reshape(len(data[k]), 2)

    inData=np.concatenate((npDataC, npDataK),axis=0)

    #random.shuffle(inData)

    y_label=[]
    for i in range(0,len(data[c])):
        x='Dumbbell curl'
        y_label.append(x)


    for i in range(0,len(data[k])):
        x='Dumbbell kickBack'
        y_label.append(x)

    #random.shuffle(y_label)

    print(np.unique(y_label, return_counts=True))

    return inData, y_label

def main():
    trainingD = TrainData()
    x_train, y_train=GenerateTrDataForm(trainingD)

    ValidateD=ValidateData()
    x_val,y_val=GenerateVDataForm(ValidateD)

    TestD=TestData()
    x_test, y_test=GenerateTDataForm(TestD)

    start=time.time()
    softmax_reg = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=200, random_state=40)
    softmax_reg.fit((x_train), (y_train))

    softmax_reg.fit((x_val), (y_val))

    Result = softmax_reg.predict_proba(x_test).round(2)
    print(Result)

    Score=softmax_reg.score((x_test), (y_test))
    print(softmax_reg.class_weight)
    print(Score)

    print("runtime=",round((time.time()-start),2))
if __name__ == '__main__':
    main()