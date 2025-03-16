#!/bin/bash

BASE_URL="http://localhost:8000/search"

curl --get --data-urlencode "question=O que é o produto" "$BASE_URL"
echo -e "\n------------------------"