import matplotlib.pyplot as plt

const = 1200

func = [1]
for i in range(1, 110):
    func.append(func[i - 1] * i)

def choose(n, m):
    return int(func[n] // func[m] // func[n - m])

def Stirling(n, m):
    sum = 0
    for i in range(1, m):
        sum += int(((-1) ** (i+1))) * choose(m, i) * int((i) ** n)
    return sum // func[m]

def calc(n):
    N = func[108] * Stirling(n, 108)
    D = 108 ** n
    # print(N, D)
    return N / D


a = []
p = []

first = 0

for n in range(200, const):
    a.append(n)
    p.append(1 - calc(n))
    if (p[len(p) - 1] >= 0.95) and (first == 0):
        print(p[len(p) - 1])
        first = n 


plt.figure(figsize=(10, 15), dpi=100)
plt.scatter(a, p, c='blue', s = 1)
plt.xlabel("the number of n(buying n boxes)")
plt.ylabel("probability of collect all coupons")
plt.title("the probability of collect all 108 types of coupons with buying n boxes")

plt.axhline(0.95, xmin = 0, xmax = 1, color='r', linestyle='--') # 0,0.61
plt.axvline(823, ymin=0, ymax= 0.91, color='r', linestyle='--')

# plt.axvline(x = 823 , ymin = 0.0, ymax = 0.95)

plt.legend()

plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 0.95, 1.0])
plt.xticks([200, 400, 600,  800, 1000, 1200])
# plt.xticks([823], fontsize = 5)

plt.show()
# print(p)
print(first)