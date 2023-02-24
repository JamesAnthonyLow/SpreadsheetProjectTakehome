#!/bin/bash
SOURCE_DIR="$(dirname "$0")"/..
IMAGE_NAME=spreadsheet_project_image

run_command(){
    docker build "$SOURCE_DIR" -t "$IMAGE_NAME"
    docker run --rm -it -v "$SOURCE_DIR":/workspace "$IMAGE_NAME" "$@"
}