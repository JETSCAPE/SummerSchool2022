#!/bin/bash
fileid="1lBL5OPf4s-Eiepd73gzkIm1FDayiQg_m"
filename="data.tar.gz"
html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o ${filename}

tar -xzf data.tar.gz
