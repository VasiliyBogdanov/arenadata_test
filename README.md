## This is test task for QA Automation position in Arenadata

### Installation
#### Required python version ```^3.6``` - found using [Vermin](https://github.com/netromdk/vermin)
If you use port other than 5000, update ```pytest.ini```\
You can also change folder, where webdriver will be installed, in ```conftest``` ```PATH_FOR_DRIVERS``` variable. Default is ```browser_drivers``` in project folder.
 - install and run app to test from [https://github.com/dgusakov/test_app](https://github.com/dgusakov/test_app)
 - clone or download this repo
 - from project directory:
    - create virtual environment. For example, ```python -m venv .venv```
    - activate it ```source .venv/bin/activate```
    - install dependencies ```pip3 install -r requirements.txt```

### Running tests
#### API tests
```
pytest tests/test_api.py
```
#### Web tests
```
pytest tests/test_web.py
```
#### Useful flags
```-v``` verbose output\
```-vv``` even more verbose output\
```-s``` show print() statements in test output\
```-k``` select tests by some keyword expression. Refer to pytest docs for more detailed explanation

Recommended way to run tests is:
```
pytest -vvs
```