#!/bin/bash
#
# Made with a little help from Pat
#
qsub -t 1-64 -cwd -o "/dev/null" -e "/dev/null"  -l h_rt=00:20:00 postJobArray.sh "postProcInputs/postProcInput"