#!/bin/bash 


file= readlink -f src/main.py

echo "Creating folder locals"
echo "Creating SecuServe File Dirs"

echo "making main dir"
mkdir /mnt/SecuServe/
echo "making config dir"
mkdir /mnt/SecuServe/Config/
echo "making user folder"
mkdir /mnt/SecuServe/user/people/
echo "making logging dir"
mkdir /mnt/SecuServe/logging/
echo "making caughtImages dir"
mkdir /mnt/SecuServe/caughtImages/
echo "creating Caut images dir"
mkdir /mnt/SecuServe/caughtImages/Admin/
mkdir /mnt/SecuServe/caughtImages/User/
mkdir /mnt/SecuServe/caughtImages/Unwanted/
mkdir /mnt/SecuServe/caughtImages/Group/
mkdir /mnt/SecuServe/caughtImages/unknown/
echo "finished making dir"

echo "Starting SecuServe Security System UwU💗"

sudo OPENBLAS_CORETYPE=ARMV8 python3 $(readlink -f src/main.py)
