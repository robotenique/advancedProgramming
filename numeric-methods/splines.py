# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import functools

###############################################################################
#
# spline = a cubic b spline with equally spaced nodes
#
###############################################################################

class spline:

# spline with support in [x_min,x_max] and n >= 10 weights,
# which correspond to n - 3 intervals

    def __init__(self, weights, x_min = 0, x_max = 1):
      assert x_max > x_min, 'x_max must be greater than x_min'
      assert type(weights) == np.ndarray, 'weight must be a numpy array'
      assert len(weights) >= 10, 'there must be at least 10 weights'
      dx = x_max - x_min
      self.n = len(weights) - 3
      self.scale = self.n/dx
      self.x_min = x_min
      self.x_max = x_max
      self.weights = weights

    def locate(self, t):
      if t <= self.x_min:
        return [0.0, 0]

      if t >= self.x_max:
        return [1.0, self.n - 1]

      dt = self.scale * (t - self.x_min)

      if dt >= self.n:
        dt = 1.0
        return [1.0, self.n - 1]

      bin = int(np.floor(dt))
      dt -= bin
      return [dt,bin]


    def piece_0_0(self, x):
      return  240 - x * (720 - x * (720 - x * 240))

    def piece_1_0(self, x):
      return x * (720 - x * (1080 - x * 420))

    def piece_1_1(self,x):
      return 60 - x * (180 - x * (180 - x * 60))

    def piece_2_0(self,x):
      return x * x * (360 - 220 * x)

    def piece_2_1(self,x):
      return 140 + x * (60 - x * (300 - x * 140))

    def piece_2_2(self,x):
      return 40 - x * (120 - x * (120 - x * 40))

    def piece_3_0(self,x):
      return 40  * x * x * x

    def piece_3_1(self,x):
      return 40 + x * (120 + x * (120 - x * 120))

    def piece_3_2(self,x):
      return 160 - x * x * (240 - x * 120)

    def piece_3_3(self,x):
      return 40 - x * (120 - x * (120 - x * 40))

    def piece_4_1(self,x):
      return  40 * x * x * x

    def piece_4_2(self,x):
      return 40 + x * (120 + x * (120 - x * 140))

    def piece_4_3(self,x):
      return 140 - x * (60 + x * (300 - x * 220))

    def piece_5_2(self,x):
      return 60 * x * x * x

    def piece_5_3(self,x):
      return 60 + x * (180 + x * (180 - x * 420))

    def piece_6_3(self,x):
      return 240  * x * x * x

    def eval(self,x):
      dt, bin = self.locate(x)
      if bin <= 2:
        if bin <= 0:
          a = self.piece_0_0(dt) * self.weights[0] + self.piece_1_0(dt) * self.weights[1]
          return a + self.piece_2_0(dt) * self.weights[2] + self.piece_3_0(dt) * self.weights[3]
#
        if bin == 1:
          a = self.piece_1_1(dt) * self.weights[1] + self.piece_2_1(dt) * self.weights[2]
          return a + self.piece_3_1(dt) * self.weights[3] + self.piece_3_0(dt) * self.weights[4]
        else: # bin = 2
          a = self.piece_2_2(dt) * self.weights[2] + self.piece_3_2(dt) * self.weights[3]
          return a + self.piece_3_1(dt) * self.weights[4] + self.piece_3_0(dt) * self.weights[5]

      # now bin > 2
      nw = len(self.weights)
      if bin >= nw - 6:
        if bin == nw - 6:
          a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
          return a + self.piece_3_1(dt) * self.weights[bin + 2] + self.piece_4_1(dt) * self.weights[bin + 3]

        if bin == nw - 5:
          a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
          return a + self.piece_4_2(dt) * self.weights[bin + 2] + self.piece_5_2(dt) * self.weights[bin + 3]

        # now bin = nw - 4
        a = self.piece_3_3(dt) * self.weights[bin] + self.piece_4_3(dt) * self.weights[bin + 1]
        return a + self.piece_5_3(dt) * self.weights[bin + 2] + self.piece_6_3(dt) * self.weights[bin + 3]

    # finally, the normal case 3 <= bin < nw - 6
      a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
      return a +  self.piece_3_1(dt) * self.weights[bin + 2] + self.piece_3_0(dt) * self.weights[bin + 3]

    def eval_beta_j(self, j, x):

      dt, bin = self.locate(x)

      if ((j < bin) or (j > bin + 3)):
        return 0

      if bin <= 2:
        if bin <= 0:
          if j < 2:
            if j == 1:
              return self.piece_1_0(dt)
            else:
              return self.piece_0_0(dt)
          else:
            if j == 2:
              return self.piece_2_0(dt)
            else:
              return self.piece_3_0(dt)
