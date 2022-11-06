#!/usr/bin/env bash

BASEDIR="$(cd ../ && pwd)"
DOCKER_DIR="${BASEDIR}/docker/"
ROS_DIR="${BASEDIR}/ros/"

function throwError () 
# args:
#   1) exit code to return
#   2) message to be printed to console
{
    local -i EXIT_CODE=$1
    local ERR_MSG=$2

    echo "[ERROR]: $(echo ${ERR_MSG})"
    exit ${EXIT_CODE}
}