#!/usr/bin/env bash

pip install -r webapp/requirements.txt
export PYTHONPATH=$PWD/texttemplatematcher:$PYTHONPATH
cd webapp
python app.py