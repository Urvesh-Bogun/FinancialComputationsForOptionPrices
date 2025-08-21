import math
from scipy.stats import norm

X1 = 120
X2 = 88
S0 = 80
sigma = 0.48
r = 0.07
T = 0.5

def calculateD1(S0, X, sigma, r, T):
    return (math.log(S0/X) + (r + ((sigma ** 2)/ 2)) * T) / (sigma * (math.sqrt(T)))

def calculateD2(d1, sigma, T):
    return d1 - (sigma * math.sqrt(T))

def calculateCallOptionPrice(S0, X, r, T, d1, d2):
    return (S0 * norm.cdf(d1)) - ((X * math.exp(-r * T)) * norm.cdf(d2))

def calculatePutOptionPrice(S0, X, r, T, d1, d2):
    return (X * math.exp(-r * T) * norm.cdf(-d2)) - (S0 * norm.cdf(-d1))

def calculateOptionPrice(S0, X, sigma, r, T, isCall):
    d1 = calculateD1(S0, X, sigma, r, T)
    d2 = calculateD2(d1, sigma, T)

    if (isCall):
        return calculateCallOptionPrice(S0, X, r, T, d1, d2)
    else:
        return calculatePutOptionPrice(S0, X, r, T, d1, d2)

if __name__ == "__main__":
    print(f"Call (X = 120): { calculateOptionPrice(S0, X1, sigma, r, T, isCall = True) } ")
    print(f"Put (X = 120): { calculateOptionPrice(S0, X1, sigma, r, T, isCall = False) } ")

    print(f"Call (X = 88): { calculateOptionPrice(S0, X2, sigma, r, T, isCall = True) } ")
    print(f"Put (X = 88): { calculateOptionPrice(S0, X2, sigma, r, T, isCall = False) } ")