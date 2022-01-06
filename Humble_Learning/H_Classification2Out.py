import numpy as np
import matplotlib.pyplot as plt
import d2l
from mxnet import autograd, nd

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

    #print(inData.shape)
    #print(len(inData))
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

    inData=np.hstack((normalRMS, normalANG))

    #print("test data")
    #print(inData)

    y_label=[]
    for i in range(0, len(data[c])):
        x=0       # biceps: 0, tri : 1
        y_label.append(x)


    for i in range(0,len(data[k])):
        x=1
        y_label.append(x)

    #random.shuffle(y_label)


    #print(np.unique(y_label, return_counts=True))
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
        x='Dumbbell curl'
        y_label.append(x)


    for i in range(0,len(data[k])):
        x='Dumbbell kickBack'
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

#print("x_train=",x_train)
#print("y_train=",y_train)

ValidateD=ValidateData()
x_val,y_val=GenerateVDataForm(ValidateD)

x_val=x_val.transpose()
y_val=np.array(y_val).reshape(1, len(y_val))

#print("x_val=",x_val)
#print("y_val=",y_val)

TestD=TestData()
x_test, y_test=GenerateTDataForm(TestD)

x_test = x_test.transpose()
y_test = np.array(y_test).reshape(1, len(y_test))

#print("x_test=",x_test)
#print("y_test=",y_test)

#print(Data)

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def sigmoid(z):
    return 1. /(1 + np.exp(-z))

def tanh(x):
    ex = np.round(np.exp(x),4)
    enx = np.round(np.exp(-x),4)
    return (ex-enx)/(ex+enx)

def affine (W, X, B):
    return np.dot(W.T, X) + B

def init_random_parameters (num_layer = 1):

    W1 = np.round(np.random.rand(2,num_layer),4)
    B1 = np.round(np.random.random((1,1)),4)
    #B1 = np.round(np.zeros((1, 1)), 4)

    return W1, B1

# W1, B1 =init_random_parameters ()
# Z1 = affine(W1, x_train,B1)
# y_hat=tanh(Z1)

#print(f"X_train.shape: {x_train}")
#plt.plot(x_train.transpose())
#plt.show()
#print(Z1)

#print("After Activation function")
#print(y_hat)
#print()
#print("length of After Activation function")
#for i in y_hat:
#    print(len(i))

def loss_eval_Activation(_params):  # sigmoid
    W1, B1 = _params
    # Forward: input Layer
    Z1 = np.round(affine(W1, x_train, B1), 4)

    y_hat = np.round(sigmoid(Z1), 4)

    # cross entropy
    loss = np.round((1. / x_train.shape[1]) * np.round(np.sum(-1 * (y_train * np.round(np.log(y_hat),4) + (1 - y_train) * np.round(np.log(1 - y_hat),4))),4),4)

    return Z1, y_hat, loss


def get_gradients_Activation(_params):
    W1, B1 = _params
    Z1, y_hat, loss = loss_eval_Activation([W1, B1])

    err=y_hat-y_train
    dZ = err*(1-err)

    dW=np.dot(x_train, dZ.T)

    dB=1./x_train.shape[0] * np.sum(dZ ,axis=1, keepdims=True)
    #print(dB)

    return [dW, dB], loss


def optimize_tanh(_params, learning_rate=0.1, iteration=1000, sample_size=0):
    params = np.copy(_params)
    loss_trace = []

    for epoch in range(iteration):
        dparams, loss = get_gradients_Activation(params)
        for param, dparam in zip(params, dparams):
            param += - learning_rate * dparam


        if (epoch % 100 == 0):
            loss_trace.append(loss)

    _, Y_hat_predict, _ = loss_eval_Activation(params)

    #print(Y_hat_predict)
    return params, loss_trace, Y_hat_predict


params = init_random_parameters(1)
new_params, loss_trace, Y_hat_predict = optimize_tanh(params, 0.1, 5000)
print(f"new_params:\n{new_params}\nloss:\n{loss_trace}\nY_hat:")
print(Y_hat_predict)
print(loss_trace[-1])
# Plot learning curve (with costs)
plt.plot(loss_trace)
plt.ylabel('loss')
plt.xlabel('iterations (per hundreds)')
plt.show()