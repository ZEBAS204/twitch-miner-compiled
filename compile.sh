#!/usr/bin/env bash
#
# This script assumes a linux environment

function compile {
    echo "Compiling..."

    #* Currently, I'm using the spec file to rename the executable with the OS and architecture
    #* Yes, the spec file is a python script
    python -m PyInstaller TwitchFarm.spec

    # Remove the Build folder
    rm -rf "build"
}

if [[ -z "$VIRTUAL_ENV" ]]; then
    echo ""
    echo "No VIRTUAL_ENV detected"

    if [[ $1 =~ --ignore-warning ]]; then
        compile
        exit 0
    fi

    echo "Compiling should be performed inside of a virtual environment" \
        "to prevent errors and reduce bundle size."
    echo "If you want to ignore this warning, pass '--ignore-warning' as an argument."
    echo ""
    exit 1

else
    echo ""
    echo "VIRTUAL_ENV is set"
    compile
    echo ""
    exit 0
fi