#
        if bin == 1:
          if j < 3:
            if j == 1:
              return self.piece_1_1(dt)
            else:
              return self.piece_2_1(dt)
          else:
            if j == 3:
              return self.piece_3_1(dt)
            else:
              return self.piece_3_0(dt)
        else: # bin = 2
          if (j < 4):
            if (j == 2):
              return self.piece_2_2(dt)
            else:
              return self.piece_3_2(dt)
          else:
            if (j == 4):
              return self.piece_3_1(dt)
            else:
              return self.piece_3_0(dt)

      # now bin > 2
      nw = len(self.weights)
      if bin >= nw - 6:
        if bin == nw - 6:
          if j < bin + 2:
            if j == bin:
              return self.piece_3_3(dt)
            else:
              return self.piece_3_2(dt)
          else:
            if j == bin + 2:
              return self.piece_3_1(dt)
            else:
              return self.piece_4_1(dt)

        if bin == nw - 5:
          if j < bin + 2:
            if j == bin:
              return self.piece_3_3(dt)
            else:
              return self.piece_3_2(dt)
          else:
            if j == bin + 2:
              return self.piece_4_2(dt)
            else:
              return self.piece_5_2(dt)

        # now bin = nw - 4
        if j < bin + 2:
          if j == bin:
            return self.piece_3_3(dt)
          else:
            return self.piece_4_3(dt)
        else:
          if j == bin + 2:
            return self.piece_5_3(dt)
          else:
            return self.piece_6_3(dt)

    # finally, the normal case 3 <= bin < nw - 6

      if j < bin + 2:
        if j == bin:
          return self.piece_3_3(dt)
        else:
          return self.piece_3_2(dt)
      else:
        if j == bin + 2:
          return self.piece_3_1(dt)
        else:
          return self.piece_3_0(dt)

    def beta_j(self, j, x):
      if type(x) == np.ndarray:
        y = x.copy()
        for i in range(len(x)):
          y[i] = self.eval_beta_j(j,x[i])
        return y
      else:
        return self.eval_beta_j(j,x)


    def __call__(self, x):
      if type(x) == np.ndarray:
        y = x.copy()
        for i in range(len(x)):
          y[i] = self.eval(x[i])
        return y
      else:
        return self.eval(x)

###############################################################################
#
# d_spline = the derivative of the previous spline
#
###############################################################################

class d_spline:

# the derivative of an spline with support in [x_min,x_max] and n >= 10 intervals
# which correspond to n -3 intervals

    def __init__(self, weights, x_min = 0, x_max = 1):
      assert x_max > x_min, 'x_max must be greater than x_min'
      assert type(weights) == np.ndarray, 'weight must be a numpy array'
      assert len(weights) >= 10, 'there must be at least 10 weights'
      dx = x_max - x_min
      self.n = len(weights) - 3
      self.scale = self.n/dx
      self.x_min = x_min
      self.x_max = x_max
      self.weights = weights

    def locate(self, t):
      if t <= self.x_min:
        return [0.0, 0]

      if t >= self.x_max:
        return [1.0, self.n - 1]

      dt = self.scale * (t - self.x_min)

      if dt >= self.n:
        dt = 1.0
        return [1.0, self.n - 1]

      bin = int(np.floor(dt))
      dt -= bin
      return [dt,bin]

    def piece_0_0(self, x):
      return -720 + x * (1440 - x * 720)

    def piece_1_0(self, x):
      return 720 - x * (2160 - x * 1260)

    def piece_1_1(self,x):
      return (-180 + x * (360 - x * 180))

    def piece_2_0(self,x):
      return x * (720 - 660 * x)

    def piece_2_1(self,x):
      return 60 - x * (600 - x * 420)

    def piece_2_2(self,x):
      return -120 + x * (240 - x * 120)

    def piece_3_0(self,x):
      return 120 * x * x;

    def piece_3_1(self,x):
      return 120 + x * (240 - x * 360)

    def piece_3_2(self,x):
      return x * (-480 + x * 360)

    def piece_3_3(self,x):
      return -120 + x * (240 - x * 120)

    def piece_4_1(self,x):
      return 120 * x * x

    def piece_4_2(self,x):
      return 120 + x * (240 - x * 420)

    def piece_4_3(self,x):
      return  -60 - x * (600 - x * 660)

    def piece_5_2(self,x):
      return 180 * x * x

    def piece_5_3(self,x):
      return 180 + x * (360 - x * 1260)

    def piece_6_3(self,x):
      return 720  * x * x;

    def eval(self,x):
      dt, bin = self.locate(x)
      if bin <= 2:
        if bin <= 0:
          a = self.piece_0_0(dt) * self.weights[0] + self.piece_1_0(dt) * self.weights[1]
          return a + self.piece_2_0(dt) * self.weights[2] + self.piece_3_0(dt) * self.weights[3]
