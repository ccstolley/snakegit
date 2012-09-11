#!/usr/bin/env bash

[ "${NS_DEV_UTILS}xxx" == "xxx" ] && NS_DEV_UTILS=~/.snakegit

echo "Uploading file"
FILE_TO_UPLOAD=`ls -rt dist/|tail -1`
test "$FILE_TO_UPLOAD" == "" && echo "You must generate an sdist first using git sdist" && exit 1
echo "Uploading $FILE_TO_UPLOAD"
curl -k -F upload_file=@dist/$FILE_TO_UPLOAD -u `git config --get pypi.user` `git config --get pypi.scheme`://`git config --get pypi.host`/upload
