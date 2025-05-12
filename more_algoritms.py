import matplotlib
matplotlib.use('Qt5Agg')  # или 'TkAgg' при необходимости
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

class SortingVisualizer:
    def __init__(self, algorithm_name, array_size, is_3d=False, update_every=10):
        self.n = array_size
        self.update_every = update_every
        self.algorithm_name = algorithm_name
        self.arr = list(range(1, self.n + 1))
        random.shuffle(self.arr)
        self.is_3d = is_3d
        self.colors = plt.cm.viridis(np.linspace(0, 1, self.n))
        self.generator = self.get_generator(self.arr.copy())
        self.current_frame = self.arr.copy()
        self.iteration = 0
        self.completed = False
        self.final_message = ""

        self.fig = plt.figure(figsize=(12, 6))
        if self.is_3d:
            from mpl_toolkits.mplot3d import Axes3D
            self.ax = self.fig.add_subplot(111, projection='3d')
            self.z = np.zeros(self.n)
            self.dx = self.dy = np.ones(self.n)
        else:
            self.ax = self.fig.add_subplot(111)
            self.bar_container = None

    def get_generator(self, arr):
        if self.algorithm_name == "quicksort":
            return self.quicksort_gen(arr)
        elif self.algorithm_name == "bubblesort":
            return self.bubblesort_gen(arr)
        elif self.algorithm_name == "mergesort":
            return self.mergesort_gen(arr)
        elif self.algorithm_name == "insertionsort":
            return self.insertionsort_gen(arr)
        elif self.algorithm_name == "selectionsort":
            return self.selectionsort_gen(arr)
        elif self.algorithm_name == "shellsort":
            return self.shellsort_gen(arr)
        else:
            raise ValueError("Неизвестный алгоритм")

    # ---------- Алгоритмы ----------
    def quicksort_gen(self, arr):
        stack = [(0, len(arr)-1)]
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

    def bubblesort_gen(self, arr):
        iterations = 0
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    iterations += 1
                    if iterations % self.update_every == 0:
                        yield arr.copy()
        self.final_message = f"Готово! Итераций: {iterations}"

    def mergesort_gen(self, arr):
        current_size = 1
        n = len(arr)
        temp = arr.copy()
        iterations = 0

        while current_size < n:
            for left in range(0, n, 2 * current_size):
                mid = min(left + current_size - 1, n - 1)
                right = min(left + 2 * current_size - 1, n - 1)
                i, j, k = left, mid + 1, left
                while i <= mid and j <= right:
                    if arr[i] <= arr[j]:
                        temp[k] = arr[i]
                        i += 1
                    else:
                        temp[k] = arr[j]
                        j += 1
                    k += 1
                    iterations += 1
                    if iterations % self.update_every == 0:
                        yield arr.copy()
                while i <= mid:
                    temp[k] = arr[i]
                    i += 1
                    k += 1
                while j <= right:
                    temp[k] = arr[j]
                    j += 1
                    k += 1
                for x in range(left, right + 1):
                    arr[x] = temp[x]
                    iterations += 1
                    if iterations % self.update_every == 0:
                        yield arr.copy()
            current_size *= 2
        self.final_message = f"Готово! Итераций: {iterations}"

    def insertionsort_gen(self, arr):
        iterations = 0
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                iterations += 1
                if iterations % self.update_every == 0:
                    yield arr.copy()
            arr[j + 1] = key
            iterations += 1
            yield arr.copy()
        self.final_message = f"Готово! Итераций: {iterations}"
        
    def selectionsort_gen(self, arr):
        iterations = 0
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_idx]:
                    min_idx = j
                iterations += 1
                if iterations % self.update_every == 0:
                    yield arr.copy()
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr.copy()
        self.final_message = f"Готово! Итераций: {iterations}"

    def shellsort_gen(self, arr):
        n = len(arr)
        gap = n // 2
        iterations = 0
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                    iterations += 1
                    if iterations % self.update_every == 0:
                        yield arr.copy()
                arr[j] = temp
                yield arr.copy()
            gap //= 2
        self.final_message = f"Готово! Итераций: {iterations}"


    # ---------- Анимация ----------
    def init_animation(self):
        if self.is_3d:
            self.ax.set_xlim(0, self.n)
            self.ax.set_ylim(0, 1)
            self.ax.set_zlim(0, self.n + 1)
            self.ax.set_xticks([]); self.ax.set_yticks([]); self.ax.set_zticks([])
            bars = self.ax.bar3d(range(self.n), self.z, self.z, self.dx, self.dy, self.current_frame, color=self.colors)
            self.bar_container = bars
            return bars
        else:
            self.ax.set_xlim(-1, self.n)
            self.ax.set_ylim(0, self.n + 1)
            self.ax.set_xticks([]); self.ax.set_yticks([])
            bars = self.ax.bar(range(self.n), self.current_frame, color=self.colors, width=1.0)
            self.bar_container = bars
            return bars

    def update_animation(self, _):
        if not self.completed:
            try:
                self.current_frame = next(self.generator)
                self.iteration += 1
                if self.is_3d:
                    self.ax.cla()
                    self.ax.set_xlim(0, self.n)
                    self.ax.set_ylim(0, 1)
                    self.ax.set_zlim(0, self.n + 1)
                    self.ax.set_xticks([]); self.ax.set_yticks([]); self.ax.set_zticks([])
                    self.ax.bar3d(range(self.n), self.z, self.z, self.dx, self.dy, self.current_frame, color=self.colors)
                    self.ax.set_title(f"{self.algorithm_name} | Итерация {self.iteration}")
                else:
                    for bar, height in zip(self.bar_container, self.current_frame):
                        bar.set_height(height)
                    self.ax.set_title(f"{self.algorithm_name} | Итерация {self.iteration}")
            except StopIteration:
                self.completed = True
                self.ax.set_title(f"{self.algorithm_name} | {self.final_message}")
        return self.bar_container

    def visualize(self):
        self.anim = FuncAnimation(
            self.fig,
            self.update_animation,
            init_func=self.init_animation,
            interval=1,
            blit=False,
            cache_frame_data=False,
            repeat=False
        )
        plt.tight_layout()
        plt.show()

# ---------- Консольный интерфейс ----------
def main():
    algorithms = {
    "1": "quicksort",
    "2": "bubblesort",
    "3": "mergesort",
    "4": "insertionsort",
    "5": "selectionsort",
    "6": "shellsort",
}


    print("Выберите алгоритм:")
    for k, v in algorithms.items():
        print(f"{k}. {v.capitalize()}")
    alg_choice = input("Введите номер алгоритма: ").strip()
    algorithm = algorithms.get(alg_choice, "quicksort")

    try:
        size = int(input("Введите размер массива (например, 100): ").strip())
    except ValueError:
        size = 100

    viz_choice = input("Выберите визуализацию: 1 - 2D, 2 - 3D: ").strip()
    is_3d = viz_choice == "2"

    visualizer = SortingVisualizer(algorithm, size, is_3d=is_3d)
    visualizer.visualize()

if __name__ == "__main__":
    main()
