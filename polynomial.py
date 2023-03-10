from decimal import Decimal, getcontext
from datetime import datetime
import math
import socket
import sys
import numpy as np
from numpy import transpose
from numpy.linalg import inv
import matplotlib.pyplot as plt
from pandas_datareader import data as reader
import pytz
import yfinance as yf

def log(message, level="INFO"):
    now = datetime.now().strftime("[%H:%M:%S]")
    print(f"{now} [{level}] {message}")

time = lambda: (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000

ticker = "MSFT"
desmos = False
polynomialize = False
getcontext().prec = 50
yf.pdr_override()

log("Modules imported and initialized")

if len(sys.argv) > 1:
    ticker = sys.argv[1]
    log(f"Ticker set. Target: {ticker}")
else:
    log("Ticker not specified. Defaulting to 'MSFT'", level="WARN")

if len(sys.argv) > 2:
    desmos = True
    log("Desmos mode enabled. Polynomial exponents will be printed in Desmos format")
else:
    log("Desmos mode disabled. Polynomial exponents will be printed with a caret")

if len(sys.argv) > 3:
    polynomialize = True
    log("Equation will be approximated with a polynomial")
else:
    log("Equation will not be polynomialized; it cannot be represented by a function")

try:
    socket.setdefaulttimeout(3)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
except socket.error:
    log("No internet. Please connect to internet, and try again.", level="ERROR")
    exit()

now = datetime.now(pytz.timezone('US/Eastern'))
if (now.hour == 9 and now.minute >= 30) or (now.hour > 9 and now.hour <= 16):
    log(f"Stock market open. Eastern time is {now.strftime('%H:%M:%S')}")
else:
    log("Stock market is closed. Retreiving most recent values.", level="WARN")

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

def differenciate(values):
    """
    Calculates the differences of a list of values.

    Parameters:
        values (list): A list of values

    Returns:
        result (list): The differences of the values
    """
    result = []
    prev = None
    for i in values:
        if i is None or prev is None:
            result.append(None)
            prev = i
            continue
        result.append(i - prev)
        prev = i
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

def degree(y_axis):
    """
    Calculates the optimal polynomial degree from a set of points.

    Parameters:
        y_axis (list): A list of y-values

    Returns:
        degree (int): The optimal degree.
    """
    # I'll be honest, I just made this random algoritiom up.
    return math.floor(math.e * math.log(len(y_axis)))

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
                strings.append("{0:.5f}".format(abs(i)))
            elif i < 0:
                strings.append("-{0:.5f}".format(abs(i)))
            continue
        if i > 0:
            strings.append(" + {0:.5f}".format(abs(i)))
        elif i < 0:
            strings.append(" - {0:.5f}".format(abs(i)))
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
    log(string)

def polygraph(x, coefficients):
    """
    Graphs a list of coefficients in polynomial standard form.

    Parameters:
        x (int): The x-value
        coefficients (list): A list of polynomial coefficients, in descending order

    Returns:
        y (float): The resulting y-value
    """
    coefficients = coefficients[::-1]
    degree = len(coefficients) - 1
    y = 0
    for i in range(degree + 1):
        y += coefficients[i] * x ** i
    return y

ms = time()

# Download the stock data from Yahoo Finance
log("Downloading stock data...")
data = list(reader.get_data_yahoo(ticker, period="1d", interval="1m")["Close"])
x_axis = []
y_axis = []
for x, y in enumerate(data):
    x_axis.append(x)
    y_axis.append(y)

log(str(data) if polynomialize else f"{str(data)[:80]}...")

if polynomialize:
    log("Approximating polynomial...")
    log(f"Degree: {degree(y_axis)}")
    coeffs = polynomial(x_axis, y_axis, degree(y_axis)) # Calculate the polynomial approximation from the given list of points
    log(str(coeffs))
    polyprint(coeffs, desmos=desmos)
    log("Calculating first derivative...")
    derivative_1 = derivative(coeffs) # Calculate the first derivative
    polyprint(derivative_1, desmos=desmos)
    log("Calculating second derivative...")
    derivative_2 = derivative(derivative_1) # Calculate the second derivative
    polyprint(derivative_2, desmos=desmos)

    # Graph the equations
    log("Graphing equations...")
    x_linspace = np.linspace(0, len(y_axis) - 1, len(y_axis) * 10 - 10)
    plt.scatter(x_axis, y_axis, color="black")
    plt.plot(x_linspace, polygraph(x_linspace, coeffs), "r")
    plt.plot(x_linspace, polygraph(x_linspace, derivative_1), "g")
    plt.plot(x_linspace, polygraph(x_linspace, derivative_2), "b")
else:
    log("Calculating first difference...")
    diff_1 = differenciate(y_axis) # Calculate the first difference
    log(f"{str(diff_1)[:80]}...")
    log("Calculating second difference...")
    diff_2 = differenciate(diff_1) # Calculate the second difference
    log(f"{str(diff_2)[:80]}...")

    plt.plot(x_axis, y_axis, '-r')
    plt.plot(x_axis[1:], diff_1[1:], '-g')
    plt.plot(x_axis[2:], diff_2[2:], '-b')

log(f"Done in {math.floor(time() - ms)} ms.")
plt.show()

