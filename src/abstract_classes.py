from abc import ABC, abstractmethod


class APIWorker(ABC):
    """
    Абстрактный класс для работы с API сервисов с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self, search_query: str):
        """
        Получает вакансии по поисковому запросу.
        :param search_query: Поисковый запрос
        :return: Список вакансий в формате JSON
        """
        pass


class Saver(ABC):
    """
    Абстрактный класс для сохранения вакансий в файл.
    """

    @abstractmethod
    def add_vacancy(self, vacancy_data: dict):
        """
        Добавляет одну вакансию в файл.
        :param vacancy_data: Данные вакансии в виде словаря
        """
        pass

    @abstractmethod
    def get_vacancies_by_criteria(self, criteria: dict) -> list[dict]:
        """
        Получает вакансии из файла по указанным критериям.
        :param criteria: Словарь с критериями поиска (например, {"city": "Москва"})
        :return: Список вакансий
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str):
        """
        Удаляет вакансию из файла по её ID.
        :param vacancy_id: Идентификатор вакансии
        """
        pass
