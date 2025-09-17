import requests

from src.abstract_classes import APIWorker


class HeadHunterAPI(APIWorker):
    """
    Класс для подключения к API HeadHunter и получения вакансий.
    """

    # Базовый URL для API HH.ru
    __BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        # Параметры по умолчанию для запроса
        self.__params = {
            "per_page": 100,  # Количество вакансий на странице (максимум 100)
            "area": 113,  # Код региона (113 - Россия)
            "text": None,  # Поисковый запрос
        }
        self.__headers = {"User-Agent": "HH-User-Agent"}

    def __get_data(self, url, params=None):
        """
        Приватный метод для отправки GET-запроса и обработки ответа.
        :param url: URL для запроса
        :param params: Параметры запроса
        :return: Данные в формате JSON
        """
        response = requests.get(url, headers=self.__headers, params=params)
        response.raise_for_status()  # Проверяем, не была ли ошибка HTTP
        return response.json()

    def get_vacancies(self, search_query: str) -> list[dict]:
        """
        Публичный метод для получения вакансий по поисковому запросу.
        :param search_query: Поисковый запрос (например, "Python developer")
        :return: Список словарей с данными о вакансиях
        """
        self.__params["text"] = search_query

        try:
            data = self.__get_data(self.__BASE_URL, self.__params)
            # API HH возвращает вакансии в ключе 'items'
            vacancies = data.get("items", [])
            return vacancies
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API HH.ru: {e}")
            return []
