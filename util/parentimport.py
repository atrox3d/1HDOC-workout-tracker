import sys
import os


def add_import_absolute_folder(folder):
    #
    #   hack to add external private data
    #
    absolute = os.path.abspath(folder)
    print(f"{__name__}: add {absolute} to sys.path")
    sys.path.insert(0, absolute)
    print(f"{__name__}: sys.path: {sys.path}")


def add_parent_import():
    #
    #   hack to add external private data
    #
    print(f"{__name__}: add .. to sys.path")
    sys.path.insert(0, "..")
    print(f"{__name__}: sys.path: {sys.path}")
