test:
	@pytest -vvs
test_api:
	@pytest -vvs tests/test_api.py
test_web:
	@pytest -vvs tests/test_web.py
test_and_report:
	@pytest -vvs --alluredir=./allure_reports
show_allure:
	@allure serve ./allure_reports

.PHONY: test test_api test_web show_allure test_and_report