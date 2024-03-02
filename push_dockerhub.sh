#!/bin/bash

docker login
docker build -t araujo88/galharufa-backend:1.0.0 .
docker push araujo88/galharufa-backend:1.0.0