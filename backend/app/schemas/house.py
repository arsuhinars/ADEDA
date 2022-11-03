import enum

from pydantic import BaseModel

class HouseSegment(str, enum.Enum):
    """ Сегмент дома """
    # Новостройка
    NEW = 'new'
    # Современное жилье
    MODERN = 'modern'
    # Старый жилой фонд
    OLD = 'old'


class HouseMaterial(str, enum.Enum):
    """ Материал стен дома """
    BRICK = 'brick'
    PANEL = 'panel'
    MONOLIT = 'monolit'


class HouseState(str, enum.Enum):
    """ Состояние дома """
    # Без отделки
    NO_DECORATION = 'no'
    # Муниципальный ремонт
    STATE_DECORATION = 'state'
    # Современная отделка
    MODERN_DECORATION = 'modern'


class SourceService(str, enum.Enum):
    """ Сервис-источник данных """
    AVITO = 'avito'
    CIAN = 'cian'


class HouseBase(BaseModel):
    """ Модель дома/квартиры """
    id: int | None = None

    location: str
    rooms_count: int
    segment: HouseSegment
    floor: int
    floors_count: int
    flat_area: float
    kitchen_area: float
    has_balcony: bool
    material: HouseMaterial
    state: HouseState
    metro_station: str
    metro_distance: float

    price: float

    source_service: SourceService
    url: str


class HouseBrief(BaseModel):
    """ Краткое описание дома/квартиры. Используется в импортируемой таблице """
    location: str
    rooms_count: int
    segment: HouseSegment
    floor: int
    floors_count: int
    flat_area: float
    kitchen_area: float
    has_balcony: bool
    material: HouseMaterial
    state: HouseState
    metro_distance: float


class HouseAdjustmentsCheckList(BaseModel):
    """
    Чек-лест выбранных корректировок
    
    Подробнее про корректировки в `HouseAnalogAdjustments`
    """
    trade: bool = True
    area: bool = True
    metro: bool = True
    floor: bool = True
    kitchen_area: bool = True
    balcony: bool = True
    repairs: bool = True


class HouseRequest(BaseModel):
    """ Модель запроса для поиска аналогов """

    house: HouseBrief
    adjustments: HouseAdjustmentsCheckList
    max_house_count: int = 10


class HouseAnalogAdjustments(BaseModel):
    """
    Модель корректировок квартиры-аналога. Корректировки указываются в процентах
    от -100 до 100
    """
    trade: float = 0.0        # Корректировка на торг
    area: float = 0.0         # Корректировка на площадь
    metro: float = 0.0        # Корректировка на отдаленность от метро
    floor: float = 0.0        # Корректировка на этаж
    kitchen_area: float = 0.0 # Корректировка на площадь кухни
    balcony: float = 0.0      # Корректировка на наличие балкона/лоджии
    repairs: float = 0.0      # Корректировка на ремонт

    def calc_size(self):
        """ Вычислить размер применненых корректировок """
        return abs(self.trade) + abs(self.area) + abs(self.metro) + \
            abs(self.floor) + abs(self.kitchen_area) + \
            abs(self.balcony) + abs(self.repairs)
