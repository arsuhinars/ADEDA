from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

from app import config


def create_webdriver() -> WebDriver:
    """ Метод для создания веб-драйвера """
    match config.PARSER_BROWSER:
        case 'chrome':
            return create_chrome_webdriver()
        case 'firefox':
            return create_firefox_webdriver()


def create_chrome_webdriver():
    options = webdriver.ChromeOptions()
    for key, val in config.WEBDRIVER_OPTIONS.items():
        setattr(options, key, val)

    return webdriver.Chrome(
        service=ChromeService(driver_path),
        options=options
    )


def create_firefox_webdriver():
    options = webdriver.FirefoxOptions()
    for key, val in config.WEBDRIVER_OPTIONS.items():
        setattr(options, key, val)

    return webdriver.Firefox(
        service=FirefoxService(driver_path),
        options=options
    )


def on_start():
    """ Функция должна вызываться при запуске приложения """
    global driver_path

    # Скачиваем менеджер драйверов
    match config.PARSER_BROWSER.lower():
        case 'chrome':
            driver_manager = ChromeDriverManager()
        case 'firefox':
            driver_manager = GeckoDriverManager()
    driver_path = driver_manager.install()

    # Создаем глобальный драйвер
    global shared_driver
    shared_driver = create_webdriver()


def on_end():
    """ Функция должна вызываться при завершении приложения """
    shared_driver.quit()


class WebdriverHelper:
    def __init__(self, driver: WebDriver=None):
        """ 
        Конструктор класса
        
        * `driver` - веб-драйвер. Если указан `None`, то будет использовать
        глобальный общий драйвер
        """
        self.driver = driver if driver is not None else shared_driver
        self.is_shared_driver = driver is None
    
    def close(self):
        """ Метод прекращения работы с драйвером """
        if not self.is_shared_driver:
            self.driver.close()

    def has_element(self, xpath: str):
        """
        Метод проверки элемента на существование
        
        * `xpath` - XPath запрос для поиска данного элемента
        """
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def get_element_text(self, xpath: str) -> (str | None):
        """
        Метод получения текстового содержания элемента по XPath запросу.
        Если элемента не существует, то возвращает `None`
        
        * `xpath` - XPath запрос для поиска данного элемента
        """
        try:
            el = self.driver.find_element(By.XPATH, xpath)
            return el.text
        except NoSuchElementException:
            return None
