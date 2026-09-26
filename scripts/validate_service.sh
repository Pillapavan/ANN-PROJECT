#!/bin/bash

set -e

echo "Validating ANN application..."

sleep 10

curl --fail http://localhost:8501

echo "ANN application validation successful."