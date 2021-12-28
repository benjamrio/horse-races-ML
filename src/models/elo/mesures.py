#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import timeit
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metrics.metriques import *
from elo.database_elo import *
from metrics.metriques import *

print(ELO_INITIAL)

first_year = 2010
last_year = 2018
nb_metriques = 3
nb_modeles = 3


def calcule_metrique_modele(year, modele):
    counter = 0
    nom_fichier = FILEPATH_DATA + "horses" + str(year) + ".csv"
    courses = pd.read_csv(nom_fichier, sep=";")[
        [
            "raceId",
            "horse_genyId",
            "horse_name",
            "results_position",
            "odds_pmu_reference10h_ratio",
        ]
    ]

    by_race = courses.groupby("raceId")
    metrics_array = np.zeros((len(by_race), 3))

    for race, race_data in by_race:
        if modele == "ref10h":
            preds = race_data["odds_pmu_reference10h_ratio"].values
            res = race_data["results_position"].values
            arrivees = np.count_nonzero(~np.isnan(np.array(res)))
            res_no_nan = np.nan_to_num(res, nan=(arrivees + len(res)) / 2)
            res_preds_real = transforme_preds_classement(
                preds, res_no_nan, croissant=False
            )

        if modele == "random":
            res_preds_real = np.random.permutation(np.arange(1, len(race_data)))

        metrics_array[counter, :] = [
            NDCG(res_preds_real),
            eDCG(res_preds_real),
            winner(res_preds_real),
        ]
        counter += 1
    return np.mean(metrics_array, axis=0)


def calcule_metriques(
    first_year, last_year,
):
    metriques = np.zeros((nb_modeles, nb_metriques, last_year - first_year + 1))
    for year in range(first_year, last_year + 1):
        initialisation_nvx_elos(year)
        metriques[0, :, year - first_year] = calcule_elo(year)
        metriques[1, :, year - first_year] = calcule_metrique_modele(
            year, modele="ref10h"
        )
        metriques[2, :, year - first_year] = calcule_metrique_modele(
            year, modele="random"
        )
        np.savetxt(
            "metriques_array" + str(year) + ".csv",
            metriques[:, :, year - first_year],
            delimiter=";",
        )
    print(metriques)
    return metriques


def plot_metriques(first_year, last_year):
    metriques = calcule_metriques(first_year, last_year)
    for i in range(nb_modeles):
        for j in range(nb_metriques):
            plt.plot(metriques[i, j, :], label=str(i) + "_" + str(j))
    plt.show()


def create_elo_dbs(first_year, last_year):
    for year in range(first_year, last_year + 1):
        reset_classement(year)


if __name__ == "__main__":
    create_elo_dbs(first_year, last_year)
    plot_metriques(first_year, last_year)

