import math

X1 = 120
X2 = 88
S0 = 80
sigma = 0.48
r = 0.07
T = 0.5
timeStep = 182

def calculateDt(T, timeStep):
    return T / timeStep

def calculateU(sigma, dt):
    return math.exp(sigma * (math.sqrt(dt)))

def calculateD(u):
    return 1 / u

def buildStockPriceTree(S0, u, d, N):
    stockPriceTree = [[0 for _ in range(N)] for _ in range(N)]
    stockPriceTree[0][0] = S0

    for i in range(1, N):
        stockPriceTree[i][0] = stockPriceTree[i - 1][0] * d 
        for j in range(1, i + 1):
            stockPriceTree[i][j] = stockPriceTree[i - 1][j - 1] * u

    return stockPriceTree

def calculateP(r, dt, u, d):
    return (math.exp(r * dt) - d) / (u - d)

def calculateF(r, dt, p, fu, fd):
    return math.exp(-r * dt) * (p * fu + (1 - p) * fd)

def calculatePayoff(S, X, isCall):
    if isCall:
        return max(S - X, 0)
    else:
        return max(X - S, 0)

def buildPayoffTree(stockPriceTree, X, u, d, p, isCall, N, dt, isAmerican):
    payoffTree = [[0 for j in range(N)] for i in range(N)]

    for j in range(N):
        payoffTree[N - 1][j] = calculatePayoff(stockPriceTree[N - 1][j], X, isCall)

    for i in range(N - 2, -1, -1):
        for j in range(i + 1):
            fu = payoffTree[i + 1][j + 1]
            fd = payoffTree[i + 1][j]
            payoffTree[i][j] = calculateF(r, dt, p, fu, fd)

            if isAmerican:
                payoffTree[i][j] = max(payoffTree[i][j], calculatePayoff(stockPriceTree[i][j], X, isCall))

    return payoffTree

def calculateOptionPrice(S0, X, isCall, sigma, r, T, timeStep, isAmerican):
    dt = calculateDt(T, timeStep)
    u = calculateU(sigma, dt)
    d = calculateD(u)
    p = calculateP(r, dt, u, d)
    N = timeStep + 1

    stockPriceTree = buildStockPriceTree(S0, u, d, N)
    payoffTree = buildPayoffTree(stockPriceTree, X, u, d, p, isCall, N, dt, isAmerican)

    return payoffTree[0][0]

print(f"European call (X = 120): { calculateOptionPrice(S0, X1, True, sigma, r, T, timeStep, isAmerican=False) } ")
print(f"European put (X = 120): { calculateOptionPrice(S0, X1, False, sigma, r, T, timeStep, isAmerican=False) } ")
print(f"American call (X = 120): { calculateOptionPrice(S0, X1, True, sigma, r, T, timeStep, isAmerican=True) } ")
print(f"American put (X = 120): { calculateOptionPrice(S0, X1, False, sigma, r, T, timeStep, isAmerican=True) } ")

print(f"European call (X = 88): { calculateOptionPrice(S0, X2, True, sigma, r, T, timeStep, isAmerican=False) } ")
print(f"European put (X = 88): { calculateOptionPrice(S0, X2, False, sigma, r, T, timeStep, isAmerican=False) } ")
print(f"American call (X = 88): { calculateOptionPrice(S0, X2, True, sigma, r, T, timeStep, isAmerican=True) } ")
print(f"American put (X = 88): { calculateOptionPrice(S0, X2, False, sigma, r, T, timeStep, isAmerican=True) } ")