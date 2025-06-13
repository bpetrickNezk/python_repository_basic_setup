
set -e 

# install all packages from the uv.lock file without updating the .lock file
uv sync --all-groups --frozen
uv run pre-commit install --install-hooks