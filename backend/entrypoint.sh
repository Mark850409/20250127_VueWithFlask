#!/bin/bash
echo "$FIREBASE_CONFIG" > /usr/src/app/config/firebase-adminsdk.json
python app.py 