import resource_management as rm

def main():
    wood = [[3, 1, 2], [5, 0, 4]]
    stone = [[2, 4, 1], [3, 2, 5]]
    money = [[7, 5, 3], [6, 2, 8]]

    sorted_wood = rm.sort_array(wood)
    sorted_stone = rm.sort_array(stone)
    sorted_money = rm.sort_array(money)

    total_resources = rm.elementwise_array_sum(
        sorted_wood,
        rm.elementwise_array_sum(sorted_stone, sorted_money)
    )

    print(f"Recursos totales ordenados y sumados: {total_resources}")

    house_cost = [[1, 2, 3], [4, 5, 1], [2, 3, 5]]
    school_cost = [[2, 0, 1], [3, 2, 4], [1, 0, 3]]

    subsidy = [[1, 3, 2], [2, 1, 0], [3, 2, 1]]

    new_house_cost = rm.matrix_sum(house_cost, subsidy)
    new_school_cost = rm.matrix_sum(school_cost, subsidy)

    print(f"Costo de construcción de casas con subsidio: {new_house_cost}")
    print(f"Costo de construcción de escuelas con subsidio: {new_school_cost}")

main()
