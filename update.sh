#!/bin/bash

git add -u
commit_message="Update $(date +%Y-%m-%d)"
git commit -m "$commit_message"
git push origin master
