import os

from .base import WebPage
from .elements import WebElement


class MainPage(WebPage):

    def __init__(self, web_driver, api, template, url=''):
        if not url:
            url = os.getenv("MAIN_APP_ADDRESS")

        api.post_template(template.value)
        api.install_template(template.name)

        super().__init__(web_driver, url)

    valid_parent = WebElement(css_selector="#valid_parent")

    valid_child_2 = WebElement(css_selector="#valid_child_2")
