import asyncio
import re

from selenium.webdriver.common.by import By

from . import Parser
from ..schemas import HouseBase, HouseSegment, HouseMaterial, HouseState, \
    SourceService
from ..internal.webdriver_helper import WebdriverHelper
from ..internal.errors import ParseError
from app import config

AVITO_BASE_URL = 'https://www.avito.ru/moskva/kvartiry/prodam'

SELECTORS = {
    'CAPCHA_LABEL': './/h2[contains(@class, "firewall-title")]',
    'FLAT_LINKS': './/div[@data-marker="catalog-serp"]//*[contains(@class, "iva-item-root-_lk9K")]//*[contains(@class, "iva-item-titleStep-pdebR")]//a',
    'NEXT_PAGE_BTN': './/span[contains(@class, "pagination-item-JJq_j") and contains(., "След")]',

    'LOCATION': './/span[contains(@class, "style-item-address__string-wt61A")]',
    'ROOMS_COUNT': './/li[contains(@class, "params-paramsList__item-appQw") and contains(span, "Количество комнат")]',
    'BUILD_YEAR': './/li[contains(@class, "style-item-params-list-item-aXXql") and contains(span, "Год постройки")]',
    'COMPLETION_DATE': './/li[contains(@class, "style-item-params-list-item-aXXql") and contains(span, "Срок сдачи")]',
    'HOUSE_TYPE': './/li[contains(@class, "style-item-params-list-item-aXXql") and contains(span, "Тип дома")]',
    'FLOOR': './/li[contains(@class, "params-paramsList__item-appQw") and contains(span, "Этаж")]',
    'FLAT_AREA': './/li[contains(@class, "params-paramsList__item-appQw") and contains(span, "Общая площадь")]',
    'KITCHEN_AREA': './/li[contains(@class, "params-paramsList__item-appQw") and contains(span, "Площадь кухни")]',
    'BALCONY_AND_LOGGIA': './/li[contains(@class, "params-paramsList__item-appQw") and contains(span, "Балкон или лоджия")]',
    'STATE': './/li[contains(@class, "params-paramsList__item-appQw") and contains(span, "Ремонт")]',
    'DECORATION': './/li[contains(@class, "params-paramsList__item-appQw") and contains(span, "Отделка")]',
    
    'METRO_STATION': '(.//*[contains(@class, "style-item-address-georeferences-item-TZsrp")]/span[not(@*)])[1]',
    'METRO_DISTANCE': '(.//*[contains(@class, "style-item-address-georeferences-item-TZsrp")]/span[contains(@class, "style-item-address-georeferences-item-interval-ujKs2")])[1]',

    'PRICE': './/span[contains(@class, "js-item-price style-item-price-text-_w822 text-text-LurtD text-size-xxl-UPhmI")]',
}

ROOMS_COUNT_REGEX = re.compile('Количество комнат: (\S+)')
BUILD_YEAR_REGEX = re.compile('Год постройки: (\d+)')
FLOOR_REGEX = re.compile('Этаж: (\d+) из (\d+)')
HOUSE_TYPE_REGEX = re.compile('Тип дома: (\S+)')
FLAT_AREA_REGEX = re.compile('Общая площадь: (\d+([.]\d+)?) м²')
KITCHEN_AREA_REGEX = re.compile('Площадь кухни: (\d+([.]\d+)?) м²')
STATE_REGEX = re.compile('Ремонт: (.+)')
DECORATION_REGEX = re.compile('Отделка: (.+)')
METRO_DISTANCE_REGEX = re.compile('(((от|до) (\d+))|(\d+[–-]\d+)|(\d+)) мин[.]')

