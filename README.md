# Weather Backend App

A Django REST Framework backend for accessing climate datasets from the UK MetOffice.

## 🚀 Access Deployed Project

- [Admin Panel](https://weatherapi.pythonanywhere.com/admin/)
- [Browsable API](https://weatherapi.pythonanywhere.com/api/climate/)
- [Swagger UI](https://weatherapi.pythonanywhere.com/api/schema/swagger-ui/)
- [ReDoc](https://weatherapi.pythonanywhere.com/api/schema/redoc/)
- [Download OpenAPI Schema](https://weatherapi.pythonanywhere.com/api/schema/)

## Local Setup

1. Create Virtual Environment

```sh
python3 -m venv .venv
```

2. Activate Virtual Environment

```bash
source .venv/bin/activate
```

3. Install Required Dependencies

```sh
pip install -r requirements.txt
```

4. Apply Migrations

```sh
python3 manage.py migrate
```

5. Create `.env` file and add required environment variables

```env
MANAGE_PY_PATH=manage.py
SECRET_KEY="<django-secret-key>"
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

6. Load climate data from UK MetOffice

```sh
python3 manage.py load_datasets
```

7. Run server

```sh
python3 manage.py runserver
```

## Development

1. Test Coverage

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

2. Run mypy type checking

```sh
mypy .
```

3. Fix formatting using black

```sh
black .
```

4. Sort imports using isort

```sh
isort --profile black --check-only .
```

5. Run pylint for code quality checks

```sh
pylint **/*.py
```

6. Pre Commit Hook

- Install pre commit dependencies

  ```sh
  pre-commit install
  ```

- Run pre-commit hooks manually

  ```sh
  pre-commit run --all-files
  ```

7. Setup pre push hook

```sh
cp .githooks/pre-push .git/hooks/pre-push && chmod +x .git/hooks/pre-push
```

8. Install recommended VS Code extensions

- Open the extensions sidebar in VS Code `ctrl+shift+x` or `cmd+shift+x`

- Type @recommended in the search bar

- Install the recommended extensions

9. Setup VS Code test runner

- Add manage.py path variable in `.env` file

  ```env
  MANAGE_PY_PATH=manage.py
  ```

10. Load climate data from UK MetOffice

```sh
python3 manage.py load_datasets
```

11. Generating OpenAPI Schema

```sh
python3 manage.py spectacular --validate --color --file schema.yml
```

12. Setup required environment variables for github workflow

<img width="1400" height="470" alt="image" src="https://github.com/user-attachments/assets/eb0a4fe3-afb4-4ca6-80aa-6e61ad58143f" />

13. Create super user

```sh
python manage.py createsuperuser
```

# Use docker for development

1. Build and start containers

```sh
docker-compose -f docker-compose.dev.yml up --build
```

2. Start in detached mode

```sh
docker-compose -f docker-compose.dev.yml up -d
```

3. Stop containers

```sh
docker-compose -f docker-compose.dev.yml down
```

4. Open a shell inside backend service container

```sh
docker-compose -f docker-compose.dev.yml exec backend bash
```

- Note: Run any Django command inside the container

```sh
python manage.py <command>
```

- Shortcut without opening shell

```sh
docker-compose -f docker-compose.dev.yml exec backend python manage.py <command>
```

5. See backend service container logs

```sh
docker-compose -f docker-compose.dev.yml logs -f backend
```

6. Restart backend service

```sh
docker-compose -f docker-compose.dev.yml restart backend
```
