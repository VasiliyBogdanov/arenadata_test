import os
from datetime import datetime as dt
from enum import Enum
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from tests.helpers.API import API

APP_ADDRESS = os.getenv("MAIN_APP_ADDRESS")
PATH_FOR_DRIVERS = Path.cwd().joinpath(Path("browser_drivers/"))
PATH_FOR_SCREENSHOTS = Path.cwd().joinpath(Path("screenshots/"))


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


def dir_exists(path: Path):
    if Path.exists(path) and Path.is_dir(path):
        return True
    return False

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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def chrome_driver(request):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(path=PATH_FOR_DRIVERS).install()),
                              options=chrome_options)
    yield driver
    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            driver.execute_script("document.body.bgColor = 'white';")

            # Save screenshot for local debug
            if not dir_exists(PATH_FOR_SCREENSHOTS):
                os.mkdir(PATH_FOR_SCREENSHOTS)

            driver.get_screenshot_as_file(
                str(PATH_FOR_SCREENSHOTS) + os.sep +
                str(request.node.name) + str(dt.today().strftime('__%Y-%m-%dT%H-%M-%S%f%z')) + '.png')
            # Attach screenshot to Allure report:
            allure.attach(driver.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)

            # For happy debugging:
            print('URL: ', driver.current_url)
            print('Browser logs:')
            for log in driver.get_log('browser'):
                print(log)

        except Exception as e:
            print(e)

    driver.quit()
