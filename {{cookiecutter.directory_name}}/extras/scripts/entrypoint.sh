#!/usr/bin/env bash
set -e
echo $1
case $1 in
web)
  echo "Deploy web"
  alembic upgrade head
  gunicorn -w ${WORKERS:-4} -b 0.0.0.0:5000 ssf.__main__:app --timeout=1200  --log-level=${LOG_LEVEL:-debug}
  ;;
*)
  echo "Fail!"
  ;;
esac
