#!/bin/bash 



echo "Starting SecuServe Security System UwU💗"

sudo OPENBLAS_CORETYPE=ARMV8 python3 -m cProfile  -o test1.pstats $(readlink -f src/main.py)
