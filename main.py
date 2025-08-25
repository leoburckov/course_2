from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_saver import JSONSaver
from src.utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, print_vacancies


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    print("Добро пожаловать в парсер вакансий с HeadHunter!")
    search_query = input("Введите поисковый запрос (например, 'Python developer'): ").strip()

    # 1. Получаем вакансии с API
    print("\nПолучаем вакансии с HH.ru...")
    hh_api = HeadHunterAPI()
    hh_vacancies_json = hh_api.get_vacancies(search_query)

    if not hh_vacancies_json:
        print("По вашему запросу ничего не найдено. Попробуйте изменить запрос.")
        return

    # 2. Конвертируем JSON в объекты Vacancy
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_json)
    print(f"Получено {len(vacancies_list)} вакансий.")

    # 3. Сохраняем все полученные вакансии в файл
    json_saver = JSONSaver()
    json_saver.add_vacancies(vacancies_list)
    print("Вакансии сохранены в файл.")

    # 4. Запрашиваем параметры у пользователя
    try:
        top_n = int(input("\nВведите количество вакансий для вывода в топ N: "))
    except ValueError:
        print("Будет выведено 10 вакансий по умолчанию.")
        top_n = 10

    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например, '100000 - 150000'): ").strip()

    # 5. Загружаем вакансии ИЗ ФАЙЛА (а не используем свежеполученные) и работаем с ними
    # Это имитирует работу с сохраненными данными
    all_vacancies_data = json_saver.get_vacancies_by_criteria({})
    # Конвертируем данные из файла обратно в объекты Vacancy
    vacancies_from_file = []
    for vac_data in all_vacancies_data:
        vacancy = Vacancy(
            title=vac_data['title'],
            url=vac_data['url'],
            salary_from=vac_data['salary_from'],
            salary_to=vac_data['salary_to'],
            currency=vac_data['currency'],
            description=vac_data['description'],
            vacancy_id=vac_data['id']
        )
        vacancies_from_file.append(vacancy)

    # 6. Применяем фильтры и сортировку
    filtered_vacancies = filter_vacancies(vacancies_from_file, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # 7. Выводим результат
    print(f"\nРезультаты поиска ({len(top_vacancies)} из {len(vacancies_from_file)}):")
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()