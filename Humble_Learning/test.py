import numpy as np

def sigmoid (o):
    return 1./(1+np.exp(-1*o))


def formal(RMS, ANG):


    X1 = -9.89347521 * RMS +16.33257357 * ANG +  2.96626043
    X2 = 4.66725605 * RMS -54.0110004 * ANG -25.43624075;

    H1 = sigmoid(X1);
    H2 = sigmoid(X2);


    A = -7.71454823 * H1 +17.75385267 * H2 -0.00684656;
    print(A)
    Y_hat = sigmoid(A);

    return Y_hat


print(75 * -9.89347521 + 16.33257357 * 120 + 2.9)
