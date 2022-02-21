#!/usr/bin/env bash
#
# This script assumes a linux environment

function compile {
    echo "Compiling..."

    #* Currently, I'm using the spec file to rename the executable with the OS and architecture
    #* Yes, the spec file is a python script
    pyinstaller TwitchFarm.spec

    #* You can use the inline script to compile, but will replace the spec file
    #* thus removing the custom build name
    # pyinstaller TwitchFarm.py --name "TwitchFarm" --onefile --console --clean

    # Remove the Build folder
    rm -r "build"
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
    echo "If you want to ingonre this warning, pass '--ignore-warning' as argument."
    echo ""
    exit 1

else
    echo ""
    echo "VIRTUAL_ENV is set"
    compile
    echo ""
    exit 0
fi
