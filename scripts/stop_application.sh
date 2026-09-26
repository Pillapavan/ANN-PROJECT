#!/bin/bash

echo "Stopping existing ANN application..."

docker stop ann-project || true

docker rm ann-project || true

echo "Existing ANN application stopped."