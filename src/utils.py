from typing import List

from src.vacancy import Vacancy


def filter_vacancies(
    vacancies_list: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам в описании.
    :param vacancies_list: Список вакансий для фильтрации.
    :param filter_words: Список ключевых слов.
    :return: Отфильтрованный список вакансий.
    """
    if not filter_words:
        return vacancies_list

    filtered = []
    for vacancy in vacancies_list:
        # Объединяем название и описание для поиска
        text_to_search = f"{vacancy.title} {vacancy._description}".lower()
        if all(word.lower() in text_to_search for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(
    vacancies_list: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат.
    :param vacancies_list: Список вакансий для фильтрации.
    :param salary_range: Строка с диапазоном, например "100000 - 150000".
    :return: Отфильтрованный список вакансий.
    """
    if not salary_range.strip():
        return vacancies_list

    try:
        # Пытаемся распарсить строку диапазона
        parts = salary_range.split("-")
        if len(parts) == 2:
            min_salary = int(parts[0].strip())
            max_salary = int(parts[1].strip())
        else:
            # Если введен один номер, ищем от этого значения и выше
            min_salary = int(parts[0].strip())
            max_salary = int("inf")
    except ValueError:
        print("Ошибка формата диапазона зарплат. Используйте формат '100000 - 150000'.")
        return vacancies_list

    ranged_vacancies = []
    for vacancy in vacancies_list:
        # Сравниваем с верхней границей вакансии, если она указана
        vac_salary = vacancy.salary_from or 0
        if min_salary <= vac_salary <= max_salary:
            ranged_vacancies.append(vacancy)

    return ranged_vacancies


def sort_vacancies(vacancies_list: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по убыванию зарплаты (от большей к меньшей).
    :param vacancies_list: Список вакансий для сортировки.
    :return: Отсортированный список вакансий.
    """
    return sorted(vacancies_list, reverse=True)


def get_top_vacancies(vacancies_list: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий из списка.
    :param vacancies_list: Список вакансий.
    :param top_n: Количество вакансий для возврата.
    :return: Список из top_n вакансий.
    """
    return vacancies_list[:top_n]


def print_vacancies(vacancies_list: List[Vacancy]):
    """
    Выводит отформатированный список вакансий.
    :param vacancies_list: Список вакансий для вывода.
    """
    if not vacancies_list:
        print("По вашему запросу вакансий не найдено.")
        return

    for i, vacancy in enumerate(vacancies_list, 1):
        print(f"\n{i}. {vacancy}")
