#!/usr/bin/env bash

git reset --hard origin/main
git pull origin main
git submodule update --init --recursive

pip install -e vendors/pysecur3
pip install -e .