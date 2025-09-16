#!/bin/sh

pip install --upgrade pip

echo "----------"
echo "Installing requirements"

pip install -r requirements.txt

echo "----------"
echo "Notebook dependencies"

pip install ipympl ipykernel

echo "=========="
python -m pip --version
docker --version
docker compose version
date
