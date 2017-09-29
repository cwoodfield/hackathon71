#!/bin/bash

for x in leaf spine vmx
do
  for y in YAML/$x*
  do
    cf=$(basename -s .yaml $y).conf
    ./template_gen.py TEMPLATES/${x}_template.j2 $y > CONFIGS/$cf
  done
done
