#!/usr/bin/env python

pip install reportlab
pip install PyPdf2

rm -r -f temp
rm -r -f output

mkdir temp
mkdir output

python main.py

rm -r -f temp