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
    if all(isinstance(x, (int, float)) for x in a) and all(isinstance(y, (int, float)) for y in b):
        return [x + y for x, y in zip(a, b)]
    
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def potencia(base, exp):
    if exp < 0:
        raise ValueError("No se pueden calcular potencias negativas sin decimales")
    if exp == 0:
        return 1
    resultado = 1
    for _ in range(exp):
        resultado *= base
    return resultado

def modulo(a, b):
    cociente = a // b
    producto = cociente * b
    return a - producto

def raiz_entera(numero):
    if numero < 0:
        raise ValueError("No se puede calcular la raíz de un número negativo")
    a = 0
    while (a + 1) * (a + 1) <= numero:
        a += 1
    return a