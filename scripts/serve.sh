#!/usr/bin/env bash

cd ~/git/andreaskdk/robo
export FLASK_APP=command/server.py
flask run --host=0.0.0.0
