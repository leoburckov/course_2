from unittest.mock import Mock, patch

import pytest

from src.hh_api import HeadHunterAPI


class TestHeadHunterAPI:
    """Test cases for HeadHunterAPI."""

    def test_inheritance(self):
        """Test that HeadHunterAPI inherits from abstract API."""
        assert issubclass(HeadHunterAPI, __BASE_URL)

    @patch("src.api.hh_api.requests.get")
    def test_get_vacancies_success(self, mock_get, mock_response):
        """Test successful vacancies retrieval."""
        mock_get.return_value = mock_response
        api = HeadHunterAPI()

        vacancies = api.get_vacancies("Python")

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        mock_get.assert_called_once()

    @patch("src.api.hh_api.requests.get")
    def test_get_vacancies_api_error(self, mock_get):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        with pytest.raises(Exception, match="API request failed"):
            api.get_vacancies("Python")

    @patch("src.api.hh_api.requests.get")
    def test_get_vacancies_with_params(self, mock_get, mock_response):
        """Test vacancies retrieval with parameters."""
        mock_get.return_value = mock_response
        api = HeadHunterAPI()

        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "text=Python" in call_args[0][0]
        assert "per_page=50" in call_args[0][0]
        assert "area=1" in call_args[0][0]

    def test_parse_salary(self):
        """Test salary parsing from API response."""
        api = HeadHunterAPI()

        # Test with salary range
        salary_data = {"from": 100000, "to": 150000, "currency": "RUR"}
        result = api._parse_salary(salary_data)
        assert result == "100000-150000 RUR"

        # Test with only from salary
        salary_from = {"from": 100000, "currency": "RUR"}
        result = api._parse_salary(salary_from)
        assert result == "100000 RUR"

        # Test with only to salary
        salary_to = {"to": 150000, "currency": "RUR"}
        result = api._parse_salary(salary_to)
        assert result == "150000 RUR"

        # Test no salary
        result = api._parse_salary(None)
        assert result == "Не указана"
