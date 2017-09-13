from math import exp
from random import uniform

# Get matrixes 'wh' and 'wo' filled with random values between -1 and 1
def _generateRandomWeights(n, l, m):
  return ([[uniform(-1, 1) for j in range(n)] for i in range(l)],
    [[uniform(-1, 1) for j in range(l)] for i in range(m)])

# Calculate a net given its inputs, weights and length
def _getNet(inputs, weights, length):
  return sum([inputs[it] * weights[it] for it in range(length)])

# Get 'net h'
def _getNeth(x, wh, n, p, j):
  return _getNet(x[p], wh[j], n)

# Get 'net o'
def _getNeto(yh, wo, l, k):
  return _getNet(yh, wo[k], l)

# Calculate 'delta o'
def _getDeltao(d, y, k, p):
  return (d[p][k] - y[k]) * y[k] * (1 - y[k])

# Calculate 'delta h'
def _getDeltah(yh, deltao, wo, m, j):
  return yh[j] * (1 - yh[j]) * sum([deltao[k] * wo[k][j] for k in range(m)])

# Returns an adjusted matrix of weights given alpha, deltas, inputs and weights
def _adjustWeights(alpha, deltas, inputs, weights, inputsLength, outputsLength):
  return [[weights[it2][it1] + (alpha * deltas[it2] * inputs[it1])
    for it1 in range(inputsLength)] for it2 in range(outputsLength)]

# Adjust 'w o'
def _adjustWo(alpha, deltao, yh, m, l, wo):
  return _adjustWeights(alpha, deltao, yh, wo, l, m)

# Adjust 'w h'
def _adjustWh(alpha, deltah, x, l, n, p, wh):
  return _adjustWeights(alpha, deltah, x[p], wh, n, l)

# Calculate the error of a learning pattern given its current 'delta o'
def _getError(deltao, m):
  return sum([deltao[k] ** 2 for k in range(m)]) / 2

# Calculate the activation function of a neuron given its net
def _activationFunction(net):
  return 1 / (1 + exp(net * -1))

# Calculate the 'y h' of a learning pattern given its inputs and weights
def _getYh(x, wh, n, p, l):
  return [_activationFunction(_getNeth(x, wh, n, p, j)) for j in range(l)]

# Calculate the 'y' of a learning pattern, can round with rnd
def _getY(yh, wo, l, m, rnd = False):
  y = [_activationFunction(_getNeto(yh, wo, l, k)) for k in range(m)]
  return y if not rnd else [int(round(v)) for v in y]

# Calculate the correct weigths to pass all learning patterns
def learningProcess(x, d, alpha, maxError):
  n = len(x[0])
  m = len(d[0])
  l = n * m
  (wh, wo) = _generateRandomWeights(n, l, m)

  error = True
  while error:
    error = False
    for p in range(len(x)):
      yh = _getYh(x, wh, n, p, l)
      deltao = [_getDeltao(d, _getY(yh, wo, l, m), k, p) for k in range(m)]

      if _getError(deltao, m) > maxError:
        deltah = [_getDeltah(yh, deltao, wo, m, j) for j in range(l)]
        wo = _adjustWo(alpha, deltao, yh, m, l, wo)
        wh = _adjustWh(alpha, deltah, x, l, n, p, wh)

        error = True

  return (n, m, l, wh, wo)

# Return the values in 'x2' and 'y2' in a string format of matrix
def _toString(x2, y2):
  return [' '.join([str(int(b)) for b in x2[p]]) +
    ' | ' + ' '.join([str(v) for v in r]) for p, r in zip(range(len(x2)), y2)]

# Calculate 'y2' given all params, can round and stringify
def getY2(x2, n, m, l, wh, wo, rnd = False, toStr = False):
  y2 = [_getY(_getYh(x2, wh, n, p, l), wo, l, m, rnd) for p in range(len(x2))]
  return _toString(x2, y2) if toStr else y2
