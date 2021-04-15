#!/bin/bash 

echo "Starting SecuServe Security System UwU💗"
file= readlink -f src/__init__.py

sudo OPENBLAS_CORETYPE=ARMV8 python3 $(readlink -f src/__init__.py)
