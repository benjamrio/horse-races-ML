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
# dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = "E:\\MyData\\KLAP\\"
FIRST_YEAR = 2010
LAST_YEAR = 2014


def main():
    """
    Gather all data from each year into a csv file
    """
    print(
        "Il y a %d fichiers de course dans le dossier %s"
        % (
            len(listdir(dir_path + "Raw\\2010-2019-races")),
            dir_path + "Raw\\2010-2019-races",
        )
    )
    frames = []
    """
    yearsCount = Counter([course[:4] for course in listdir(dir_path+"Raw\\2010-2019-races")])
    print(yearsCount)
    plt.bar(yearsCount.keys(), yearsCount.values())
    plt.ylabel("Nombre de courses")
    plt.title("Data disponible par année")
    plt.show()
    """
    year = "2010"
    resultYear = pd.DataFrame({})

    for file in listdir(dir_path + "Raw\\2010-2019-races"):
        # Lors d'un changement d'année, on exporte le dataframe.
        # Hypothèse : les fichiers sont dans l'ordre alphabétique (=chronologique)
        if file[:4] != year:
            resultYear = pd.DataFrame(frames)
            resultYear.to_csv(
                dir_path + "CleanData\\horses%s.csv" % year, encoding="utf-8", sep=";"
            )
            frames = []
            print(
                "CSV for year %s created at path %s"
                % (year, dir_path + "CleanData\\horses%s.csv" % year)
            )
            year = file[:4]

        with open(
            dir_path + "Raw\\2010-2019-races\\" + file, encoding="utf-8"
        ) as json_file:
            data = json.load(json_file)
        frames += [flatten_dic(cheval) for cheval in data["partants"]]


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time to process:", stop - start)


"""
First method : 3mins to concatenate all the data : copie du df à chaque ajout
Deuxième methode : 26 secondes ! mais des opérations a priori inutiles (transposée, etc)
Troisième méthode : 0.5 secondes !! masterclass. 8 fois plus long sur un HDD que sur un SSD.
1 mois = 4sec
10 ans = 500sec

Un mois = 16MB
Un an = 200MB
10 ans = 2GB
"""
