from decimal import Decimal

import numpy as np
from numpy import transpose
from numpy.linalg import inv

x_axis = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
y_axis = np.array([20, 17, 10, 2, 2, 0, 1, 2, 9, 15, 25])
power = 3

def polynomial(x_axis, y_axis):
    x = np.empty((len(x_axis), power+1))
    for i, j in enumerate(x):
        for j in range(power + 1): x[i, j] = x_axis[i] ** j
    xt = transpose(x)
    b = np.dot(np.dot(inv(np.dot(xt, x)), xt), y_axis)
    x = 0
    for i in b:
        b[x] = Decimal(str(i))
        x += 1
    coefficients = b[::-1]
    return coefficients

def derivative(coefficients):
    result = []
    coefficients = coefficients[::-1]
    x = -1
    for i in coefficients:
        x += 1
        if x == 0: continue
        result.append(i * x)
    result = result[::-1]
    return result

def polyprint(coefficients):
    strings = []
    for i in coefficients:
        if strings == []:
            if i > 0:
                strings.append(str(i))
            elif i < 0:
                strings.append("-" + str(abs(i)))
            continue
        if i > 0:
            strings.append(" + " + str(i))
        elif i < 0:
            strings.append(" - " + str(abs(i)))
    string = "y = "
    x = len(strings)
    for i in strings:
        string += i
        if x > 2:
            string += f"x^{x - 1}"
        elif x == 2:
            string += "x"
        else:
            pass
        x -= 1
    print(string)

coefficients = polynomial(x_axis, y_axis)
polyprint(coefficients)
derivative_1 = derivative(coefficients)
polyprint(derivative_1)
derivative_2 = derivative(derivative_1)
polyprint(derivative_2)