#
        if bin == 1:
          a = self.piece_1_1(dt) * self.weights[1] + self.piece_2_1(dt) * self.weights[2]
          return a + self.piece_3_1(dt) * self.weights[3] + self.piece_3_0(dt) * self.weights[4]
        else: # bin = 2
          a = self.piece_2_2(dt) * self.weights[2] + self.piece_3_2(dt) * self.weights[3]
          return a + self.piece_3_1(dt) * self.weights[4] + self.piece_3_0(dt) * self.weights[5]

      # now bin > 2
      nw = len(self.weights)
      if bin >= nw - 6:
        if bin == nw - 6:
          a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
          return a + self.piece_3_1(dt) * self.weights[bin + 2] + self.piece_4_1(dt) * self.weights[bin + 3]

        if bin == nw - 5:
          a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
          return a + self.piece_4_2(dt) * self.weights[bin + 2] + self.piece_5_2(dt) * self.weights[bin + 3]

        # now bin = nw - 4
        a = self.piece_3_3(dt) * self.weights[bin] + self.piece_4_3(dt) * self.weights[bin + 1]
        return a + self.piece_5_3(dt) * self.weights[bin + 2] + self.piece_6_3(dt) * self.weights[bin + 3]

    # finally, the normal case 3 < bin < nw - 6
      a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
      return a +  self.piece_3_1(dt) * self.weights[bin + 2] + self.piece_3_0(dt) * self.weights[bin + 3]

    def __call__(self, x):
      if type(x) == np.ndarray:
        y = x.copy()
        for i in range(len(x)):
          y[i] = self.eval(x[i])
        return y
      else:
        return self.eval(x)

###############################################################################
#
# d2_spline = the second derivative of the previous spline
#
###############################################################################

class d2_spline:

