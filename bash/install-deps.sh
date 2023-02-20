#!/usr/bin/env bash

source "./common.sh"

function usage ()
{
cat <<EOF
Under construction.
EOF
}

DEFAULT_FILE="packages.list"

while (( "$#" ))
do
    case "${1}" in 
        -f|--file)
            FILE="${2}"
            shift 2
            ;;
        -h|--help)
            usage
            shift 1
            ;;
        "")
            echo "No argument provided."
            echo usage
            shift 1
            ;;
        *)
            throwError 1 "Argument not supported: ${ARG}"
            shift 1
            ;;
    esac
done

for LIST in ./*.list; do
    echo "Loading package list from file: ${LIST:-}"

    readarray -t packages < ${LIST:-}
    sudo apt install -y "${packages[@]}"
done

