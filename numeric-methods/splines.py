# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

###############################################################################
#
# spline = a cubic b spline with equally spaced nodes
#
###############################################################################

class spline:

# spline with support in [x_min,x_max] and n >= 8 intervals

    def __init__(self, weights, x_min = 0, x_max = 1):
      assert x_max > x_min, 'x_max must be greater than x_min'
      assert type(weights) == np.ndarray, 'weight must be a numpy array'
      assert len(weights) >= 8, 'there must be at least 8 weights'
      dx = x_max - x_min
      self.n = len(weights) - 3
      self.scale = self.n/dx
      self.x_min = x_min
      self.x_max = x_max
      self.weights = weights

    def locate(self, t):
      if t <= self.x_min:
        return [0.0, 0]

      nw = len(self.weights)

      if t >= self.x_max:
        return [1.0, nw - 4]

      dt = self.scale * (t - self.x_min)

      if dt >= nw:
        dt = 1.0
        return [1.0, nw - 1]

      bin = int(np.floor(dt))
      dt -= bin
      return [dt,bin]

  # Hardcoded Splines
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
# d_spline = the derivative of the previous spline
#
###############################################################################

class d_spline:

# the derivative of an spline with support in [x_min,x_max] and n >= 8 intervals

    def __init__(self, weights, x_min = 0, x_max = 1):
      assert x_max > x_min, 'x_max must be greater than x_min'
      assert type(weights) == np.ndarray, 'weight must be a numpy array'
      assert len(weights) >= 8, 'there must be at least 8 weights'
      dx = x_max - x_min
      self.n = len(weights) - 3
      self.scale = self.n/dx
      self.x_min = x_min
      self.x_max = x_max
      self.weights = weights

    def locate(self, t):
      if t <= self.x_min:
        return [0.0, 0]

      nw = len(self.weights)

      if t >= self.x_max:
        return [1.0, nw - 4]

      dt = self.scale * (t - self.x_min)

      if dt >= nw:
        dt = 1.0
        return [1.0, nw - 1]

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

# the derivative of an spline with support in [x_min,x_max] and n >= 8 intervals

    def __init__(self, weights, x_min = 0, x_max = 1):
      assert x_max > x_min, 'x_max must be greater than x_min'
      assert type(weights) == np.ndarray, 'weight must be a numpy array'
      assert len(weights) >= 8, 'there must be at least 8 weights'
      dx = x_max - x_min
      self.n = len(weights) - 3
      self.scale = self.n/dx
      self.x_min = x_min
      self.x_max = x_max
      self.weights = weights

    def locate(self, t):
      if t <= self.x_min:
        return [0.0, 0]

      nw = len(self.weights)

      if t >= self.x_max:
        return [1.0, nw - 4]

      dt = self.scale * (t - self.x_min)

      if dt >= nw:
        dt = 1.0
        return [1.0, nw - 1]

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
"""
Some fixed data:
weights =[ 0.71362165  0.7312819   0.28578785  0.72625597  0.02829012  0.12093212
  0.57039311  0.07396345  0.30056213  0.72305948  0.13181418  0.39346008
  0.27301438  0.76474467  0.86693262  0.43410863]

err = [ -7.85157709 -12.92255349 -17.32423387  -0.89025862  13.13619879
   0.57082557   8.73400619  19.15203654  -7.36949562 -17.17361854
 -11.97772227  -3.29295136  17.1989631    0.41401076  12.64912304
 -15.99940417  11.80196631  15.87606787 -17.67073401   3.23636432
  -0.28562633   8.6316289  -17.02878288   1.79054375   2.73716767
   3.95991511  -2.08428861 -25.13198744  -1.47526867  -2.54935011
  10.88130686   8.15709343  14.63744526   7.47877596 -14.35635258
  -0.43598964  -6.49773062  -5.2879045   -9.51904213  -7.55298738
   1.75881947  -4.38373551  20.58606902  -4.34927156   2.8519147
  -4.96762026  -8.82744649   3.53348654   6.31765094  12.27277917
  17.34041646  -9.08565129 -13.66671513  -1.77283233  11.71713346
   0.95528386  18.95830559   7.7191811  -15.54325112 -16.17633469
   3.51011188  20.69877155   1.18673353  -2.1621375  -16.91327138
 -29.85700319 -27.83832409   6.82408984   0.23278505  -7.47693559
   1.10090316  13.71523873   2.25795915  -5.35280909  -4.30512874
 -14.28870776 -33.29891759   1.02618189 -12.61151097  16.44126939
  -0.21563856  -1.3496143   11.66052487  25.40249952  -6.86231148
 -16.4040602   -3.3531628    1.11823809   8.31014697  17.23290813
  12.91901202 -16.17753123   2.35060184  19.67399187 -12.22543148
  16.8739259   -7.93283968  -7.01616971   8.12422586   6.00343464]
"""


def get_points(m_data, n_splines, x_min=0, x_max=1):
  t = np.linspace(x_min, x_max, m_data)
  weights = np.random.rand(n_splines)
  spl = spline(weights, x_min=x_min, x_max=x_max)
  spl_t = spl(t)
  mu, sigma = 0, np.std(spl_t)/3
  err = np.random.normal(mu, sigma, m_data)
  x_t = spl_t + err
  return t, x_t, spl_t

def main():
  # Testing the get points
  t, x_t, spl_t = get_points(100, 16, 0, 10)
  plt.scatter(t, x_t, label="Simulated with noise", color=np.random.rand(3,))
  plt.plot(t, spl_t, label="Original data")
  plt.xlabel("t")
  plt.ylabel("spl(t)")
  plt.title("Dados gerados")
  plt.legend(loc="upper right")
  plt.show()


if __name__ == '__main__':
  main()
