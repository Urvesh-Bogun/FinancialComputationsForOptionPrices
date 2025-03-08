import math
from scipy.stats import norm

X1 = 120
X2 = 88
S0 = 80
sigma = 0.48
r = 0.07
T = 0.5
timeStep = 182
numberOfSimulations = 50000

def calculateDt(T, timeStep):
    return T / timeStep

def calculateDiscountFactor(r, T):
    return math.exp(-r * T)

def randomNormal():
    return norm.rvs()

def simululatePath(S0, sigma, r, T, timeStep):
    dt = calculateDt(T, timeStep)
    lnS = math.log(S0)

    for i in range(timeStep):
        epsilon = randomNormal()
        lnS += ((r - ((sigma ** 2) / 2)) * dt) + (sigma * epsilon * math.sqrt(dt))

    return math.exp(lnS)

def calculatePayoff(S, X, isCall):
    if isCall:
        return max(S - X, 0)
    else:
        return max(X - S, 0)
    
def createSample(S0, X, sigma, r, T, timeStep, isCall):
    S = simululatePath(S0, sigma, r, T, timeStep)
    payoff = calculatePayoff(S, X, isCall)
    return payoff

def calculateAveragePayoff(S0, X, sigma, r, T, timeStep, numberOfSimulations, isCall):
    totalPayoff = 0

    for i in range(numberOfSimulations):
        payoff = createSample(S0, X, sigma, r, T, timeStep, isCall)
        totalPayoff += payoff

    averagePayoff = totalPayoff / numberOfSimulations
    return averagePayoff

def calculateOptionPrice(S0, X, sigma, r, T, timeStep, numberOfSimulations, isCall):
    averagePayoff = calculateAveragePayoff(S0, X, sigma, r, T, timeStep, numberOfSimulations, isCall)
    discountFactor = calculateDiscountFactor(r, T)

    return discountFactor * averagePayoff

print(f"Call (X = 120): { calculateOptionPrice(S0, X1, sigma, r, T, timeStep, numberOfSimulations, isCall = True) } ")
print(f"Put (X = 120): { calculateOptionPrice(S0, X1, sigma, r, T, timeStep, numberOfSimulations, isCall = False) } ")

print(f"Call (X = 88): { calculateOptionPrice(S0, X2, sigma, r, T, timeStep, numberOfSimulations, isCall = True) } ")
print(f"Put (X = 88): { calculateOptionPrice(S0, X2, sigma, r, T, timeStep, numberOfSimulations, isCall = False) } ")