#!/bin/bash
cd /home/fenics/acc11/Cloud-Computing-Airfoil
celery -A tasks worker --loglevel=info --concurrency=1 -Ofair -E -n celery@worker_name &
# cd /home/fenics/acc11/Cloud-Computing-Airfoil/docker_container
# python py_airfoil.py
