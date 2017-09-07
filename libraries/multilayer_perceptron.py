from math import exp
from random import uniform

# Get matrixes 'wh' and 'wo' filled with random values between -1 and 1
def generateRandomWeights(n, l, m):
  return ([[uniform(-1, 1) for j in range(n)] for i in range(l)],
    [[uniform(-1, 1) for j in range(l)] for i in range(m)])

# Calculate a net given its inputs, weights and length
def getNet(inputs, weights, length):
  return sum([inputs[it] * weights[it] for it in range(length)])

# Get 'net h'
def getNeth(x, wh, n, p, j):
  return getNet(x[p], wh[j], n)

# Get 'net o'
def getNeto(yh, wo, l, k):
  return getNet(yh, wo[k], l)

# Calculate 'delta o'
def getDeltao(d, y, k, p):
  return (d[p][k] - y[k]) * y[k] * (1 - y[k])

# Calculate 'delta h'
def getDeltah(yh, deltao, wo, m, j):
  return yh[j] * (1 - yh[j]) * sum([deltao[k] * wo[k][j] for k in range(m)])

# Returns an adjusted matrix of weights given alpha, deltas, inputs and weights
def adjustWeights(alpha, deltas, inputs, weights, inputsLength, outputsLength):
  return [[weights[it2][it1] + (alpha * deltas[it2] * inputs[it1])
    for it1 in range(inputsLength)] for it2 in range(outputsLength)]

# Adjust 'w o'
def adjustWo(alpha, deltao, yh, m, l, wo):
  return adjustWeights(alpha, deltao, yh, wo, l, m)

# Adjust 'w h'
def adjustWh(alpha, deltah, x, l, n, p, wh):
  return adjustWeights(alpha, deltah, x[p], wh, n, l)

# Calculate the error of a learning pattern given its current 'delta o'
def getError(deltao, m):
  return sum([deltao[k] ** 2 for k in range(m)]) / 2

# Calculate the activation function of a neuron given its net
def activationFunction(net):
  return 1 / (1 + exp(net * -1))

# Calculate the 'y h' of a learning pattern given its inputs and weights
def getYh(x, wh, n, p, l):
  return [activationFunction(getNeth(x, wh, n, p, j)) for j in range(l)]

# Calculate the 'y' of a learning pattern given its 'y h' and weights
def getY(yh, wo, l, m):
  return [activationFunction(getNeto(yh, wo, l, k)) for k in range(m)]

# Calculate the correct weigths to pass all learning patterns
def learningProcess(x, d, wh, wo, n, l, m, alpha, maxError):
  n = len(x[0])
  m = len(d[0])
  l = n * m
  (wh, wo) = generateRandomWeights(n, l, m)

  error = True
  while error:
    error = False
    for p in range(len(x)):
      yh = getYh(x, wh, n, p, l)
      deltao = [getDeltao(d, getY(yh, wo, l, m), k, p) for k in range(m)]

      if getError(deltao, m) > maxError:
        deltah = [getDeltah(yh, deltao, wo, m, j) for j in range(l)]
        wo = adjustWo(alpha, deltao, yh, m, l, wo)
        wh = adjustWh(alpha, deltah, x, l, n, p, wh)

        error = True

  return (n, m, l, wh, wo)

# Return the values in 'x2' and 'y2' in a string format of matrix
def toString(x2, y2):
  return [' '.join([str(int(b)) for b in x2[p]]) +
    ' | ' + ' '.join([str(v) for v in r]) for p, r in zip(range(len(x2)), y2)]

# Calculate 'y2' given 'x2', 'wh', 'wo' and all the lengths
def getY2(x2, n, m, l, wh, wo, string = False):
  y2 = [getY(getYh(x2, wh, n, p, l), wo, l, m) for p in range(len(x2))]
  return toString(x2, y2) if string else y2
