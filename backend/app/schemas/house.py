import enum

from pydantic import BaseModel

class HouseSegment(enum.Enum):
    """ Сегмент дома """
    # Новостройка
    NEW = 'new'
    # Современное жилье
    MODERN = 'modern'
    # Старый жилой фонд
    OLD = 'old'


class HouseMaterial(enum.Enum):
    """ Материал стен дома """
    BRICK = 'brick'
    PANEL = 'panel'
    MONOLIT = 'monolit'


class HouseState(enum.Enum):
    """ Состояние дома """
    # Без отделки
    NO_DECORATION = 'no'
    # Муниципальный ремонт
    STATE_DECORATION = 'state'
    # Современная отделка
    MODERN_DECORATION = 'modern'


class SourceService(enum.Enum):
    """ Сервис-источник данных """
    AVITO = 'avito'
    CIAN = 'cian'


class HouseBase(BaseModel):
    """ Модель дома/квартиры """
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
    trade: bool
    area: bool
    metro: bool
    floor: bool
    room_count: bool
    kitchen_area: bool
    balcony: bool
    repairs: bool


class HouseRequest(BaseModel):
    """ Модель запроса для поиска аналогов """

    house: HouseBrief
    adjustments: HouseAdjustmentsCheckList
    max_house_count: int


class HouseAnalogAdjustments(BaseModel):
    """
    Модель корректировок квартиры-аналога. Корректировки указываются в процентах
    от -100 до 100
    """
    trade: float        # Корректировка на торг
    area: float         # Корректировка на площадь
    metro: float        # Корректировка на отдаленность от метро
    floor: float        # Корректировка на этаж
    room_count: float   # Корректировка на комнатность
    kitchen_area: float # Корректировка на площадь кухни
    balcony: float      # Корректировка на наличие балкона/лоджии
    repairs: float      # Корректировка на ремонт

    def calc_size(self):
        """ Вычислить размер применненых корректировок """
        return abs(self.trade) + abs(self.area) + abs(self.metro) + \
            abs(self.floor) + abs(self.room_count) + abs(self.kitchen_area) + \
            abs(self.balcony) + abs(self.repairs)
