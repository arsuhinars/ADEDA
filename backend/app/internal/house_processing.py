from ..schemas import HouseBase, HouseBrief, HouseAnalogAdjustments, \
    HouseState, HouseAdjustmentsCheckList

AREA_RANGES = [30, 50, 65, 90, 120]
AREA_TABLE = [
    [0, -6, -12, -17, -22, -24],
    [6, 0, -7, -12, -17, -19],
    [14, 7, 0, -6, -11, -13],
    [21, 14, 6, 0, -6, -8],
    [28, 21, 13, 6, 0, -3],
    [31, 24, 16, 9, 3, 0]
]
KITCHEN_RANGES = [7, 10]
KITCHEN_TABLE = [
    [0, 3, 9],
    [-2.9, 0, 5.8],
    [-8.3, -5.5, 0]
]
METRO_RANGES = [5, 10, 15, 30, 60]
METRO_TABLE = [
    [0, -7, -11, -15, -19, -22],
    [7, 0, -4, -8, -13, -17],
    [12, 4, 0, -5, -10, -13],
    [17, 9, 5, 0, -6, -9],
    [24, 15, 11, 6, 0, -4],
    [29, 20, 15, 10, 4, 0]
]

def __find_range(x, rng):
    for i in range(len(rng)):
        if x < rng[i]:
            return i
    return len(rng)


def calculate_adjustments(
    reference: HouseBrief,
    analog: HouseBase,
    check_list = HouseAdjustmentsCheckList()
    ) -> HouseAnalogAdjustments:
    """
    Функция вычисления корректировок для аналога и эталона

    * `reference` - объект дома - эталона
    * `analog` - объект аналога
    """
    adjustments = HouseAnalogAdjustments()

    # Корректировка на торг
    if check_list.trade:
        adjustments.trade = -4.5
    
    # Корректировка на этаж
    if check_list.floor and reference.floor != analog.floor:
        if analog.floor == 1:
            adjustments.floor = \
                3.2 if reference.floor == reference.floors_count else 7.5
        elif analog.floor == analog.floors_count:
            adjustments.floor = -3.1 if reference.floor == 1 else 4.2
        else:
            adjustments.floor = -7.0 if reference.floor == 1 else -4.0
    
    # Корректировка на площадь
    if check_list.area:
        adjustments.area = AREA_TABLE \
            [__find_range(analog.flat_area, AREA_RANGES)] \
            [__find_range(reference.flat_area, AREA_RANGES)]

    # Корректировка на площадь кухни
    if check_list.kitchen_area:
        adjustments.kitchen_area = KITCHEN_TABLE \
            [__find_range(analog.kitchen_area, KITCHEN_RANGES)] \
            [__find_range(reference.kitchen_area, KITCHEN_RANGES)]

    # Корректировка на наличие балкона/лоджии
    if check_list.balcony:
        if analog.has_balcony and not reference.has_balcony:
            adjustments.balcony = -5
        elif not analog.has_balcony and reference.has_balcony:
            adjustments.balcony = 5.3
    
    # Корректировка на расстояние до метро
    if check_list.metro:
        adjustments.metro = METRO_TABLE \
            [__find_range(analog.metro_distance, METRO_RANGES)] \
            [__find_range(reference.metro_distance, METRO_RANGES)]
    
    # Корректировка на ремонт
    if check_list.repairs and analog.state != reference.state:
        if analog.state == HouseState.NO_DECORATION:
            adjustments.repairs = 13400 \
                if reference.state == HouseState.STATE_DECORATION else 20100
        elif analog.state == HouseState.STATE_DECORATION:
            adjustments.repairs = -1300 \
                if reference.state == HouseState.NO_DECORATION else 6700
        else:
            adjustments.repairs = -20100 \
                if reference.state == HouseState.NO_DECORATION else -6700
    
    return adjustments
