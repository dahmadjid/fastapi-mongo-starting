set -o allexport
source .env
set +o allexport

uvicorn src.main:app --reload --host 0.0.0.0
