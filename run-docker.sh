#!/bin/bash

docker rm web-xwl

docker run -p 8000:5000 --name web-xwl \
	-e LOCAL_USER_ID=`id -u $USER` \
	-e XWL_ROOT_URL="http://xwl.me/"
	-v $PWD:/dbpath/ xwl
