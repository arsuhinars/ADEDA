from pydantic import BaseModel

from .house import HouseBrief, HouseBase, HouseAdjustments

class ExportAnalog(BaseModel):
    """ Схема экспортируемого аналога """
    house: HouseBase
    adjustments: HouseAdjustments


class ExportTable(BaseModel):
    """ Схема экспортируемой таблицы """
    reference: HouseBrief
    analogs: list[ExportAnalog]
