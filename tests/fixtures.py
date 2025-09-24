# flake8: noqa

import os
from unittest.mock import patch

import pytest

from dbt_ai.dbt import DbtModelProcessor

sample_sql_content = "SELECT * FROM table1;"

# Sample data for testing
sample_yaml_content = """
models:
  - name: model1
    description: Example model 1
  - name: model2
    description: Example model 2
"""


@pytest.fixture
def dbt_project(tmp_path):
    models_path = tmp_path / "models"
    models_path.mkdir()

    sources_yml = models_path / "sources.yml"
    sources_yml.touch()

    yaml_file = tmp_path / "schema.yml"
    yaml_file.write_text(sample_yaml_content)

    sql_file = models_path / "model1.sql"
    sql_file.write_text(sample_sql_content)

    return tmp_path


@pytest.fixture
def mock_generate_response():
    with patch.object(DbtModelProcessor, "suggest_dbt_model_improvements", autospec=True) as mock_function, \
         patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        mock_function.return_value = "Use ref() function instead of hardcoding table names."
        yield mock_function


@pytest.fixture
def mock_generate_response_advanced():
    with patch.object(DbtModelProcessor, "suggest_dbt_model_improvements_advanced") as mock_function, \
         patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        mock_function.return_value = "Use ref() function instead of hardcoding table names (advanced)."
        yield mock_function


@pytest.fixture
def mock_generate_models():
    with patch("dbt_ai.dbt.generate_models") as mock:
        mock.return_value = [
            "model_name: model_a\n\nSELECT *\nFROM {{ source('beautiful_source', 'organisation') }}\n",
            "model_name: model_b\n\nSELECT *\nFROM {{ source('beautiful_source', 'user') }}\n",
            "model_name: model_c\n\nSELECT a.industry, SUM(b.total) as total\nFROM {{ ref('model_a') }} a\nJOIN {{ ref('model_b') }} b\nON a.id = b.id\nGROUP BY a.industry",
        ]
        yield mock
