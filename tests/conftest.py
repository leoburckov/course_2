from unittest.mock import Mock

import pytest

from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancy_data():
    """Sample vacancy data for testing."""
    return {
        "name": "Python Developer",
        "url": "https://hh.ru/vacancy/123",
        "salary": "100000-150000 руб.",
        "description": "Требуется опыт работы от 3 лет",
        "requirements": "Python, Django, Flask",
    }


@pytest.fixture
def sample_vacancy(sample_vacancy_data):
    """Create a sample vacancy instance."""
    return Vacancy(**sample_vacancy_data)


@pytest.fixture
def sample_vacancies():
    """Create multiple sample vacancies."""
    return [
        Vacancy(
            "Junior Python",
            "https://hh.ru/vacancy/1",
            "50000-70000",
            "Для начинающих",
            "Python basics",
        ),
        Vacancy(
            "Middle Python",
            "https://hh.ru/vacancy/2",
            "100000-150000",
            "Опыт от 2 лет",
            "Python, Django",
        ),
        Vacancy(
            "Senior Python",
            "https://hh.ru/vacancy/3",
            "200000-300000",
            "Опыт от 5 лет",
            "Python, Microservices",
        ),
    ]


@pytest.fixture
def json_saver(tmp_path):
    """Create JSONSaver instance with temporary file."""
    test_file = tmp_path / "test_vacancies.json"
    return JSONSaver(file_path=str(test_file))


@pytest.fixture
def mock_response():
    """Mock response for API calls."""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {
                    "requirement": "Python experience",
                    "responsibility": "Development",
                },
            }
        ]
    }
    return mock
