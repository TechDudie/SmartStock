from decimal import Decimal, getcontext

import matplotlib.pyplot as plt
import numpy as np
from numpy import transpose
from numpy.linalg import inv

getcontext().prec = 50

x_axis = np.array([0, 0.5, 1, 1.5, 2, 2.3, 2.7, 3, 3.3, 3.6, 4, 4.7, 5, 5.5, 6, 6.5, 6.8, 7, 7.4, 7.8, 7.9, 8, 8.2, 8.5, 8.9, 9, 9.4, 9.8, 10]) # type: ignore
y_axis = np.array([0, 0.25, 0.5, 0.75, 1, 0.8, 1.2, 1, 2, 3, 2.6, 2.25, 2.5, 3, 3.4, 4, 4.3, 4.2, 4, 3.9, 4, 4.5, 5, 4.6, 4.25, 5, 5.6, 6.2, 6.1]) # type: ignore

def polynomial(x_axis, y_axis, power):
    """
    Calculates a polynomial approximation from a list of points and a given polynomal degree.

    Parameters:
        x_axis (list): A list of x-values
        y_axis (list): A list of y-values

    Returns:
        coefficients (list): A list of polynomial coefficients, in descending order
    """
    x = np.empty((len(x_axis), power + 1))
    for i, j in enumerate(x):
        for j in range(power + 1):
            x[i, j] = x_axis[i] ** j
    xt = transpose(x)
    b = np.dot(np.dot(inv(np.dot(xt, x)), xt), y_axis)
    x = 0
    for i in b:
        b[x] = Decimal(str(i))
        x += 1
    coefficients = b[::-1]
    return coefficients

def derivative(coefficients):
    """
    Calculates the derative of a list of coefficients.

    Parameters:
        coefficients (list): A list of polynomial coefficients, in descending order

    Returns:
        result (list): The derative of the coefficients
    """
    result = []
    coefficients = coefficients[::-1]
    x = -1
    for i in coefficients:
        x += 1
        if x == 0:
            continue
        result.append(i * x)
    result = result[::-1]
    return result

def peak(y_axis):
    """
    Calculates how many times a graph peaks.

    Parameters:
        y_axis (list): A list of y-values

    Returns:
        counter (int): The amount of times the graph peaks
    """
    state = True
    prev = 0
    counter = 1
    for i in y_axis:
        if state:
            if i < prev:
                counter += 1
                state = False
        else:
            if i > prev:
                counter += 1
                state = True
        prev = i
    return counter // 2

def polyprint(coefficients, desmos=False):
    """
    Prints a list of coefficients in polynomial standard form.

    Parameters:
        coefficients (list): A list of polynomial coefficients, in descending order
        desmos (bool): A flag whether or not to print exponents in Desmos form
    """
    strings = []
    for i in coefficients:
        if not strings:
            if i > 0:
                strings.append('{0:.30f}'.format(abs(i)))
            elif i < 0:
                strings.append("-" + '{0:.30f}'.format(abs(i)))
            continue
        if i > 0:
            strings.append(" + " + '{0:.30f}'.format(abs(i)))
        elif i < 0:
            strings.append(" - " + '{0:.30f}'.format(abs(i)))
    string = "y = "
    x = len(strings)
    for i in strings:
        string += i
        if x > 2:
            string += f"x^{{{x - 1}}}" if desmos else f"x^{x - 1}"
        elif x == 2:
            string += "x"
        else:
            pass
        x -= 1
    print(string)

def polygraph(x, coefficients):
    """
    Graphs a list of coefficients in polynomial standard form.

    Parameters:
        x (int): The x-value
        coefficients (list): A list of polynomial coefficients, in descending order

    Returns:
        y (int): The resulting y-value
    """
    coefficients = coefficients[::-1]
    degree = len(coefficients) - 1
    y = 0
    for i in range(degree + 1):
        y += coefficients[i] * x ** i
    return y

if __name__ == "__main__":
    power = peak(y_axis)
    print(power)
    coeffs = polynomial(x_axis, y_axis, power)
    print(coeffs)
    polyprint(coeffs)
    derivative_1 = derivative(coeffs)
    polyprint(derivative_1)
    derivative_2 = derivative(derivative_1)
    polyprint(derivative_2)

    x_linspace = np.linspace(0, 10, 100)
    plt.scatter(x_axis, y_axis, color="black")
    plt.plot(x_linspace, polygraph(x_linspace, coeffs), color="red")
    plt.plot(x_linspace, polygraph(x_linspace, derivative_1), color="green")
    plt.plot(x_linspace, polygraph(x_linspace, derivative_2), color="blue")
    plt.show()
