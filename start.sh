#!/bin/bash
rasa run actions --port 5055 &
rasa run --enable-api --cors "*" --port 5005
