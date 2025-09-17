import json
from pathlib import Path

from src.abstract_classes import Saver
from src.vacancy import Vacancy


class JSONSaver(Saver):
    """
    Класс для сохранения и загрузки вакансий в/из JSON файл(а).
    """

    def __init__(self, filename: str = "../data/vacancies.json"):
        """
        :param filename: Имя файла для сохранения/загрузки данных.
        """
        # Создаем путь к файлу относительно расположения класса
        self._file_path = Path(__file__).parent / filename
        # Создаем директорию, если её нет
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        # Создаем файл с пустым списком, если его нет
        if not self._file_path.exists():
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def __read_file(self) -> list[dict]:
        """Приватный метод для чтения данных из файла."""
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def __write_file(self, data: list[dict]):
        """Приватный метод для записи данных в файл."""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy_data: dict):
        """
        Добавляет одну вакансию в файл, если её ещё нет.
        :param vacancy_data: Данные вакансии в виде словаря.
        """
        vacancies = self.__read_file()
        # Проверяем, есть ли уже вакансия с таким ID
        if not any(vac["id"] == vacancy_data.get("id") for vac in vacancies):
            vacancies.append(vacancy_data)
            self.__write_file(vacancies)
            print(f"Вакансия '{vacancy_data.get('title')}' добавлена в файл.")
        else:
            print(f"Вакансия '{vacancy_data.get('title')}' уже существует в файле.")

    def get_vacancies_by_criteria(self, criteria: dict) -> list[dict]:
        """
        Возвращает вакансии, соответствующие критериям поиска.
        :param criteria: Словарь с критериями {поле: значение}.
        :return: Список найденных вакансий.
        """
        vacancies = self.__read_file()
        filtered_vacancies = []

        for vac in vacancies:
            match = True
            for key, value in criteria.items():
                # Поиск по подстроке в строковых полях, точное совпадение для остальных
                if key in vac:
                    if isinstance(vac[key], str) and isinstance(value, str):
                        if value.lower() not in vac[key].lower():
                            match = False
                            break
                    elif vac[key] != value:
                        match = False
                        break
            if match:
                filtered_vacancies.append(vac)

        return filtered_vacancies

    def delete_vacancy(self, vacancy_id: str):
        """
        Удаляет вакансию по её ID.
        :param vacancy_id: ID вакансии для удаления.
        """
        vacancies = self.__read_file()
        initial_length = len(vacancies)
        vacancies = [vac for vac in vacancies if vac.get("id") != vacancy_id]

        if len(vacancies) < initial_length:
            self.__write_file(vacancies)
            print(f"Вакансия с ID {vacancy_id} удалена.")
        else:
            print(f"Вакансия с ID {vacancy_id} не найдена.")

    def add_vacancies(self, vacancies_list: list["Vacancy"]):
        """
        Добавляет список объектов Vacancy в файл.
        :param vacancies_list: Список объектов Vacancy.
        """
        for vacancy in vacancies_list:
            # Конвертируем объект Vacancy в словарь для сохранения
            vac_data = {
                "title": vacancy.title,
                "url": vacancy._url,
                "salary_from": vacancy.salary_from,
                "salary_to": vacancy._salary_to,
                "currency": vacancy._currency,
                "description": vacancy._description,
                "id": vacancy.id,
            }
            self.add_vacancy(vac_data)
