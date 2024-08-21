v  = input("tag: ")

from os import system
from os import system, remove, path
from time import sleep
import sys

system('docker build  . -t  ggbr12/arbspro:' + v)
system('docker push  ggbr12/arbspro:' + v)