from ..schemas import HouseBase, HouseAnalogAdjustments

def calculate_adjustments(
    reference: HouseBase,
    analog: HouseBase
    ) -> HouseAnalogAdjustments:
    """
    Функция вычисления корректировок для аналога и эталона

    * `reference` - объект дома - эталона
    * `analog` - объект аналога
    """
    pass
