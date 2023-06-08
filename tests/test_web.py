import allure

from conftest import TEMPLATES

from .helpers.pages.main_page import MainPage


@allure.suite("UI tests")
@allure.sub_suite("Main Page")
class Test_MainPage():

    def test_enabled_button(self, api, chrome_driver):
        """Enabled button should be visible and clickable"""
        template = TEMPLATES.valid_parent_and_children
        page = MainPage(chrome_driver, api, template)
        enabled_button = page.valid_parent

        assert enabled_button.is_visible() == True
        assert enabled_button.is_clickable() == True

    def test_enabled_button_link(self, api, chrome_driver):
        """Clicking enabled button should result in moving to address in the 'link' field"""
        template = TEMPLATES.valid_parent_and_children
        page = MainPage(chrome_driver, api, template)
        enabled_button = page.valid_parent

        enabled_button.click()
        page.wait_page_loaded()
        page_address = page.get_current_url()

        assert page_address == "https://www.google.com/"

    def test_disabled_button(self, api, chrome_driver):
        """Disabled button should not be clickable"""
        template = TEMPLATES.valid_parent_and_children
        page = MainPage(chrome_driver, api, template)
        disabled_button = page.valid_child_2

        classes = disabled_button.get_attribute("class")

        assert "disabled" in classes
