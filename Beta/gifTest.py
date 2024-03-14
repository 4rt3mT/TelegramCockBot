import matplotlib.pyplot as plt
import numpy as np
import imageio
from matplotlib import animation
# Создаем данные для анимации
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

# Создаем фигуру и ось для графика
fig, ax = plt.subplots()

# Устанавливаем пределы осей
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1, 1)

# Создаем пустой график
line, = ax.plot([], [], lw=2)

# Функция инициализации анимации
def init():
    line.set_data([], [])
    return line,

# Функция для обновления данных на графике в каждом кадре
def animate(i):
    ydata = np.sin(x + i / 10)
    line.set_data(x, ydata)
    return line,

# Создаем анимацию
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=50, blit=True)

# Сохраняем анимацию как GIF
ani.save('test_animation.gif', writer='pillow', fps=10)

plt.show()
