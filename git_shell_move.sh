#!/bin/bash

ORIGIN_LOCATION=$1
TARGET_LOCATION=$2
TARGET_URL=$3
TMP_REPO='./git_repo'

# Clone repository
git clone --mirror $ORIGIN_LOCATION $TMP_REPO
# Go into directory
cd $TMP_REPO
# Set new (target) remote
git remote set-url origin $TARGET_LOCATION
# Push to new remote
git push --mirror

# Remove mirrored repository
cd ../
rm -R $TMP_REPO
# Checkout non-mirrored
git clone $ORIGIN_LOCATION $TMP_REPO
cd $TMP_REPO
# Read current readme.md
ORIG_TEXT=$(cat README.md)
# Add notice of repo move
echo "**Repository location moved! Please check [$TARGET_URL]($TARGET_URL)**" | cat - README.md > README && mv README README.md
# Commit move of repo
git add README.md && git commit -m "Added repo move notice" && git push

cd ../
rm -r $TMP_REPO