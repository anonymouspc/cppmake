from cppmakelib import *

def main():
    main_package.is_built()
    getattr(main_package.cppmake, config.target)()