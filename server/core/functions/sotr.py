def Bubble_Sort(arr):
    """
    Сортировка пузырьком.
    Сравнивает попарно элементы и "всплывает" максимальные значения в конец массива.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def Insertion_Sort(arr):
    """
    Сортировка вставками.
    Каждый элемент вставляется на своё место в отсортированной части массива.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def Selection_Sort(arr):
    """
    Сортировка выбором.
    Находит минимальный элемент и ставит его на первую неотсортированную позицию.
    """
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def Merge_Sort(arr):
    """
    Сортировка слиянием.
    Рекурсивно делит массив пополам и сливает отсортированные части.
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        Merge_Sort(L)
        Merge_Sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def Quick_Sort(arr):
    """
    Быстрая сортировка (Quick Sort).
    Делит массив относительно опорного элемента и рекурсивно сортирует части.
    """
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]
        return Quick_Sort(less_than_pivot) + [pivot] + Quick_Sort(greater_than_pivot)
    
def Heap_Sort(arr):
    """
    Пирамидальная сортировка (Heap Sort).
    Строит кучу и извлекает максимальные элементы по одному.
    """
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def Counting_Sort(arr):
    """
    Сортировка подсчётом.
    Подходит для целых чисел в ограниченном диапазоне.
    """
    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    sorted_arr = []
    for i, cnt in enumerate(count):
        sorted_arr.extend([i] * cnt)

    return sorted_arr

def Radix_Sort(arr):
    """
    Поразрядная сортировка (Radix Sort).
    Сортирует числа поразрядно с помощью сортировки подсчётом.
    """
    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1

        for i in range(n):
            arr[i] = output[i]

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr

def Bucket_Sort(arr):
    """
    Сортировка корзинами (Bucket Sort).
    Делит элементы на корзины и сортирует каждую отдельно.
    """
    bucket = []
    for i in range(len(arr)):
        bucket.append([])

    for j in arr:
        index = int(10 * j)
        bucket[index].append(j)

    for i in range(len(bucket)):
        bucket[i] = sorted(bucket[i])

    result = []
    for i in range(len(bucket)):
        result += bucket[i]

    return result

def Shell_Sort(arr):
    """
    Сортировка Шелла.
    Улучшенная сортировка вставками с убывающим шагом.
    """
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def Tim_Sort(arr):
    """
    TimSort — гибридная сортировка, основанная на сортировке вставками и слиянием.
    Используется в Python по умолчанию.
    """
    min_run = 32
    n = len(arr)

    def insertion_sort(arr, left, right):
        for i in range(left + 1, right + 1):
            key_item = arr[i]
            j = i - 1
            while j >= left and arr[j] > key_item:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key_item

    def merge(left, mid, right):
        left_copy = arr[left:mid + 1]
        right_copy = arr[mid + 1:right + 1]

        left_cursor, right_cursor = 0, 0
        sorted_index = left

        while left_cursor < len(left_copy) and right_cursor < len(right_copy):
            if left_copy[left_cursor] <= right_copy[right_cursor]:
                arr[sorted_index] = left_copy[left_cursor]
                left_cursor += 1
            else:
                arr[sorted_index] = right_copy[right_cursor]
                right_cursor += 1
            sorted_index += 1

        while left_cursor < len(left_copy):
            arr[sorted_index] = left_copy[left_cursor]
            left_cursor += 1
            sorted_index += 1

        while right_cursor < len(right_copy):
            arr[sorted_index] = right_copy[right_cursor]
            right_cursor += 1
            sorted_index += 1

    size = n
    for start in range(0, size, min_run):
        end = min(start + min_run - 1, size - 1)
        insertion_sort(arr, start, end)

    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(n - 1, start + size - 1)
            end = min((start + size * 2 - 1), (n - 1))

            if mid < end:
                merge(start, mid, end)
        size *= 2

    return arr

def Comb_Sort(arr):
    """
    Сортировка расчёской (Comb Sort).
    Улучшение пузырьковой сортировки с использованием большого шага.
    """
    gap = len(arr)
    shrink = 1.3
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1
        sorted = True

        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
    return arr

def Gnome_Sort(arr):
    """
    Сортировка гномом (Gnome Sort).
    Переставляет элементы, пока не окажутся на своих местах.
    """
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr

def Pigeonhole_Sort(arr):
    """
    Сортировка по принципу "голубятни" (Pigeonhole Sort).
    Подходит для целых чисел в небольшом диапазоне.
    """
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    holes = [0] * size

    for num in arr:
        holes[num - min_val] += 1

    index = 0
    for i in range(size):
        while holes[i] > 0:
            arr[index] = i + min_val
            index += 1
            holes[i] -= 1
    return arr

def Cycle_Sort(arr):
    """
    Циклическая сортировка (Cycle Sort).
    Минимизирует количество записей в массив.
    """
    writes = 0
    for cycle_start in range(len(arr) - 1):
        item = arr[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, len(arr)):
            if arr[i] < item:
                pos += 1

        if pos == cycle_start:
            continue

        while item == arr[pos]:
            pos += 1

        if pos != cycle_start:
            arr[pos], item = item, arr[pos]
            writes += 1

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, len(arr)):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            if item != arr[pos]:
                arr[pos], item = item, arr[pos]
                writes += 1
    return arr

def Stooge_Sort(arr, l, h):
    """
    Сортировка глупцом (Stooge Sort).
    Рекурсивная сортировка с низкой эффективностью.
    arr — массив, l — левый индекс, h — правый индекс.
    """
    if l >= h:
        return

    if arr[l] > arr[h]:
        arr[l], arr[h] = arr[h], arr[l]

    if h - l + 1 > 2:
        m = (h - l + 1) // 3
        Stooge_Sort(arr, l, h - m)
        Stooge_Sort(arr, l + m, h)
        Stooge_Sort(arr, l, h - m)
    return arr