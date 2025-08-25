from src.vacancy import Vacancy


class TestVacancy:
    """Test cases for Vacancy model."""

    def test_vacancy_creation_valid_data(self, sample_vacancy_data):
        """Test vacancy creation with valid data."""
        vacancy = Vacancy(**sample_vacancy_data)

        assert vacancy.name == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary == "100000-150000 руб."
        assert vacancy.description == "Требуется опыт работы от 3 лет"

    def test_vacancy_creation_missing_optional_fields(self):
        """Test vacancy creation with missing optional fields."""
        vacancy = Vacancy("Test", "https://test.com", "100000")

        assert vacancy.name == "Test"
        assert vacancy.url == "https://test.com"
        assert vacancy.salary == "100000"
        assert vacancy.description is None
        assert vacancy.requirements is None

    def test_vacancy_salary_validation(self):
        """Test salary validation."""
        vacancy_no_salary = Vacancy("Test", "https://test.com", "Не указана")
        vacancy_with_salary = Vacancy("Test", "https://test.com", "100000-150000")

        assert vacancy_no_salary.salary == "Не указана"
        assert vacancy_with_salary.salary == "100000-150000"

    def test_vacancy_comparison(self):
        """Test vacancy comparison by salary."""
        low_salary = Vacancy("Low", "url1", "50000")
        medium_salary = Vacancy("Medium", "url2", "100000")
        high_salary = Vacancy("High", "url3", "200000")
        no_salary = Vacancy("No", "url4", "Не указана")

        # Test less than
        assert low_salary < medium_salary
        assert no_salary < low_salary  # No salary should be considered lowest

        # Test greater than
        assert high_salary > medium_salary
        assert medium_salary > no_salary

        # Test equality
        same_salary1 = Vacancy("Test1", "url5", "100000")
        same_salary2 = Vacancy("Test2", "url6", "100000")
        assert same_salary1 == same_salary2

    def test_vacancy_str_representation(self, sample_vacancy):
        """Test string representation of vacancy."""
        result = str(sample_vacancy)
        assert "Python Developer" in result
        assert "100000-150000 руб." in result

    def test_vacancy_to_dict(self, sample_vacancy):
        """Test conversion to dictionary."""
        vacancy_dict = sample_vacancy.to_dict()

        assert vacancy_dict["name"] == "Python Developer"
        assert vacancy_dict["url"] == "https://hh.ru/vacancy/123"
        assert vacancy_dict["salary"] == "100000-150000 руб."
        assert isinstance(vacancy_dict, dict)
