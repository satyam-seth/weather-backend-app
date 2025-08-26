# weather-backend-app

1. Create Virtual Environment

- if windows

  ```bash
  python -m venv .venv
  ```

- if mac or linux

  ```bash
  python3 -m venv .venv
  ```

2. Activate Virtual Environment

- if windows

  ```bash
  source .venv/Scripts/activate
  ```

- if mac or linux

  ```bash
  source .venv/bin/activate
  ```

- Note:- if you want to deactivate

  ```bash
  deactivate
  ```

3. Test Coverage

- Run tests with coverage

  ```sh
  coverage run manage.py test
  ```

- See coverage report on terminal

  ```sh
  coverage report
  ```

- Generate HTML report

  ```sh
  coverage html
  ```