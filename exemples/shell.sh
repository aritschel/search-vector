#!/bin/bash

BASE_URL="http://localhost:8000/search"

curl --get --data-urlencode "question=O que é a Hotmart" "$BASE_URL"
echo -e "\n------------------------"