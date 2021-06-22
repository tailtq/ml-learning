#!/bin/bash

python app/db/migrations/01_create_faces_table.py
python app/db/migrations/02_create_attendances_table.py
