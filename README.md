# Script to read and write bnr files from OPUS

Simple script that reads the bnr spectral files (to modify
the spectra then write them again for example)

There is already a script written by UCAR that 
does this, called bnc.c in the ckopus project,
but this one uses libc and makes the file 
size 4 times smaller than the original bnr
