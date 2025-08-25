from typing import Any


class Vacancy:
    """
    Класс для представления вакансии.
    """

    # __slots__ для экономии памяти и контроля над атрибутами
    __slots__ = (
        "_title",
        "_url",
        "_salary_from",
        "_salary_to",
        "_currency",
        "_description",
        "_id",
    )

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: int | None,
        salary_to: int | None,
        currency: str | None,
        description: str,
        vacancy_id: Any
    ):
        """
        Инициализация объекта Вакансия.
        :param title: Название вакансии
        :param url: Ссылка на вакансию
        :param salary_from: Нижняя граница зарплаты
        :param salary_to: Верхняя граница зарплаты
        :param currency: Валюта зарплаты
        :param description: Описание вакансии/требования
        :param vacancy_id: Идентификатор вакансии на платформе
        """
        self._title = title
        self._url = url
        # Валидация зарплаты
        self._salary_from = self._validate_salary(salary_from)
        self._salary_to = self._validate_salary(salary_to)
        self._currency = currency
        self._description = description
        self._id = vacancy_id

    @staticmethod
    def _validate_salary(salary_value: int | None) -> int:
        """
        Приватный метод валидации зарплаты.
        Если зарплата не указана, возвращает 0.
        :param salary_value: Значение зарплаты
        :return: Валидированное значение зарплаты (int)
        """
        return salary_value if salary_value is not None else 0

    @property
    def salary_from(self) -> int:
        """Геттер для нижней границы зарплаты."""
        return self._salary_from

    @property
    def salary_to(self) -> int:
        """Геттер для верхней границы зарплаты."""
        return self._salary_to

    @property
    def title(self) -> str:
        """Геттер для названия вакансии."""
        return self._title

    @property
    def id(self) -> str:
        """Геттер для ID вакансии."""
        return self._id

    def __gt__(self, other) -> bool:
        """Сравнение 'больше' (>). Сравниваем по нижней границе зарплаты."""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self.salary_from > other.salary_from

    def __lt__(self, other) -> bool:
        """Сравнение 'меньше' (<). Сравниваем по нижней границе зарплаты."""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self.salary_from < other.salary_from

    def __ge__(self, other) -> bool:
        """Сравнение 'больше или равно' (>=)."""
        return self.salary_from >= other.salary_from

    def __le__(self, other) -> bool:
        """Сравнение 'меньше или равно' (<=)."""
        return self.salary_from <= other.salary_from

    def __str__(self) -> str:
        """Строковое представление вакансии для пользователя."""
        salary_info = "Зарплата не указана"
        if self._salary_from or self._salary_to:
            from_str = f"от {self._salary_from}" if self._salary_from else ""
            to_str = f"до {self._salary_to}" if self._salary_to else ""
            currency_str = f" {self._currency}" if self._currency else ""
            salary_info = f"{from_str} {to_str}{currency_str}".strip()

        return (
            f"Вакансия: {self._title}\n"
            f"Ссылка: {self._url}\n"
            f"Зарплата: {salary_info}\n"
            f"Описание: {self._description[:100]}...\n"
            f"---"
        )

    @classmethod
    def cast_to_object_list(cls, hh_vacancies: list[dict]) -> list["Vacancy"]:
        """
        Классовый метод для преобразования списка вакансий из JSON (HH.ru)
        в список объектов класса Vacancy.
        :param hh_vacancies: Список вакансий в формате HH.ru
        :return: Список объектов Vacancy
        """
        vacancy_list = []
        for vac in hh_vacancies:
            # Обрабатываем структуру зарплаты от HH
            salary = vac.get("salary")
            if salary:
                salary_from = salary.get("from")
                salary_to = salary.get("to")
                currency = salary.get("currency")
            else:
                salary_from = salary_to = currency = None

            # Создаем объект Vacancy
            vacancy = cls(
                title=vac.get("name", "Без названия"),
                url=vac.get("alternate_url", "Ссылка не указана"),
                salary_from=salary_from,
                salary_to=salary_to,
                currency=currency,
                description=vac.get("snippet", {}).get(
                    "requirement", "Описание не указано"
                ),
                vacancy_id=vac.get("id"),
            )
            vacancy_list.append(vacancy)
        return vacancy_list
