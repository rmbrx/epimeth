# shell学习笔记

1. [简介](简介.md)

```shell
# 数值运算
index=0
for f in $(ls *.*.md|sort); do
    index=$((index+1))
done
```