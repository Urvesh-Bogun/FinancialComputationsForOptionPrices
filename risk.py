import math, random
from bs import calculateOptionPrice

S0 = 80.0
sigma = 0.48
r = 0.07
T = 0.5
trading_days = 252
dt = 1.0 / trading_days
mu = 0.0
alpha=0.95
numberOfSimulations = 50000
random.seed(16)

# Creating a portfolio of one long call @ 88 and half a short put @ 120
portfolio = [
    (True,  88,  1.0,  T),
    (False, 120, -0.5, T),
]

def calculateTodaysPortfolioValue(S0, sigma, r, portfolio):
    total = 0.0
    for isCall, K, position_quantity, time_left in portfolio:
        price = calculateOptionPrice(S0, K, sigma, r, time_left, isCall)
        total += position_quantity * price
    return total

V0 = calculateTodaysPortfolioValue(S0, sigma, r, portfolio)
print("Portfolio value today:", V0)

# Reduce maturity by theta (one day)
portfolioT1 = [
    (is_call, strike, position_quantity, max(time_left - dt, 0.0))
    for (is_call, strike, position_quantity, time_left) in portfolio
]

def calculateNextDaySpotPrice(S0, sigma, trading_days, mu):
    dt = 1.0 / trading_days
    z  = random.gauss(0, 1)   # ~ N(0,1)
    return S0 * math.exp((mu - 0.5 * (sigma ** 2)) * dt + sigma * math.sqrt(dt) * z)


def tailCount(sample_size, alpha):
    t = int((1 - alpha) * sample_size)
    if t < 1:
        t = 1
    return t

def calculateVaRFromSorted(sorted_pnls, tail_size):
    if tail_size < 1:
        tail_size = 1
    if tail_size > len(sorted_pnls):
        tail_size = len(sorted_pnls)
    cutoff_pnl = sorted_pnls[tail_size - 1]
    return -cutoff_pnl


def calculateESFromSorted(sorted_pnls, tail_size):
    if tail_size < 1:
        tail_size = 1
    if tail_size > len(sorted_pnls):
        tail_size = len(sorted_pnls)
    total = 0.0
    i = 0
    while i < tail_size:
        total += sorted_pnls[i]
        i += 1
    return -(total / tail_size)

def calculateVaRAndESFromPnL(pnl, alpha):
    sorted_pnls = sorted(pnl)
    sample_size = len(sorted_pnls)
    tail_size = tailCount(sample_size, alpha)

    VaR = calculateVaRFromSorted(sorted_pnls, tail_size)
    ES  = calculateESFromSorted(sorted_pnls, tail_size) 
    return VaR, ES


def simulateOneDayPnl(num_paths, S0, sigma, r, mu, trading_days, portfolio_T1, V0):
    pnl = []
    i = 0
    while i < num_paths:
        S1 = calculateNextDaySpotPrice(S0, sigma, trading_days, mu)
        V1 = calculateTodaysPortfolioValue(S1, sigma, r, portfolio_T1)
        pnl.append(V1 - V0)
        i += 1
    return pnl

pnl = simulateOneDayPnl(numberOfSimulations, S0, sigma, r, mu, trading_days, portfolioT1, V0)
VaR95, ES95 = calculateVaRAndESFromPnL(pnl, 0.95)
VaR99, ES99 = calculateVaRAndESFromPnL(pnl, 0.99)
print("VaR99 =", VaR99)
print("ES99 =", ES99)
print("VaR95 =", VaR95)
print("ES95  =", ES95)