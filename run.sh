set -x
set -e
set -o allexport
source .env
set +o allexport


docker compose build
docker compose up
