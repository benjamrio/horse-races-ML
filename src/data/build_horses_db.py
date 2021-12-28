#!/usr/bin/env python
# coding : utf-8

import pandas as pd
import json
from os import listdir
from os.path import isfile, join
import timeit
from utils import flatten_dic

import os

# the path to the directory of the data
# dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = "E:\\MyData\\KLAP\\"


def main():
    """
    Gather all data from the first year into a data lake
    """
    print(
        "Il y a %d fichiers de course dans le dossier %s"
        % (
            len(listdir(dir_path + "Raw\\2010-2019-races")),
            dir_path + "Raw\\2010-2019-races",
        )
    )
    frames = []
    for file in listdir(dir_path + "Raw\\2010-2019-races"):
        # if not file.startswith('2010'):
        #    break
        with open(
            dir_path + "Raw\\2010-2019-races\\" + file, encoding="utf-8"
        ) as json_file:
            data = json.load(json_file)
        frames += [flatten_dic(cheval) for cheval in data["partants"]]

    result = pd.DataFrame(frames)
    result.to_csv(dir_path + "CleanData\\horses.csv", encoding="utf-8", sep=";")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("CSV created at path %s" % dir_path + "\\CleanData\\horses.csv")
    print("Time to process:", stop - start)

