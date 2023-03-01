#!/bin/bash

conda activate ml
dir=/Users/johannbrehmer/work/projects/manifold_flow/manifold-flow
cd $dir/experiments

for i in 0 1 2
do
    # python evaluate.py -c configs/evaluate_pie_celeba_april.config -i $i
    python evaluate.py -c configs/evaluate_pie_celeba_may.config -i $i
done
