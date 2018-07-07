import numpy as np
from splines import spline, matrix_m2
import matplotlib.pyplot as plt

def interpolate(x, y, num_splines, lmbda):
  default_spl = spline(np.ones(num_splines), x_min=x[0], x_max=x[-1])
  mu = np.zeros((len(x), num_splines))
  for i in range(len(x)):
      for j in range(num_splines):
          mu[i][j] = default_spl.beta_j(j, x[i])
  m_1 = mu.T@mu
  b = mu.T@y.T
  m_2 = matrix_m2(num_splines)
  M = m_1 + lmbda*m_2
  res = np.linalg.solve(M, b)
  return res

def get_points(m_data, n_splines, fn, x_min=0, x_max=1):
  t = np.linspace(x_min, x_max, m_data)
  spl_t = fn(t)
  mu, sigma = 0, np.std(spl_t) / 3
  err = np.random.normal(mu, sigma, m_data)
  x_t = spl_t + err
  return t, x_t, spl_t

def main():
  # Testing the get points
  num_splines = 10
  num_dados = 1000
  x_min = 0
  x_max = 10
  lmbda = 100

  # Generate a random spline to get samples from it
  weights = np.random.rand(num_splines)
  spl = spline(weights, x_min=x_min, x_max=x_max)

  # Get samples with noise
  t, x_t, spl_t = get_points(num_dados, num_splines, spl, x_min, x_max)

  if num_dados < 1000:
    plt.scatter(t, x_t, label="Simulated with noise", color=np.random.rand(3,))
  plt.plot(t, spl_t, label="Original data")
  plt.xlabel("t")
  plt.ylabel("spl(t)")
  plt.title("Dados")

  # Interpolate the samples
  res = interpolate(t, x_t, num_splines, lmbda)
  new_spline = spline(res, x_min=x_min, x_max=x_max)

  plt.plot(t, new_spline(t), label="Simulated curve")
  plt.legend(loc="upper right")
  plt.show()

if __name__ == '__main__':
  main()
