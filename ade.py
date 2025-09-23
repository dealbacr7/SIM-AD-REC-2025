import resource_management as rm

def main():
    wood = [999]
    stone = [999]
    money = [999]
    obreros = [999]
    espacio_dis = [999]

    sorted_wood = rm.sort_array(wood)
    sorted_stone = rm.sort_array(stone)
    sorted_money = rm.sort_array(money)

    total_resources = rm.elementwise_array_sum(
        sorted_wood,
        rm.elementwise_array_sum(sorted_stone, sorted_money)
    )

    print(f"Recursos totales ordenados y sumados: {total_resources}")

    house_cost = [10,20,100,30]
    school_cost = [50,100,200,200]

    subsidy = [10]

    new_house_cost = rm.matrix_sum(house_cost, subsidy)
    new_school_cost = rm.matrix_sum(school_cost, subsidy)

    print(f"Costo de construcción de casas con subsidio: {new_house_cost}")
    print(f"Costo de construcción de escuelas con subsidio: {new_school_cost}")

main()
