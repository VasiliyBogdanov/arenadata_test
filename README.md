## This is test task for QA Automation position in Arenadata

### Installation
#### Required python version ```^3.6``` - found using [Vermin](https://github.com/netromdk/vermin)
 - install and run app to test from [https://github.com/dgusakov/test_app](https://github.com/dgusakov/test_app)
 - clone or download this repo
 - from project directory:
    - create virtual environment. For example, ```python -m venv .venv```
    - activate it ```source .venv/bin/activate```
    - install dependencies ```pip3 install -r requirements.txt```
    - install allure [https://docs.qameta.io/allure/](https://docs.qameta.io/allure/)
### Configuration
If you use port other than 5000, update ```pytest.ini```\
There are several constants in ```conftest```:\
```PATH_FOR_DRIVERS``` - folder, where webdrivers will be installed. Default is ```browser_drivers``` in project root.\
```PATH_FOR_SCREENSHOTS``` - folder, where screenshots made by Selenium will be stored. Default is ```screenshots``` in project root.\
You can change ```allure reports``` location directly in command line argument, see below.
### Running tests
#### API tests
```
pytest tests/test_api.py
```
#### Web tests
```
pytest tests/test_web.py
```
#### Test and generate allure report
```
pytest --alluredir=./allure_reports
```
#### Show allure reports
```
allure serve ./allure_reports
```
#### There's also Makefile with these commands
### Useful flags
```-v``` verbose output\
```-vv``` even more verbose output\
```-s``` show print() statements in test output\
```-k``` select tests by some keyword expression. Refer to pytest docs for more detailed explanation

Recommended way to run tests is:
```
pytest -vvs
```
```base.py```, ```elements.py``` (Page Object Model) were used from this repository, check it out [https://github.com/TimurNurlygayanov/ui-tests-example](https://github.com/TimurNurlygayanov/ui-tests-example)