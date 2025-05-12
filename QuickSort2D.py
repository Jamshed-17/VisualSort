import matplotlib
matplotlib.use('Qt5Agg')  # можно заменить на 'TkAgg' при необходимости
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

class QuickSortVisualizer:
    def __init__(self, n=500, update_every=5):
        self.n = n
        self.update_every = update_every  # обновлять граф каждые N шагов
        self.arr = list(range(1, n + 1))
        random.shuffle(self.arr)
        self.colors = plt.cm.viridis(np.linspace(0, 1, self.n))
        self.generator = self.quicksort_gen(self.arr.copy())
        self.current_frame = self.arr.copy()
        self.iteration = 0
        self.completed = False
        self.final_message = ""

        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.bar_container = None

    def quicksort_gen(self, arr):
        stack = [(0, len(arr) - 1)]
        iterations = 0
        while stack:
            l, r = stack.pop()
            if l >= r:
                continue
            pivot = arr[l]
            j = l
            for i in range(l + 1, r + 1):
                if arr[i] <= pivot:
                    j += 1
                    arr[j], arr[i] = arr[i], arr[j]
                    iterations += 1
                    if iterations % self.update_every == 0:
                        yield arr.copy()
            arr[l], arr[j] = arr[j], arr[l]
            iterations += 1
            yield arr.copy()
            stack.append((j + 1, r))
            stack.append((l, j - 1))
        self.final_message = f"Готово! Итераций: {iterations}"

    def init_animation(self):
        self.ax.set_title("QuickSort > Быстрая сортировка")
        self.ax.set_ylim(0, self.n + 1)
        self.ax.set_xlim(-1, self.n)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        bars = self.ax.bar(range(self.n), self.current_frame, color=self.colors, width=1.0)
        self.bar_container = bars
        return bars

    def update_animation(self, _):
        if not self.completed:
            try:
                self.current_frame = next(self.generator)
                self.iteration += 1
                for bar, height in zip(self.bar_container, self.current_frame):
                    bar.set_height(height)
                self.ax.set_title(f"QuickSort > Итерация: {self.iteration}")
            except StopIteration:
                self.completed = True
                self.ax.set_title(f"QuickSort > {self.final_message}")
        return self.bar_container

    def visualize(self):
        self.anim = FuncAnimation(
            self.fig,
            self.update_animation,
            init_func=self.init_animation,
            interval=1,  # можно увеличить до 10–20 для меньшей нагрузки
            blit=False,
            cache_frame_data=False,
            repeat=False
        )
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    visualizer = QuickSortVisualizer(n=500, update_every=50)  # меньше update_every — плавнее, но тяжелее
    visualizer.visualize()
