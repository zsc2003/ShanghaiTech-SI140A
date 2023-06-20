p = 1.0
E = 1.0
v = 0.0

maxn = 366
for j in range(2, maxn + 1):
    p = p * (1 - (j - 2) / 365.0)
    E += p
    v += p * (j - 1)

V = E + 2.0 * v - E ** 2

print("E(X) = ", E)
print("Var(X) = ", V)