from cppmake.system.all import system
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.usage = "cppmake [path] [options...]"
parser.formatter_class = lambda *args, **kwargs: argparse.HelpFormatter(*args, max_help_position=32, width=os.get_terminal_size().columns, **kwargs)
parser.add_argument("path",       nargs='?',                            default='.',                  help= "Specify your project path (example: ., .., path/to/my/project; default: .).")
parser.add_argument("--compiler",                                       default=system.compiler_path, help=f"Use specific C++ compiler (example: g++, /usr/bin/g++, /opt/homebrew/clang++; default: {system.compiler_path}).")
parser.add_argument("--std",      choices=["c++20", "c++23", "c++26"],  default="c++26",              help= "Use specific C++ standard (default: c++26).")
parser.add_argument("--type",     choices=["debug", "release", "size"], default="debug",              help= "Choose build config type  (default: debug).")
parser.add_argument("--parallel", type   =lambda n: int(n),             default=os.cpu_count(),       help=f"Allow maximun concurrency (default: {os.cpu_count()}).")
parser.add_argument("--verbose",  action ="store_true",                 default=False,                help= "Show verbose build info.")
config = parser.parse_args()

sys.dont_write_bytecode = True
os.chdir(config.path)