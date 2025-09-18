def _bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def sort_array(array):
    if all(isinstance(row, list) for row in array):
        return [_bubble_sort(row[:]) for row in array]
    else:
        return _bubble_sort(array[:])

def elementwise_array_sum(a, b):
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]

def matrix_sum(a, b):
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]

numero = int(input("Introduce un número: "))
potencia = int(input("Introduce una potencia: "))

if potencia < 0:
    print("No se pueden calcular potencias negativas sin decimales")
elif potencia == 0:
    print("Si la potencia es 0 el resultado siempre es 1")
else:
    resultado = 1
    for _ in range(potencia):
        resultado *= numero
    print(f"{numero} elevado a {potencia} es {resultado}")
