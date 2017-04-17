from importlib import import_module
from os import listdir
from os.path import isfile, join

commands = {}

for f in listdir('.'):
    if isfile(join('.', f)):
        mod = import_module(f)
        commands[f[:-3]] = mod.exports
