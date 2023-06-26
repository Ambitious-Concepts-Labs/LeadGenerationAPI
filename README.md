# Lead Generation API

<!-- Analytics app that gathers data from multiple social media platforms, organizes the data and then puts it into easy to understand data visualizations for content creators to get a better understanding of how their content is performing across social media platforms. Questions? [Email Us](trifecta1906@gmail.com) -->

- [Lead Generation API](#lead-generation-api)
  - [Getting Up and Running](#getting-up-and-running)
  - [Overview Details](#overview-details)
    - [Release History](#release-history)
    - [Contributing](#contributing)
    - [Python Packages](#python-packages)
  - [Resources](#resources)
  - [Running End-To-End Tests](#running-end-to-end-tests)
  - [Evidence of Test](#evidence-of-test)
  - [Unsolved Problems](#unsolved-problems)
  - [Future Enhancements](#future-enhancements)

## Getting Up and Running

Suggested setup

- [Virtual Env - venv](https://docs.python.org/3/library/venv.html)

  - Create virtual environment folder

  ```bash
  python3 -m venv venv
  ```

  - Activate VENV

  ```bash
  source venv/bin/activate
  ```

  - Install packages

  ```bash
  pip install -r requirements.txt
  ```

  - Added more packages>

  ```bash
  pip freeze > requirements.txt
  ```

  - Check Packages

  ```bash
  pip list --local
  ```

  - Deactivate VENV

  ```bash
  deactivate
  ```

  - Automatically Format Code

  ```bash
  black filename.py
  ```

  - Run Linter
  
  ```bash
  pylint main.py | pylint-json2html -o pylint.html
  ```

  - Sort Imports
  
  ```bash
  isort .
  ```

  Want to run locally checkout the [Requirements file](requirements.txt)

  - Run Locally

  ```bash
  uvicorn main:app --reload  
  ```

  The server is running on http://127.0.0.1:8000/

## Overview Details

### Release History

- 0.0.1
  - Work in progress

### Contributing

Review how here [contribution guide](CONTRIBUTION.md)

### Python Packages

- [Github Actions](https://docs.github.com/en/actions/quickstart)
- [Unittest](https://docs.python.org/3/library/unittest.html)
- [Pytest](https://docs.pytest.org/en/stable/warnings.html)
- [Prosector](https://github.com/PyCQA/prospector)
- [Mutpy](https://pypi.org/project/MutPy/)
- [XML Reporting](https://pypi.org/project/unittest-xml-reporting/)
- [Coverage.py](https://coverage.readthedocs.io/en/6.0/)
  
- [AWS Secret Manager](https://docs.aws.amazon.com/secretsmanager/index.html)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
  - AWS SDK
- [Black](https://github.com/psf/black)
- [CSV](https://docs.python.org/3/library/csv.html)
- [FastAPI](https://fastapi.tiangolo.com/)
- [iSort](https://github.com/PyCQA/isort)
- [Logging](https://docs.python.org/3/howto/logging.html/)
- [New Relic](https://one.R.com/dashboards?account=3991784&duration=1800000&state=952cfb48-9a21-39d6-f543-19b373e9cd69)
- [Outscraper](https://app.outscraper.com/api-docs#tag/Google-Maps/paths/~1maps~1search-v3/get)
- [Pylint](https://docs.pylint.org/)
- [Pylint Config](https://www.codeac.io/documentation/pylint-configuration.html)
- [Pylint-json2html](https://pypi.org/project/pylint-json2html/)
- [Redis](https://redis.readthedocs.io/en/stable/examples/set_and_get_examples.html)
- [Requests](https://docs.python-requests.org/en/master/)
  - Covers all of the code scenarios
  - If a test is present


## Resources

To view the docs checkout: https://analytics-ios.herokuapp.com/docs or https://analytics-ios.herokuapp.com/redoc

## Running End-To-End Tests

Run Pytest

```bash
pytest -v
```

Flags

- Disable the warnings
  - ```bash
    pytest -v --disable-warnings
    ```
- Adds prints statements
  - ```bash
    pytest -v -s
    ```
- Stops the tests if one fails
  - ```bash
    pytest -v -s -x
    ```

## Evidence of Test

| Report      | Pipline Job        | Location                                     |
|-------------|--------------------|----------------------------------------------|
| Debricked   | vulnerability-scan | https://debricked.com/app/en/dashboard       |
| Coverage.py | build              | htmlcov                                      |
| Unittest    | build              | TEST-tests.unittest.TestStringMethods-\*.xml |
| Prospector  | build              |                                              |

## Unsolved Problems

## Future Enhancements

- Lock down API with OAuth2

  - OAuth2 with Password (and hashing), Bearer with JWT tokens¶
  - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

- Allow users to manage their Youtube accounts with OAuth2.0
- Export with google sheets and pdfs
