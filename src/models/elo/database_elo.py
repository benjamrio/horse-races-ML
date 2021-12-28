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

# Constantes logiciel
FILEPATH_DATA = "e:/MyData/KLAP/CleanData/"
nom_fichier = "horses2010.csv"

# Constantes pour le calcul d'elo
ELO_INITIAL = 1500
K = 24
"""
#database des courses
courses = pd.read_csv(FILEPATH_DATA+nom_fichier, sep=";")
print("Le fichier course contient %d lignes" % len(courses))
data_courses = courses[['raceId', 'horse_genyId','horse_name','results_position']]

#database des classements elos
classement = pd.DataFrame(columns = ['id', 'nom', 'elo']).set_index('id', drop=False)
"""


def initialisation_nvx_elos(year, how="uniform"):
    """
  Intialise l'elo pour les chevaux absents de la database classement.
  Lecture, chargement en mémoire, query sur le dataframe et ecriture du fichier classement.
  """
    nom_fichier = FILEPATH_DATA + "horses" + str(year) + ".csv"
    df = pd.read_csv(nom_fichier, sep=";")[
        ["raceId", "horse_genyId", "horse_name", "results_position"]
    ]

    classement = pd.read_csv(
        "outputs/elo/classement_elo" + str(year) + ".csv", encoding="utf-8", sep=";"
    )
    index_absents = ~df["horse_genyId"].isin(classement["id"]).values
    absents = df[["horse_genyId", "horse_name"]][index_absents].drop_duplicates().values
    liste_elo = np.broadcast_to(ELO_INITIAL, (len(absents), 1))
    nvx_chevaux_data = np.concatenate((absents, liste_elo), axis=1)
    df2 = pd.DataFrame(nvx_chevaux_data, columns=["id", "nom", "elo"])
    classement = classement.append(df2, ignore_index=True).set_index("id", drop=True)
    classement.to_csv("outputs/elo/classement_elo" + str(year) + ".csv", sep=";")


def calcule_elo(year):
    """
  A partir de la database des courses d'une certaine période, calcule les élos résultants ainsi que les métriques prédictives
  Calcul successif, course par course.
  Args :
    year--(int) année sur laquelle on veut effectuer le calcul d'elo et le ca
  Renvoie un tableau 1D des évaluations des métriques
  """
    nom_fichier = FILEPATH_DATA + "horses" + str(year) + ".csv"
    df = pd.read_csv(nom_fichier, sep=";")[
        ["raceId", "horse_genyId", "horse_name", "results_position"]
    ]

    classement = pd.read_csv(
        "outputs/elo/classement_elo" + str(year) + ".csv", encoding="utf-8", sep=";"
    )

    by_race = df.groupby("raceId")
    metrics_array = np.zeros((len(by_race), 3))
    counter = 0

    print(
        "Calcul de l'elo à l'issue %d courses contenues dans le fichier %s"
        % (len(by_race), FILEPATH_DATA + nom_fichier),
        end="\n\n",
    )
    print(
        "Description du nombre de chevaux par course\n",
        by_race["horse_genyId"].count().describe(),
    )
    for _, race_data in by_race:
        infos_course = pd.merge(
            race_data, classement, how="inner", left_on="horse_genyId", right_on="id"
        )

        # Calcul de la métrique sur la course
        preds = infos_course["elo"].values
        res = infos_course["results_position"].values
        arrivees = np.count_nonzero(~np.isnan(np.array(res)))
        res_no_nan = np.nan_to_num(res, nan=(arrivees + len(res)) / 2)
        res_preds_real = transforme_preds_classement(preds, res_no_nan, croissant=True)
        metrics_array[counter, :] = [
            NDCG(res_preds_real),
            eDCG(res_preds_real),
            winner(res_preds_real),
        ]
        counter += 1

        # update de l'elo
        nouveaux_elos = new_elo(
            infos_course["elo"].values, infos_course["results_position"].values
        )
        for indice, id in enumerate(infos_course["horse_genyId"]):
            classement.loc[classement["id"] == id, "elo"] = nouveaux_elos[indice]

    classement.to_csv("outputs/elo/classement_elo" + str(year) + ".csv", sep=";")
    return np.mean(metrics_array, axis=0)


def new_elo(anciens_elo, resultats):
    """
    Calcule la liste des nouveaux elos
    Args :
      anciens_elo -- liste de float
      resultats -- liste de float, contenant des nan (et rien d'autre)
    """
    nb_partants = len(anciens_elo)
    nb_arrivees = np.count_nonzero(~np.isnan(resultats))
    R = 10 ** (anciens_elo / 400)
    Rtot = np.sum(R)
    E = R / (R + (1 / (nb_partants - 1)) * (Rtot - R))
    S = np.array(
        [
            (nb_arrivees - position + 1) / nb_arrivees if not np.isnan(position) else 0
            for position in resultats
        ]
    )
    new_elo_tot = K * np.sum(S - E)
    nvx_elo = anciens_elo + K * (S - E) - new_elo_tot / nb_partants
    return nvx_elo


def reset_classement(year):
    """
  Création d'un fichier csv blanc avec les headers,
  correspondant à la database vierge des classements elo
  """
    classement = pd.DataFrame(columns=["id", "nom", "elo"]).set_index("id", drop=True)
    classement.to_csv("outputs/elo/classement_elo" + str(year) + ".csv", sep=";")


def main():

    tmps1 = timeit.default_timer()
    initialisation_nvx_elos()
    tmps2 = timeit.default_timer()
    calcule_elo()
    tmps3 = timeit.default_timer()
    print("Initialisation en %f secondes" % (tmps2 - tmps1))
    print("Calcul des nouveaux élos en %f secondes" % (tmps3 - tmps2))


if __name__ == "__main__":
    # reset_classement()
    # main()
    pass
