import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
from itertools import zip_longest

class SortingVisualizer:
    def __init__(self, n=20):
        self.n = n
        self.arr = list(range(1, n+1))
        random.shuffle(self.arr)
        self.setup_figure()
        self.setup_algorithms()
        self.completed = [False] * 4
        self.current_frames = [self.arr.copy() for _ in range(4)]
        self.iterations = [0] * 4
        self.final_messages = [""] * 4

    def setup_figure(self):
        self.fig = plt.figure(figsize=(14, 10), dpi=100)
        self.fig.suptitle('Сравнение алгоритмов сортировки (3D)', fontsize=16)
        self.axes = [
            self.fig.add_subplot(221, projection='3d'),
            self.fig.add_subplot(222, projection='3d'),
            self.fig.add_subplot(223, projection='3d'),
            self.fig.add_subplot(224, projection='3d')
        ]
        self.titles = ["QuickSort > Быстрая", "BubbleSort > Пузырьковая", "MergeSort > Слиянием", "InsertionSort > Вставками"]
        self.colors = plt.cm.viridis(np.linspace(0, 1, self.n))
        self.z = np.zeros(self.n)
        self.dx = self.dy = np.ones(self.n)

    def setup_algorithms(self):
        self.generators = [
            self.quicksort_gen(self.arr.copy()),
            self.bubblesort_gen(self.arr.copy()),
            self.mergesort_gen(self.arr.copy()),
            self.insertionsort_gen(self.arr.copy())
        ]

    def quicksort_gen(self, arr):
        stack = [(0, len(arr)-1)]
        iterations = 0
        while stack:
            l, r = stack.pop()
            if l >= r:
                continue
                
            x = arr[l]
            j = l
            for i in range(l+1, r+1):
                if arr[i] <= x:
                    j += 1
                    arr[j], arr[i] = arr[i], arr[j]
                    iterations += 1
                    yield arr.copy()
            arr[l], arr[j] = arr[j], arr[l]
            iterations += 1
            yield arr.copy()
            
            stack.append((j+1, r))
            stack.append((l, j-1))
        self.final_messages[0] = f"Готово! Итераций: {iterations}"

    def bubblesort_gen(self, arr):
        n = len(arr)
        iterations = 0
        for i in range(n):
            swapped = False
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    swapped = True
                    iterations += 1
                    yield arr.copy()
            if not swapped:
                break
        self.final_messages[1] = f"Готово! Итераций: {iterations}"

    def mergesort_gen(self, arr):
        current_size = 1
        n = len(arr)
        temp_arr = arr.copy()
        iterations = 0
        
        while current_size < n:
            for left in range(0, n, 2*current_size):
                mid = min(left + current_size - 1, n-1)
                right = min(left + 2*current_size - 1, n-1)
                
                i, j, k = left, mid+1, left
                while i <= mid and j <= right:
                    if arr[i] <= arr[j]:
                        temp_arr[k] = arr[i]
                        i += 1
                    else:
                        temp_arr[k] = arr[j]
                        j += 1
                    k += 1
                    iterations += 1
                    yield arr.copy()
                
                while i <= mid:
                    temp_arr[k] = arr[i]
                    i += 1
                    k += 1
                    iterations += 1
                    yield arr.copy()
                
                while j <= right:
                    temp_arr[k] = arr[j]
                    j += 1
                    k += 1
                    iterations += 1
                    yield arr.copy()
                
                for x in range(left, right+1):
                    arr[x] = temp_arr[x]
                    iterations += 1
                    yield arr.copy()
            
            current_size *= 2
        self.final_messages[2] = f"Готово! Итераций: {iterations}"

    def insertionsort_gen(self, arr):
        iterations = 0
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >= 0 and arr[j] > key:
                arr[j+1] = arr[j]
                j -= 1
                iterations += 1
                yield arr.copy()
            arr[j+1] = key
            iterations += 1
            yield arr.copy()
        self.final_messages[3] = f"Готово! Итераций: {iterations}"

    def init_animation(self):
        for ax, title, frame in zip(self.axes, self.titles, self.current_frames):
            ax.clear()
            dz = np.array(frame)
            ax.bar3d(range(self.n), self.z, self.z, self.dx, self.dy, dz, 
                    color=self.colors, shade=True, alpha=0.8)
            ax.set_title(title, y=1.02)
            ax.set_xlim(0, self.n)
            ax.set_ylim(0, 1)
            ax.set_zlim(0, self.n+1)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks(range(0, self.n+1, max(1, self.n//5)))
        return self.axes

    def update_animation(self, _):
        any_active = False
        
        for i in range(4):
            if not self.completed[i]:
                try:
                    self.current_frames[i] = next(self.generators[i])
                    self.iterations[i] += 1
                    self.axes[i].clear()
                    dz = np.array(self.current_frames[i])
                    self.axes[i].bar3d(range(self.n), self.z, self.z, 
                                     self.dx, self.dy, dz, 
                                     color=self.colors, shade=True, alpha=0.8)
                    title = f"{self.titles[i]} (итерация: {self.iterations[i]})"
                    self.axes[i].set_title(title, y=1.02)
                    self.axes[i].set_xlim(0, self.n)
                    self.axes[i].set_ylim(0, 1)
                    self.axes[i].set_zlim(0, self.n+1)
                    self.axes[i].set_xticks([])
                    self.axes[i].set_yticks([])
                    self.axes[i].set_zticks(range(0, self.n+1, max(1, self.n//5)))
                    any_active = True
                except StopIteration:
                    self.completed[i] = True
                    self.axes[i].set_title(f"{self.titles[i]} - {self.final_messages[i]}", y=1.02)
        
        if not any_active:
            self.anim.event_source.stop()
            print("\nВсе алгоритмы завершены!")
            for i, title in enumerate(self.titles):
                print(f"{title}: {self.final_messages[i]}")
        
        return self.axes

    def visualize(self):
        self.anim = FuncAnimation(
            self.fig,
            self.update_animation,
            init_func=self.init_animation,
            interval=30,
            blit=False,
            cache_frame_data=False,
            repeat=False
        )
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()

if __name__ == "__main__":
    # n = int(input("Введите размер массива (рекомендуется 10-30): "))
    n = 16
    visualizer = SortingVisualizer(n)
    visualizer.visualize()