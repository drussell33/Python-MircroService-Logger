#!/usr/bin/env bash
export FLASK_APP=app.py
export FLASK_ENV=development
export DB='wolfit_activity_log'
export DB_USER='admin-derek'
export DB_PASSWORD='yXgR1K9tSXciFodd'
export DB_HOST='mongodb+srv://admin-derek:yXgR1K9tSXciFodd@microservices407.pdlfu.mongodb.net/wolfit_activity_log?retryWrites=true&ssl_cert_reqs=CERT_NONE'
export SLEEP_TIME=50
flask run --host=0.0.0.0 --port $@