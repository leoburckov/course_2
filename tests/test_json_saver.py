import json
import os


class TestJSONSaver:
    """Test cases for JSONSaver."""

    def test_file_creation(self, json_saver, sample_vacancy):
        """Test that file is created when adding vacancy."""
        assert not os.path.exists(json_saver._file_path)

        json_saver.add_vacancy(sample_vacancy)

        assert os.path.exists(json_saver._file_path)

    def test_add_vacancy(self, json_saver, sample_vacancy):
        """Test adding vacancy to file."""
        json_saver.add_vacancy(sample_vacancy)

        with open(json_saver._file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["name"] == "Python Developer"

    def test_prevent_duplicates(self, json_saver, sample_vacancy):
        """Test that duplicates are not added."""
        json_saver.add_vacancy(sample_vacancy)
        json_saver.add_vacancy(sample_vacancy)  # Same vacancy

        with open(json_saver._file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1  # Should still be only one

    def test_delete_vacancy(self, json_saver, sample_vacancy):
        """Test deleting vacancy from file."""
        json_saver.add_vacancy(sample_vacancy)

        # Verify vacancy was added
        with open(json_saver._file_path, "r", encoding="utf-8") as f:
            assert len(json.load(f)) == 1

        json_saver.delete_vacancy(sample_vacancy)

        # Verify vacancy was deleted
        with open(json_saver._file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert len(data) == 0

    def test_get_vacancies(self, json_saver, sample_vacancies):
        """Test retrieving vacancies with filters."""
        for vacancy in sample_vacancies:
            json_saver.add_vacancy(vacancy)

        # Test get all
        all_vacancies = json_saver.get_vacancies()
        assert len(all_vacancies) == 3

        # Test filter by keyword
        python_vacancies = json_saver.get_vacancies(keyword="Python")
        assert len(python_vacancies) == 3

        # Test filter by salary range
        high_salary = json_saver.get_vacancies(salary_min=150000)
        assert len(high_salary) == 1
        assert "Senior" in high_salary[0]["name"]

    def test_clear_file(self, json_saver, sample_vacancies):
        """Test clearing all vacancies from file."""
        for vacancy in sample_vacancies:
            json_saver.add_vacancy(vacancy)

        assert len(json_saver.get_vacancies()) == 3

        json_saver.clear()

        assert len(json_saver.get_vacancies()) == 0
