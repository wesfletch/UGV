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

echo "Loading package list from file: ${FILE:-${DEFAULT_FILE}}"

# packages="$(cat ${FILE:-${DEFAULT_FILE}})"
readarray -t packages < ${FILE:-${DEFAULT_FILE}}
sudo apt install -y "${packages[@]}"