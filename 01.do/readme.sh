#!/bin/bash

# get the directory where the script file is located
curdir=$(
    cd "$(dirname "$0")" || exit
    pwd
)
cd ${curdir}
filename=README.md
echo -e "# 实践" > $filename

md_data=""
for f in $(ls *.*.md|sort); do
    # index=$(echo $f | awk -F '.' '{print $1}')
    fname=$(echo $f | awk -F '.' '{print $2}')
    md_data="${md_data}\n1. [${fname}](${f})"
done

echo -e $md_data >> $filename