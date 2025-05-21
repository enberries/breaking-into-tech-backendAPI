#!/bin/bash
# Migration helper script
export FLASK_APP=api.py
export FLASK_ENV=development

flask db init
flask db migrate -m "Create user table"
flask db upgrade
