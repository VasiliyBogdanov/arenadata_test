import os
from enum import Enum
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from tests.helpers.API import API

APP_ADDRESS = os.getenv("MAIN_APP_ADDRESS")
PATH_FOR_DRIVERS = Path().cwd().joinpath(Path("browser_drivers/"))


class TEMPLATES(Enum):
    minimum_valid = Path("./tests/test_data/yaml_files/minimum_valid.yaml")
    without_id_field = Path(
        "./tests/test_data/yaml_files/without_id_field.yaml")
    without_label_field = Path(
        "./tests/test_data/yaml_files/without_label_field.yaml")
    with_nonexistent_parent_element = Path(
        "./tests/test_data/yaml_files/with_nonexistent_parent_element.yaml")
    with_empty_label = Path(
        "./tests/test_data/yaml_files/with_empty_label.yaml")
    with_empty_id = Path(
        "./tests/test_data/yaml_files/with_empty_id.yaml")
    correct_yaml_without_extension = Path(
        "./tests/test_data/yaml_files/correct_yaml_without_extension")
    pdf_extension = Path("./tests/test_data/yaml_files/pdf_extension.pdf")
    empty = Path("./tests/test_data/yaml_files/empty.yaml")
    valid_parent_and_children = Path(
        "./tests/test_data/yaml_files/valid_parent_and_children.yaml")
    parent_and_child_with_the_same_id = Path(
        "./tests/test_data/yaml_files/parent_and_child_with_the_same_id.yaml")
    without_label_with_link = Path(
        "./tests/test_data/yaml_files/without_label_with_link.yaml")


POPULATE_DATA: list[TEMPLATES] = [item for item in TEMPLATES if item.name not in (
    TEMPLATES.correct_yaml_without_extension.name, TEMPLATES.pdf_extension.name)]

# Helper functions


def cleanup(api):
    templates = api.get_templates()
    for tmpl_id in templates.json().get("templates"):
        api.delete_template(tmpl_id)


def get_resp_message(resp):
    return resp.json().get("message")


def get_templates_message(resp):
    return resp.json().get("templates")

# end of helper functions


@pytest.fixture(scope="session")
def api():
    return API(APP_ADDRESS)


@pytest.fixture(autouse=True)
def clean_up_templates(api):
    """Cleanup before every test."""

    cleanup(api)


@pytest.fixture
def populate_with_test_data(api):
    for elem in [i.value for i in POPULATE_DATA]:
        api.post_template(elem)


@pytest.fixture(scope="session", autouse=True)
def clean_up_templates_after_all_tests(api):
    """Cleanup after all tests."""

    yield
    cleanup(api)


@pytest.fixture
def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(path=PATH_FOR_DRIVERS).install()),
                              options=chrome_options,)
    yield driver
    driver.quit()
