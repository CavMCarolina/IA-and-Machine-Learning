# pip install pandas numpy matplotlib openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcula_A(y, x):
    a = np.dot(x - np.mean(x), y - np.mean(y)) / np.dot(x - np.mean(x), x - np.mean(x))
    return a

def calcula_B(y, x):
    b = np.mean(y) - a * np.mean(x)
    return b

def calcula_erro(a, b, x, y):
    erro = 0

    # Somar os valores de cada erro da reta
    for i in range(len(y)):
        erro += (a * x[i] + b - y[i])**2
    
    return erro

# array com valores especificados 
A = np.linspace(-10, 10, 100) # 100 números de 0.2 em 0.2
B = np.linspace(-5, 5, 100) # 100 números de 0.1 em 0.1

data = pd.read_excel("./dados/data.xlsx")
data_x = data['x']
data_y = data['y']

# Cria uma matriz de 100 por 100 apenas com 0 --> 10.000 retas a serem criadas
erros = np.zeros(shape= (100, 100))

# Valor de referência comparável com o resto da lista. Precisa pertencer ao conjunto (para ser comparável)
menor = calcula_erro(A[0], B[0], data_x, data_y)

# CASO o menor seja esse mesmo para não dar pau (chance de 1 em 10000....)
valores = [A[0], B[0], menor]

for i, a in enumerate(A):
    for j, b in enumerate(B):
        # Calcula todos os erros de cada linha do conjunto
        erro = calcula_erro(a, b, data_x, data_y)

        # Coloca o erro na matriz de acordo com a posição do índice
        erros[i][j] = erro
        
        if erro < menor:
            menor = erro
            valores = [a, b, menor]

print(valores)

# Pegar a e b do erro mínimo
a, b = valores[0], valores[1]

# Comparar com a aula passada
minimos_a, minimos_b = calcula_A(data_y, data_x), calcula_B(data_y, data_x)

plt.plot(data_x, data_y, 'bo')
# Criar a reta com o erro mínimo
plt.plot(data_x, a * data_x + b, 'g', label= 'Aula 3 (Arrays)')

# Comparar com o da aula passada
plt.plot(data_x, minimos_a * data_x + minimos_b, 'r', label= 'Aula 2 (Derivadas)')
plt.legend()
plt.figure()
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

X, Y = np.meshgrid(A, B)
ax.plot_surface(X, Y, erros, cmap="viridis")

plt.show()