#!/usr/bin/env python
# coding : utf-8

import pandas as pd
import json
from os import listdir
from os.path import isfile, join
import timeit
from collections import Counter
import matplotlib.pyplot as plt
import os
from utils import flatten_dic

# the path to the directory of the data
# dir_raw_data = os.path.dirname(os.path.realpath(__file__))
dir_raw_data = "data/raw/2010-2019-races/"


def main():
    """
    Gather all data from horses' performances  from each year into a csv file
    """
    print(
        "Il y a %d fichiers de course dans le dossier %s"
        % (len(listdir(dir_raw_data)), dir_raw_data,)
    )
    frames = []
    year = "2010"

    for file in listdir(dir_raw_data):
        # Lors d'un changement d'année, on exporte le dataframe.
        # Hypothèse : les fichiers sont dans l'ordre alphabétique (=chronologique)
        if file[:4] != year:
            year = save_df(frames, file, year)

        with open(dir_raw_data + file, encoding="utf-8") as json_file:
            data = json.load(json_file)
            frames += [flatten_dic(cheval) for cheval in data["partants"]]

    save_df(frames, file, year)


def save_df(frames, file, year):
    """Save the dataframe to a csv file, while returning the next year

    Arguments:
        frames {DataFrame} -- DataFrame containing all info from the last year
        file {String} -- The string name file of the new year file
        year {String} -- Current year of dataframe infos
    Returns the next year of files
    """
    resultYear = pd.DataFrame(frames)
    resultYear.to_csv("data\\interim\\horses%s.csv" % year, encoding="utf-8", sep=";")
    frames = []
    print(
        "CSV for year %s created at path %s"
        % (year, "data\\interim\\horses%s.csv" % year)
    )
    return file[:4]


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time to process:", stop - start)
    # 700 seconds to process
