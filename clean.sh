#!/usr/bin/env bash
#
# This script assumes a linux environment

# Directories to remove
folders=('analytics' 'assets' 'build' 'cookies' 'logs')

for f in "${folders[@]}"; do
    [[ -d "$f" ]] && rm -r "$f" || echo "${f^^}: not found"
done