# the derivative of an spline with support in [x_min,x_max] and n >= 10 weights,
# which correspond to n - 3 intervals

    def __init__(self, weights, x_min = 0, x_max = 1):
      assert x_max > x_min, 'x_max must be greater than x_min'
      assert type(weights) == np.ndarray, 'weight must be a numpy array'
      assert len(weights) >= 10, 'there must be at least 10 weights'
      dx = x_max - x_min
      self.n = len(weights) - 3
      self.scale = self.n/dx
      self.x_min = x_min
      self.x_max = x_max
      self.weights = weights

    def locate(self, t):
      if t <= self.x_min:
        return [0.0, 0]

      if t >= self.x_max:
        return [1.0, self.n - 1]

      dt = self.scale * (t - self.x_min)

      if dt >= self.n:
        dt = 1.0
        return [1.0, self.n - 1]

      bin = int(np.floor(dt))
      dt -= bin
      return [dt,bin]

    def piece_0_0(self, x):
      return 1440 - x * 1440

    def piece_1_0(self, x):
      return -2160 + x * 2520

    def piece_1_1(self,x):
      return 360 - x * 360

    def piece_2_0(self,x):
      return 720 - x * 1320

    def piece_2_1(self,x):
      return -600 + x * 840

    def piece_2_2(self,x):
      return 240 - x * 240

    def piece_3_0(self,x):
      return 240 * x

    def piece_3_1(self,x):
      return 240 - x * 720

    def piece_3_2(self,x):
      return -480 + x * 720

    def piece_3_3(self,x):
      return 240 - x * 240

    def piece_4_1(self,x):
      return 240 * x

    def piece_4_2(self,x):
      return 240 - x * 840

    def piece_4_3(self,x):
      return -600 + x * 1320

    def piece_5_2(self,x):
      return 360 * x

    def piece_5_3(self,x):
      return 360 - x * 2520

    def piece_6_3(self,x):
      return 1440 * x

    def eval(self,x):
      dt, bin = self.locate(x)
      if bin <= 2:
        if bin <= 0:
          a = self.piece_0_0(dt) * self.weights[0] + self.piece_1_0(dt) * self.weights[1]
          return a + self.piece_2_0(dt) * self.weights[2] + self.piece_3_0(dt) * self.weights[3]

        if bin == 1:
          a = self.piece_1_1(dt) * self.weights[1] + self.piece_2_1(dt) * self.weights[2]
          return a + self.piece_3_1(dt) * self.weights[3] + self.piece_3_0(dt) * self.weights[4]
        else: # bin = 2
          a = self.piece_2_2(dt) * self.weights[2] + self.piece_3_2(dt) * self.weights[3]
          return a + self.piece_3_1(dt) * self.weights[4] + self.piece_3_0(dt) * self.weights[5]

      # now bin > 2
      nw = len(self.weights)
      if bin >= nw - 6:
        if bin == nw - 6:
          a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
          return a + self.piece_3_1(dt) * self.weights[bin + 2] + self.piece_4_1(dt) * self.weights[bin + 3]

        if bin == nw - 5:
          a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
          return a + self.piece_4_2(dt) * self.weights[bin + 2] + self.piece_5_2(dt) * self.weights[bin + 3]

        # now bin = nw - 4
        a = self.piece_3_3(dt) * self.weights[bin] + self.piece_4_3(dt) * self.weights[bin + 1]
        return a + self.piece_5_3(dt) * self.weights[bin + 2] + self.piece_6_3(dt) * self.weights[bin + 3]

    # finally, the normal case 3 < bin < nw - 6
      a = self.piece_3_3(dt) * self.weights[bin] + self.piece_3_2(dt) * self.weights[bin + 1]
      return a +  self.piece_3_1(dt) * self.weights[bin + 2] + self.piece_3_0(dt) * self.weights[bin + 3]

    def eval_beta_j(self, j, x):

      dt, bin = self.locate(x)

      if ((j < bin) or (j > bin + 3)):
        return 0

      if bin <= 2:
        if bin <= 0:
          if j < 2:
            if j == 1:
              return self.piece_1_0(dt)
            else:
              return self.piece_0_0(dt)
          else:
            if j == 2:
              return self.piece_2_0(dt)
            else:
              return self.piece_3_0(dt)
#
        if bin == 1:
          if j < 3:
            if j == 1:
              return self.piece_1_1(dt)
            else:
              return self.piece_2_1(dt)
          else:
            if j == 3:
              return self.piece_3_1(dt)
            else:
              return self.piece_3_0(dt)
        else: # bin = 2
          if (j < 4):
            if (j == 2):
              return self.piece_2_2(dt)
            else:
              return self.piece_3_2(dt)
          else:
            if (j == 4):
              return self.piece_3_1(dt)
            else:
              return self.piece_3_0(dt)

      # now bin > 2
      nw = len(self.weights)
      if bin >= nw - 6:
        if bin == nw - 6:
          if j < bin + 2:
            if j == bin:
              return self.piece_3_3(dt)
            else:
              return self.piece_3_2(dt)
          else:
            if j == bin + 2:
              return self.piece_3_1(dt)
            else:
              return self.piece_4_1(dt)

        if bin == nw - 5:
          if j < bin + 2:
            if j == bin:
              return self.piece_3_3(dt)
            else:
              return self.piece_3_2(dt)
          else:
            if j == bin + 2:
              return self.piece_4_2(dt)
            else:
              return self.piece_5_2(dt)

        # now bin = nw - 4
        if j < bin + 2:
          if j == bin:
            return self.piece_3_3(dt)
          else:
            return self.piece_4_3(dt)
        else:
          if j == bin + 2:
            return self.piece_5_3(dt)
          else:
            return self.piece_6_3(dt)

    # finally, the normal case 3 <= bin < nw - 6

      if j < bin + 2:
        if j == bin:
          return self.piece_3_3(dt)
        else:
          return self.piece_3_2(dt)
      else:
        if j == bin + 2:
          return self.piece_3_1(dt)
        else:
          return self.piece_3_0(dt)

    def beta_j(self, j, x):
      if type(x) == np.ndarray:
        y = x.copy()
        for i in range(len(x)):
          y[i] = self.eval_beta_j(j,x[i])
        return y
      else:
        return self.eval_beta_j(j,x)


    def __call__(self, x):
      if type(x) == np.ndarray:
        y = x.copy()
        for i in range(len(x)):
          y[i] = self.eval(x[i])
        return y
      else:
        return self.eval(x)

