import pytest

from src.utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies
from src.vacancy import Vacancy


class TestFilters:
    """Test cases for filter functions."""

    @pytest.fixture
    def vacancies(self):
        return [
            Vacancy(
                "Python Junior", "url1", "50000", "Python development", "Python basics"
            ),
            Vacancy(
                "Python Middle", "url2", "100000", "Web development", "Python, Django"
            ),
            Vacancy(
                "Java Developer", "url3", "120000", "Java development", "Java, Spring"
            ),
        ]

    def test_filter_vacancies_by_keyword(self, vacancies):
        """Test filtering vacancies by keyword."""
        filtered = filter_vacancies(vacancies, ["Python"])
        assert len(filtered) == 2
        assert all("Python" in vac.name for vac in filtered)

    def test_filter_vacancies_multiple_keywords(self, vacancies):
        """Test filtering by multiple keywords."""
        filtered = filter_vacancies(vacancies, ["Python", "Junior"])
        assert len(filtered) == 1
        assert "Junior" in filtered[0].name

    def test_filter_vacancies_no_matches(self, vacancies):
        """Test filtering when no matches found."""
        filtered = filter_vacancies(vacancies, ["JavaScript"])
        assert len(filtered) == 0

    def test_filter_vacancies_empty_keywords(self, vacancies):
        """Test filtering with empty keywords list."""
        filtered = filter_vacancies(vacancies, [])
        assert len(filtered) == len(vacancies)

    def test_get_vacancies_by_salary(self, vacancies):
        """Test filtering by salary range."""
        # Test minimum salary
        result = get_vacancies_by_salary(vacancies, "80000")
        assert len(result) == 2
        assert all(vac.salary != "50000" for vac in result)

        # Test range
        result = get_vacancies_by_salary(vacancies, "80000-110000")
        assert len(result) == 1
        assert result[0].salary == "100000"

    def test_sort_vacancies(self, vacancies):
        """Test sorting vacancies by salary."""
        sorted_vac = sort_vacancies(vacancies)

        salaries = [vac.salary for vac in sorted_vac]
        assert salaries == ["120000", "100000", "50000"]

    def test_sort_vacancies_with_none(self):
        """Test sorting when some vacancies have no salary."""
        vacancies = [
            Vacancy("No Salary", "url1", "Не указана"),
            Vacancy("With Salary", "url2", "100000"),
        ]

        sorted_vac = sort_vacancies(vacancies)
        assert sorted_vac[0].salary == "100000"
        assert sorted_vac[1].salary == "Не указана"
