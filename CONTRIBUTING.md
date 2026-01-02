# Contributing to Fetal Plane Explorer

Thank you for your interest in contributing to Fetal Plane Explorer! We welcome contributions from the community to help improve this research demo.

## Development Setup

You can develop using Docker or a local environment.

### Docker (Recommended)

1.  Ensure you have Docker and Docker Compose installed.
2.  Run the full stack:
    ```bash
    docker-compose -f infra/docker-compose.yml up --build
    ```

### Local Environment

**Backend:**
1.  Python 3.12+ is required.
2.  Install dependencies:
    ```bash
    cd backend
    pip install -e ".[dev]"
    ```
3.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

**Frontend:**
1.  Node.js 20+ is required.
2.  Install dependencies:
    ```bash
    cd frontend
    npm install
    ```
3.  Run the dev server:
    ```bash
    npm run dev
    ```

## Code Style

We enforce strict code style and static analysis to maintain repository health.

### Backend (Python)
-   **Formatting**: We use `ruff` for formatting.
-   **Linting**: We use `ruff` for linting.
-   **Typing**: We use `mypy` for static type checking.

Run checks:
```bash
ruff check .
ruff format --check .
mypy app/
```

### Frontend (TypeScript)
-   **Formatting**: We use `prettier`.
-   **Linting**: We use `eslint`.

Run checks:
```bash
npm run lint
npm run format:check
```

## Testing

### Backend
We use `pytest`. All new features must include unit tests.

```bash
pytest tests/
```

### Frontend
We use `vitest` for unit tests and `playwright` for smoke/E2E tests.

```bash
npm run test
npm run test:e2e
```

## Pull Request Process

1.  Fork the repository and create your branch from `main`.
2.  If you've added code that should be tested, add tests.
3.  Ensure the test suite passes.
4.  Make sure your code lints.
5.  Update the documentation.
6.  Submit the Pull Request.

## Commits

We prefer squash commits for PRs. Please write clear, descriptive commit messages. No emojis in commit messages please.

## License

By contributing, you agree that your contributions will be licensed under its Apache-2.0 License.