# use  '%matplotlib qt' for plotting on external window

#plotting a 3d curve

def curve(t, spx, spy, spz):
  fig = plt.figure()
  ax = fig.gca(projection='3d')
  ax.plot(spx(t), spy(t), spz(t))
  ax.legend()
  plt.show()

# Computing the matrix m2 = integral of the square of the second derivative
# The function we are integrating is quadratic, and Simpson's rule is
# exact in this case

def simpson_fg(f, g, a, b, n):
  assert n % 2 == 0, 'the number of points must be even'

  h = (b - a) / n
  s = f(a) * g(a) + f(b) * g(b)

  for i in range(1, n, 2):
      fi = f(a + i * h)
      gi = g(a + i * h)
      s += 4 * fi * gi

  for i in range(2, n-1, 2):
      fi = f(a + i * h)
      gi = g(a + i * h)
      s += 2 * fi * gi

  return s * h / 3

# n is the number of weights, and the spline is sum_(i = 0)^(n-1) aj beta_j

def matrix_m2(n):
  na = 12
  w = np.random.rand(na)
  d2s = d2_spline(w, 0, na - 3)
  a = np.zeros(shape=(na,na))
  i = 0
  while i < na:
    j = i
    bind_i = lambda z : d2s.beta_j(i,z)
    while (j < i + 4) and (j < na):
      bind_j = lambda z : d2s.beta_j(j,z)
      a[i,j] = simpson_fg(bind_i, bind_j, 0, na - 3, 2 * (na - 3))
      a[j,i] = a[i,j]
      j = j + 1
    i = i + 1

  b = np.zeros(shape=(n,n))
  i = 0
  while i < 6:
    j = 0
    while j < i + 4:
      b[i,j] = a[i,j]
      b[j,i] = b[i,j]
      j = j + 1
    i = i + 1

  while i < n - 6:
    k = -3
    while k < 4:
      b[i,i + k] = a[6,6 + k]
      b[i + k,i] = b[i,i + k]
      k = k + 1
    i = i + 1

  while i < n:
    k = - 3
    while k < n - i:
      b[i,i + k] = a[12 + (i - n), 12 + (i - n) + k]
      b[i + k,i] = b[i,i + k]
      k = k + 1
    i = i + 1

  #checking

  i = 0
  while i < n:
    j = 0
    while j < n:
      error = abs(b[i,j] - b[n - 1 - i, n - 1-j])
      assert error < 1.0e-5, 'bug....' + str(i) + ',' + str(j)
      j = j + 1
    i = i + 1


  return 1.0e-5 * b


