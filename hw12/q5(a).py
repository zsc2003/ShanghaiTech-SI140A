import numpy as np
import matplotlib.pyplot as plt
import tqdm

sample_size = 1000000

Y = np.random.uniform(0, 1, sample_size)
c = 256 / 27
FoverG = c * Y * ((1 - Y) ** 3)

X = np.zeros(sample_size)
U = np.random.uniform(0, 1, sample_size)

for i in tqdm.tqdm(range(sample_size)):
    if FoverG[i] >= U[i]:
        X[i] = Y[i]
    else:
        while True:
            y = np.random.uniform(0, 1)
            foverg = c * y * ((1 - y) ** 3)
            if np.random.uniform(0, 1) <= foverg:
                X[i] = y
                break

plt.hist(X, bins=100, density=True) # histogram of X

# Beta(2,4) PDF
def beta(x): # the PDF of the Beta(2,4)
    return 20 * x * ((1 - x) ** 3)

# theoretical PDF
x = np.linspace(0, 1, 1000) # sample points for plotting pdf
pdf = beta(x) # pdf values at sample points
plt.plot(x, pdf)

plt.xlabel('x')
plt.ylabel('PDF')
plt.title('Beta(2,4)')
plt.legend(['theoretical PDF','histogram'])
plt.xticks(np.arange(0, 1.01, 0.2))
plt.show()