class AvitoParser(Parser):
    """ Парсер с сайта Avito """

    async def begin(self):
        self.helper = WebdriverHelper()
        self.helper.driver.switch_to.new_window()
        self.main_win_handle = self.helper.driver.current_window_handle

        self.helper.driver.get(AVITO_BASE_URL)
        self.flat_iter = iter(self.get_flats_links())

    async def parse_next(self) -> HouseBase:
        await asyncio.sleep(config.PARSE_DELAY)

        try:
            try:
                # Пытаемся получить ссылку на следующую квартиру
                link = next(self.flat_iter)
            except StopIteration:
                # Если список закончился
                self.helper.driver.switch_to.window(
                    self.main_win_handle
                )
                # Переходим на следующую страницу
                self.helper.driver.find_element(
                    By.XPATH, SELECTORS['NEXT_PAGE_BTN']
                ).click()
                # Проверяем капчу
                if self.check_capcha():
                    raise ParseError('Capcha required')
                # Получаем список квартир
                self.flat_iter = iter(self.get_flats_links())
                
                link = next(self.flat_iter)
                await asyncio.sleep(config.PARSE_DELAY)
            
            # Открываем страницу след. квартиры
            self.helper.driver.switch_to.new_window()
            self.helper.driver.get(link)
            if self.check_capcha():
                raise ParseError('Capcha required')

            try:
                # Адрес
                location = self.helper.get_element_text(SELECTORS['LOCATION'])

                # Кол-во комнат
                rooms_count_str = ROOMS_COUNT_REGEX.match(
                    self.helper.get_element_text(SELECTORS['ROOMS_COUNT'])
                ).group(1)
                if rooms_count_str.lower() == 'студия':
                    rooms_count = 1
                else:
                    try:
                        rooms_count = int(rooms_count_str)
                    except ValueError:
                        raise ParseError('Unable to parse rooms count', link)
                
                # Сегмент дома
                build_year_str = self.helper.get_element_text(SELECTORS['BUILD_YEAR'])
                if build_year_str is not None:
                    build_year = int(BUILD_YEAR_REGEX.match(build_year_str).group(1))
                    if build_year < 1917:
                        segment = HouseSegment.OLD
                    else:
                        segment = HouseSegment.NEW
                else:
                    if self.helper.has_element(SELECTORS['COMPLETION_DATE']):
                        segment = HouseSegment.MODERN
                    else:
                        raise ParseError('Unable to parse house segment', link)

                # Этаж и кол-во этажей
                floor_match = FLOOR_REGEX.match(
                    self.helper.get_element_text(SELECTORS['FLOOR'])
                )
                floor = int(floor_match.group(1))
                floors_count = int(floor_match.group(2))

                # Материал стен
                house_type = HOUSE_TYPE_REGEX.match(
                    self.helper.get_element_text(SELECTORS['HOUSE_TYPE'])
                ).group(1)
                match house_type.lower():
                    case 'кирпичный':
                        material = HouseMaterial.BRICK
                    case 'монолитный' | 'монолитно-кирпичный':
                        material = HouseMaterial.MONOLIT
                    case 'панельный' | 'блочный':
                        material = HouseMaterial.PANEL
                    case _:
                        raise ParseError('Unable to parse house type', link)

                # Общая площадь
                flat_area = float(FLAT_AREA_REGEX.match(
                    self.helper.get_element_text(SELECTORS['FLAT_AREA'])
                ).group(1))
                
                # Площадь кухни
                kitchen_area_str = self.helper.get_element_text(
                    SELECTORS['KITCHEN_AREA']
                )
                if kitchen_area_str is not None:
                    kitchen_area = float(KITCHEN_AREA_REGEX.match(
                        kitchen_area_str
                    ).group(1))
                else:
                    kitchen_area = 0
            
                # Есть ли балкон или лоджия
                balcony_str = self.helper.get_element_text(
                    SELECTORS['BALCONY_AND_LOGGIA']
                )
                has_balcony = balcony_str is not None and \
                    ('балкон' in balcony_str or 'лоджия' in balcony_str)

                # Состояние дома
                decoration_str = self.helper.get_element_text(
                    SELECTORS['DECORATION']
                )
                if decoration_str is not None:
                    match DECORATION_REGEX.match(decoration_str).group(1).lower():
                        case 'чистовая' | 'предчистовая':
                            state = HouseState.STATE_DECORATION
                        case 'без отделки':
                            state = HouseState.NO_DECORATION
                        case _:
                            raise ParseError('Unable to parse house state', link)
                else:
                    state_str = self.helper.get_element_text(SELECTORS['STATE'])
                    if state_str is None:
                        raise ParseError('Unable to parse house state', link)
                    match STATE_REGEX.match(state_str).group(1).lower():
                        case 'требует ремонта':
                            state = HouseState.NO_DECORATION
                        case 'косметический' | 'дизайнерский' | 'евро':
                            state = HouseState.MODERN_DECORATION
                        case _:
                            raise ParseError('Unable to parse house state', link)
                
                # Ближайшая станция метро
                metro_station = self.helper.get_element_text(
                    SELECTORS['METRO_STATION']
                )
                metro_distance_str = self.helper.get_element_text(
                    SELECTORS['METRO_DISTANCE']
                )
                if metro_station is None or metro_distance_str is None:
                    raise ParseError('Unable to parse metro station', link)
                
                metro_distance_match = METRO_DISTANCE_REGEX.match(
                    metro_distance_str
                )

                if metro_distance_match.group(4):
                    metro_distance = int(metro_distance_match.group(4))
                elif metro_distance_match.group(6):
                    metro_distance = int(metro_distance_match.group(6))
                elif metro_distance_match.group(5):
                    metro_distance = sum(
                        map(int, metro_distance_match.group(5).split('–'))
                    ) // 2
                else:
                    raise ParseError('Unable to parse metro distance', link)

                # Стоимость квартиры
                price = int(
                    self.helper
                    .get_element_text(SELECTORS['PRICE'])
                    .replace(' ', '')
                )

                return HouseBase(
                    location=location,
                    rooms_count=rooms_count,
                    segment=segment,
                    floor=floor,
                    floors_count=floors_count,
                    flat_area=flat_area,
                    kitchen_area=kitchen_area,
                    has_balcony=has_balcony,
                    material=material,
                    state=state,
                    metro_station=metro_station,
                    metro_distance=metro_distance,
                    price=price,
                    source_service=SourceService.AVITO,
                    url=link
                )
            finally:
                self.helper.driver.close()
                self.helper.driver.switch_to.window(
                    self.main_win_handle
                )
        except Exception:
            raise ParseError('Unknown error', link)
   
    async def end(self):
        self.helper.driver.switch_to.window(self.main_win_handle)
        self.helper.driver.close()
        self.helper.driver.switch_to.window(
            self.helper.driver.window_handles[0]
        )
        self.helper.close()

    def check_capcha(self):
        """ Метод проверки на капчу на сайте """
        return self.helper.has_element(SELECTORS['CAPCHA_LABEL'])

    def get_flats_links(self):
        """ Получить ссылки на все квартиры с текущей страницы """
        els = self.helper.driver.find_elements(
            By.XPATH, SELECTORS['FLAT_LINKS']
        )
        return map(lambda el: el.get_attribute('href'), els)
