#!/usr/bin/env bash

for prj in "mapdb" "oryx" "netty" "elasticsearch" "orientdb"
do
    python3.4 deterministicy_check.py git_url=/home/geryxyz/repos/${prj}.git source_path=/home/geryxyz/stability/${prj}/source output_path=/home/geryxyz/stability/${prj}/result
done
