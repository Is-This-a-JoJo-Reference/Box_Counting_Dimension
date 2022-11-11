import matplotlib
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math
import numpy as np
from scipy import stats

'''
Ну, которче, вот код, вычисляющий размерность Минковского по изображению.
Частично не знаю как он работает, но результаты, вроде, верные
Ответ должен быть в консоли в самом конце
'''

image = Image.open('Maps/Rus/rus_map.png') # Открвыаем картинку (максимальный размер картинок - 178956970 пикселей)
width, height = image.size # Размер изображения
pix = image.load() # pix - список всех пикселей

# Ща будет максимально костыльный код

def box_count(eps): # eps is scale (in interval from 2 to inf)
    temp_list = []

    for x in range(width):
        temp = []
        counter = 0
        flag = 0
        for y in range(height):
            if counter < eps-1:
                if pix[x, y] == 0:
                    flag = 1
                counter += 1
            else:
                temp.append(flag)
                counter = 0
                flag = 0
        temp_list.append(temp)

    matrix = []

    for y in range(len(temp_list[0])):
        temp = []
        counter = 0
        flag = 0
        for x in range(width):
            if counter < eps-1:
                if temp_list[x][y] == 1:
                    flag = 1
                counter += 1
            else:
                temp.append(flag)
                counter = 0
                flag = 0
        matrix.append(temp)

    n=0
    for i in matrix:
        n+= sum(i)
    return n

x = [] # Список значений Eps
y = [] # Список значений N(Eps)

num_exp  = 15 # Уже не помню что это

max_c = math.ceil((min(height, width))) # И это тоже какая-то фигня
delta = math.ceil((max_c - 2)/num_exp) # Ну, это просто Дельта

for eps in range(2, max_c, delta):
    print(eps/max_c*100, '%')
    x.append(eps)
    y.append(box_count(eps))

print('100 %\n-------')

slope, intercept, r_value, p_value, std_err = stats.linregress([np.log(i) for i in x],[np.log(i) for i in y]) # Считаем методом минимальных квадратов
yy = [slope*i + intercept for i in [np.log(i) for i in x]] # slope = k, intercept = b, y = kx + b

print('Размерность Минковского границы', -1*slope) # Ответ

plt.subplot(211)
plt.plot(x, y)
plt.xlabel('N(ε)')
plt.ylabel('ε')
plt.grid(True)

plt.subplot(212)
plt.plot([np.log(i) for i in x], [np.log(i) for i in y])
plt.plot([np.log(i) for i in x], yy)
plt.xlabel('ln(N(ε))')
plt.ylabel('ln(ε)')
plt.grid(True)

plt.subplots_adjust(hspace=0.35)

plt.savefig('Res/graph.png', dpi=300) # Сохраняем графики
plt.show()