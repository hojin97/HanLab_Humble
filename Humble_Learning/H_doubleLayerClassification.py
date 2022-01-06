import numpy as np
import matplotlib.pyplot as plt


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

    RMS=[]
    for i in inData:
        tmp=i[0]
        RMS.append(tmp)

    ANG=[]
    for i in inData:
        tmp=i[1]
        ANG.append(tmp)

    RMS = np.array(RMS).reshape(len(inData),1)
    ANG = np.array(ANG).reshape(len(inData),1)

    # normalRMS = ((RMS-np.mean(RMS)) / (np.std(RMS)))
    # normalANG = ((ANG-np.mean(ANG)) / (np.std(ANG)))

    # Min-Max normalize
    normalRMS=(RMS-np.min(RMS))/(np.max(RMS)-np.min(RMS))
    normalANG=(ANG-np.min(ANG))/(np.max(ANG)-np.min(ANG))

    print(f"minR:{np.min(RMS)},max-min{np.max(RMS)-np.min(RMS)}")
    print(f"minA:{np.min(ANG)},max-min{np.max(ANG) - np.min(ANG)}")

    inData=np.hstack((normalRMS, normalANG))

    y_label=[]
    for i in range(0, len(data[c])):
        x=0       # biceps: 0, tri : 1
        y_label.append(x)


    for i in range(0,len(data[k])):
        x=1
        y_label.append(x)


    y_label=np.array(y_label)
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
        x=0
        y_label.append(x)


    for i in range(0,len(data[k])):
        x=1
        y_label.append(x)

    #random.shuffle(y_label)

    RMS = []
    for i in inData:
        tmp = i[0]
        RMS.append(tmp)

    ANG = []
    for i in inData:
        tmp = i[1]
        ANG.append(tmp)

    RMS = np.array(RMS).reshape(len(inData), 1)
    ANG = np.array(ANG).reshape(len(inData), 1)

    #normalRMS = ((RMS - np.mean(RMS)) / np.std(RMS))
    #normalANG = ((ANG - np.mean(ANG)) / np.std(ANG))

    # Min-Max normalize
    normalRMS = (RMS - np.min(RMS)) / (np.max(RMS) - np.min(RMS))
    normalANG = (ANG - np.min(ANG)) / (np.max(ANG) - np.min(ANG))

    inData = np.hstack((normalRMS, normalANG))


    #print(np.unique(y_label, return_counts=True))

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
        x=0
        y_label.append(x)


    for i in range(0,len(data[k])):
        x=1
        y_label.append(x)

    RMS = []
    for i in inData:
        tmp = i[0]
        RMS.append(tmp)

    ANG = []
    for i in inData:
        tmp = i[1]
        ANG.append(tmp)

    RMS = np.array(RMS).reshape(len(inData), 1)
    ANG = np.array(ANG).reshape(len(inData), 1)

    # normalRMS = ((RMS - np.mean(RMS)) / np.std(RMS))
    # normalANG = ((ANG - np.mean(ANG)) / np.std(ANG))

    # Min-Max normalize
    normalRMS = (RMS - np.min(RMS)) / (np.max(RMS) - np.min(RMS))
    normalANG = (ANG - np.min(ANG)) / (np.max(ANG) - np.min(ANG))

    inData = np.hstack((normalRMS, normalANG))
    return inData, y_label

trainingD = TrainData()
x_train, y_train=GenerateTrDataForm(trainingD)

x_train=x_train.transpose()
y_train=np.array(y_train).reshape(1, len(y_train))

ValidateD=ValidateData()
x_val,y_val=GenerateVDataForm(ValidateD)

x_val=x_val.transpose()
y_val=np.array(y_val).reshape(1, len(y_val))


TestD=TestData()
x_test, y_test=GenerateTDataForm(TestD)

x_test = x_test.transpose()
y_test = np.array(y_test).reshape(1, len(y_test))
# ===================================================================================
#plt.plot(x_train.T)
#plt.show()

def affine (W, X, B):
    return np.dot(W.T, X) + B

def sigmoid (o):
    return 1./(1+np.exp(-1*o))

def init_random_parameters (num_hidden = 2):

    W1 = np.random.rand(2,num_hidden)
    B1 = np.random.random((num_hidden,1))
    W2 = np.random.rand(num_hidden,1)
    B2 = np.random.random((1,1))
    return W1, B1, W2, B2

W1,B1,W2,B2=init_random_parameters ()

Z1=affine(W1,x_train,B1)
H=sigmoid(Z1)

Z2 = affine(W2,H, B2)
Y_hat = sigmoid(Z2)


def loss_eval(_params):
    W1, B1, W2, B2 = _params

    # Forward: input Layer
    Z1 = affine(W1, x_train, B1)
    H = sigmoid(Z1)

    # Forward: Hidden Layer
    Z2 = affine(W2, H, B2)
    Y_hat = sigmoid(Z2)

    loss = 1. / x_train.shape[1] * np.sum(-1 * (y_train * np.log(Y_hat) + (1 - y_train) * np.log(1 - Y_hat)))
    return Z1, H, Z2, Y_hat, loss


loss_eval([W1, B1, W2, B2])[-1]


def get_gradients(_params):
    W1, B1, W2, B2 = _params
    m = x_train.shape[1]

    Z1, H, Z2, Y_hat, loss = loss_eval([W1, B1, W2, B2])

    # BackPropagate: Hidden Layer
    dW2 = np.dot(H, (Y_hat - y_train).T)
    dB2 = 1. / 4. * np.sum(Y_hat - y_train, axis=1, keepdims=True)
    dH = np.dot(W2, Y_hat - y_train)

    # BackPropagate: Input Layer
    dZ1 = dH * H * (1 - H)
    dW1 = np.dot(x_train, dZ1.T)
    dB1 = 1. / 4. * np.sum(dZ1, axis=1, keepdims=True)

    return [dW1, dB1, dW2, dB2], loss


def optimize(_params, learning_rate=0.1, iteration=1000, sample_size=0):
    params = np.copy(_params)

    loss_trace = []

    for epoch in range(iteration):

        dparams, loss = get_gradients(params)

        for param, dparam in zip(params, dparams):
            param += - learning_rate * dparam

        if (epoch % 100 == 0):
            loss_trace.append(loss)

    _, _, _, Y_hat_predict, _ = loss_eval(params)

    return params, loss_trace, Y_hat_predict

params = init_random_parameters(2)
new_params, loss_trace, Y_hat_predict = optimize(params, 0.1, 100000, 0)
#print(Y_hat_predict.shape)
#print()
print(np.mean(Y_hat_predict))

print("*"*80)
print(new_params)

def softmax(a):
    exp_a=np.exp(a)
    sum_exp_a=np.sum(exp_a)
    y=exp_a/sum_exp_a

    return y

#result=softmax(Y_hat)

def stepfunc(val):
    cri=np.mean(val)+0.01
    print(cri)
    result=[]
    countI=0
    count0=0
    for sign in val:
        for each in sign:

            if float(each)>cri:
                result.append('1')
                countI+=1
            else:
                result.append('0')
                count0+=1
    print(countI)
    print(count0)
    result=np.array(result).reshape(1,x_train.shape[1])
    return result
result = stepfunc(Y_hat_predict)
print("result:\n",result)
plt.plot(loss_trace)
plt.ylabel('loss')
plt.xlabel('iterations (per hundreds)')
plt.show()