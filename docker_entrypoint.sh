#!/bin/sh

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback

USER_ID=${LOCAL_USER_ID:-9001}
USER_NAME="xwlunixuser"

echo "Starting with UID : $USER_ID"
useradd --shell /bin/bash -u $USER_ID -o -c "" -m $USER_NAME
export HOME=/home/user

su - $USER_NAME -p -c "/env/bin/python /app/run.py"
