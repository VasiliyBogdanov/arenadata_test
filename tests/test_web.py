from conftest import TEMPLATES

from .helpers.pages.main_page import MainPage


def test_enabled_button(api, chrome_driver):
    template = TEMPLATES.valid_parent_and_children
    page = MainPage(chrome_driver, api, template)
    enabled_button = page.valid_parent

    assert enabled_button.is_visible() == True
    assert enabled_button.is_clickable() == True


def test_enabled_button_link(api, chrome_driver):
    template = TEMPLATES.valid_parent_and_children
    page = MainPage(chrome_driver, api, template)
    enabled_button = page.valid_parent

    enabled_button.click()
    page.wait_page_loaded()
    page_address = page.get_current_url()

    assert page_address == "https://www.google.com/"


def test_disabled_button(api, chrome_driver):
    template = TEMPLATES.valid_parent_and_children
    page = MainPage(chrome_driver, api, template)
    disabled_button = page.valid_child_2

    classes = disabled_button.get_attribute("class")

    assert "disabled" in classes
