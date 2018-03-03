#!/usr/bin/env bash

cd ~/git/andreaskdk/robo
export FLASK_APP=command/server.py
python -m flask run --host=0.0.0.0
