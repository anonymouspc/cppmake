from cppmakelib.system.all       import system
from cppmakelib.utility.optional import value_or
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.usage = "cppmake [project] [options...]"
parser.formatter_class = lambda *args, **kwargs: argparse.HelpFormatter(*args, max_help_position=32, width=value_or(lambda: os.get_terminal_size().columns, 64), **kwargs)
parser.add_argument("project",       nargs='?',                         default='.',                  help=f"path to your C++ project  (example: ., .., /home/me/project; requires: contains cppmake.py; default: .).")
parser.add_argument("--target",                                         default="make",               help=f"run target in cppmake.py  (example: make, build, test; requires: defined in cppmake.py; default: make).")
parser.add_argument("--compiler",                                       default=system.compiler_path, help=f"use specific C++ compiler (example: g++, /usr/bin/g++, /opt/homebrew/clang++; requires: executable; default: {system.compiler_path}).")
parser.add_argument("--std",      choices=["c++20", "c++23", "c++26"],  default="c++26",              help=f"use specific C++ standard (default: c++26).")
parser.add_argument("--type",     choices=["debug", "release", "size"], default="debug",              help=f"choose build config type  (default: debug).")
parser.add_argument("--parallel", type   =lambda n: int(n),             default=os.cpu_count(),       help=f"allow maximun concurrency (default: {os.cpu_count()}).")
parser.add_argument("--verbose",  action ="store_true",                 default=False,                help=f"show verbose make outputs.")
config = parser.parse_args()

sys.dont_write_bytecode = True
os.chdir(config.project)