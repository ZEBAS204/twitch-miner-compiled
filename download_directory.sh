#!/usr/bin/env bash
#
# This script assumes a linux environment

# Twitch-Channel-Points-Miner-v2 repository to download
# The original URL will be https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2
repo="rdavydov/Twitch-Channel-Points-Miner-v2"

# This script will download the repository as a tar file and extract the folder
# "TwitchChannelPointsMiner" automatically into the root directory.
curl -L https://api.github.com/repos/${repo}/tarball | tar xz --wildcards "*/TwitchChannelPointsMiner" --strip-components=1
