#!/usr/bin/env bash
#
# This script assumes a linux environment

# Twitch-Channel-Points-Miner-v2 repository to download
# The original URL will be https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2
repo="rdavydov/Twitch-Channel-Points-Miner-v2"

# Create the tmp directory if it doesn't exist
mkdir -p tmp

# This script will download the repository as a tar file and extract the folder
# "TwitchChannelPointsMiner" automatically into the root directory.
curl -L https://api.github.com/repos/${repo}/tarball | tar -xz -C tmp --wildcards \
    "*/TwitchChannelPointsMiner" \
    "*/requirements.txt" \
    --strip-components=1

# Move requirements.txt into TwitchChannelPointsMiner
mv tmp/requirements.txt tmp/TwitchChannelPointsMiner/

# Finally move the TwitchChannelPointsMiner folder into the root directory
mv tmp/TwitchChannelPointsMiner .

# Clean up
rm -rf tmp