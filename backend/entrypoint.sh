#!/bin/bash
echo "$FIREBASE_CONFIG" > /usr/src/app/config/firebase-adminsdk.json
ls -la /usr/src/app/config/firebase-adminsdk.json || exit 1
python app.py 