"""
Some fixed data:
weights =[0.43470768679675065, 0.70234026438735053, 0.06557777761086947, 0.1600460261762634, 0.54135062262335298, 0.050856016107522328, 0.17473709130199, 0.74161650357776676, 0.45860648789704928, 0.14159481604757318, 0.84721980315075984, 0.086969974586579846, 0.10755203343042352, 0.7009617941803733, 0.62476516555503137, 0.84680596019512555]

err = [4.0407246040420395, 17.923076414120604, -10.767841085140835, 4.1393430179930775, 10.565085709868121, -3.584372809095576, -11.774566767372946, 17.257106170388049, 2.6757461616453817, -10.527234880136081, 8.9848685270152622, -6.6169058175221496, -3.7332405500642714, -13.02819409732825, 22.750078462351926, -4.2842739152321094, 14.96757783200326, -2.4553840583728324, 18.861396668965529, -6.738813066862412, -8.4186285044590647, 7.4745396854916644, -13.559257482658458, -7.0204800255297615, 10.190792445314555, -17.823240291866707, 6.8026629126934148, 28.076870129591931, 9.1254265942523141, -11.364608723643313, 11.130477983696728, -14.425502355253265, -5.806975177393717, 2.6439377596784928, 5.9834056423728752, -44.09287902866226, 3.2457202857835865, 8.9932719431376658, -16.281282503217362, -18.738001438454987, -26.660671082997442, -8.6756844257800267, -11.304234163552247, -4.7872864657413361, 3.4258073451241695, -16.146674499028919, 9.0544681137787215, 24.848650542341094, 17.249853581359027, -0.30283797800742379, 0.37855493839974697, 4.4639944302046128, 20.225936254776382, 7.2556634177390036, 9.7897475601732431, -5.113334423387788, 7.0289069745437285, 24.19659714478404, -15.070958575128437, -11.974895353808336, -7.9217580071927234, 23.293920381732761, -6.7173190176511053, 2.1251620231213275, 3.9208470023037778, -9.2048186380279429, -12.031589993324703, 15.441730221060265, 14.197219907797001, -1.5403968817083806, 2.2266240309869718, 9.8391447338750222, -8.7659657931732315, 4.7198740432965476, -7.6448678383435258, 8.2774563718206426, 14.215887214498119, -5.8908381646577146, 6.6490880175057407, 5.4571918097483625, -9.7642109675504702, 8.7614178777467249, 7.660913381188883, -12.562982700498488, 5.5425282272514256, 20.084548902645526, -2.1418877013537481, 20.792510705733893, 26.207094680784824, -6.5188612054901851, -20.379346648258174, -34.356217384323699, 13.522426602406133, 24.637814902341464, 4.3255971858103592, -12.096729849949023, 14.903784302042354, -8.9308771583215361, 5.1727237461466506, 4.2302726340482]

calculated = [0.46215165101240407, 0.72451809655289978, 0.034505942139361853, 0.20103394093477878, 0.50756752382645198, 0.10693555052448254, 0.052481669158447326, 0.78396137171634217,
             0.50607678792654842, 0.11057751400915164, 0.88526496637460661, 0.067658833366388976, 0.16218838312986433, 0.66793335862573522, 0.65314875153266527, 0.85473860433433557]

"""


def ep_labnum(t, x_t, num_splines):
  default_spl = spline(np.ones(num_splines), x_min=t[0], x_max=t[-1])
  mu = np.zeros((len(t), num_splines))
  for i in range(len(t)):
      for j in range(num_splines):
          mu[i][j] = default_spl.beta_j(j, t[i])
  lmbda = 5
  m_1 = mu.T@mu
  b = mu.T@x_t.T
  m_2 = matrix_m2(num_splines)
  M = m_1 + lmbda*m_2
  res = np.linalg.solve(M, b)
  return res

def get_points(m_data, n_splines, x_min=0, x_max=1):
  t = np.linspace(x_min, x_max, m_data)
  weights = np.random.rand(n_splines)
  weights = np.array(weights)
  spl = spline(weights, x_min=t[0], x_max=t[-1])
  spl_t = spl(t)
  mu, sigma = 0, np.std(spl_t) / 3
  err = np.random.normal(mu, sigma, m_data)
  err = np.array(err)
  x_t = spl_t + err
  return t, x_t, spl_t


def main():
  # Testing the get points
  num_splines = 1600
  num_dados = 10001
  t, x_t, spl_t = get_points(num_dados, num_splines, 0, 10)
  t = np.linspace(0, 5, num_dados)
  x_t = np.sin(1/t)
  if len(t) < 1000:
    plt.scatter(t, x_t, label="Simulated with noise", color=np.random.rand(3,))
  #plt.plot(t, spl_t, label="Original data")
  plt.plot(t, x_t, label="Original data")
  plt.xlabel("t")
  plt.ylabel("spl(t)")
  plt.title("Dados")
  default_spl = spline(np.ones(num_splines), x_min=t[0], x_max=t[-1])
  mu = np.zeros((len(t), num_splines))
  for i in range(len(t)):
      for j in range(num_splines):
          mu[i][j] = default_spl.beta_j(j, t[i])
  print(mu)
  lmbda = 20
  m_1 = mu.T@mu
  b = mu.T@x_t.T
  m_2 = matrix_m2(num_splines)
  M = m_1 + lmbda*m_2
  res = np.linalg.solve(M, b)
  new_spline = spline(res, x_min=t[0], x_max=t[-1])
  plt.plot(t, new_spline(t), label="Simulated data")
  plt.legend(loc="upper right")
  plt.show()



if __name__ == '__main__':
  main()
