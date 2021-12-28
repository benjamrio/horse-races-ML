import numpy as np
import pandas as pd

"""
Output finale des modèles : un classement des chevaux. Un tableau ou les index correspondent au classement prédit et les valeurs sont les résulats 
effectifs de la course. Par exemple, sur une course à trois chevaux, si le premier selon les prédiction finit troisième, 
le deuxième premier et le troisième deuxième, le tableau résultat sera [3,1,2]. Une prédicition parfaite serait [1,2,3,...,n]

Idée de métrique: On pourrait compter le nombre de cycles
"""


def DCG(results, n=-1):
    """
    Implémente le calcul du Discounted Cumulative Gain
    Entrée :
        results -- liste de résultats où les index correspondent au classement prédit et les valeurs sont les résultats réels de la course
        n -- la limite de la somme, par défaut tous les chevaux sont pris en compte
    """
    if n == -1:
        n = len(results)
    top = results[:n]
    return np.sum(
        np.array([len(top) - top[i] / (np.log(i + 2)) for i in range(len(top))])
    )


def eDCG(results, n=-1):
    """
    Implémente le calcul du Discounted Cumulative Gain en pondérant le classement réel de manière exponentielle (les premiers classements ont plus d'importance)
    """
    if n == -1:
        n = len(results)
    top = results[:n]
    return np.sum(
        np.array(
            [(2 ** (len(top) - top[i]) - 1) / (np.log(i + 2)) for i in range(len(top))]
        )
    )


def winner(results):
    return int(results[0] == 1)


def NDCG(results, n=-1):
    """
    Compute le Normalized Discouted Cumulative Gain. Le gain idéal est celui du classement parfait.
    Meme args que DCG
    """
    if n == -1:
        n = len(results)
    top = results[:n]
    return DCG(top, n) / DCG(list(range(1, n + 1)), n)


def NeDCG(results, n=-1):
    """
    Compute le Normalized Exponential Discouted Cumulative Gain. Le gain idéal est celui du classement parfait.
    Meme args que DCG
    """
    if n == -1:
        n = len(results)
    top = results[:n]
    return eDCG(top, n) / eDCG(list(range(1, n + 1)), n)


def transforme_preds_classement(res, preds, croissant=False):
    """
    Retourne le tableau résultat, qui sert d'entrée pour les fonctions évaluation métriques,
    qui donne les positions du classment à partir des résultats (prédits ou non)
    args :
        preds -- un tableau contenant une prédiction de résultats (elo, ote)
        res -- un tableau contenant les vrais résultats (les indices sont en accords avec ceux de preds)
        croissant -- un booléen indiquant si le tableau resultats est croissant ie que le cheval le plus fort a le plus haut indicateur (vrai pour l'elo, faux pour les cotes)
    """
    if croissant:
        args = np.argsort(preds)[::-1]
    else:
        args = np.argsort(preds)
    results_vs_preds = [res[args[i]] for i in range(len(preds))]
    return results_vs_preds


def evaluate_from_csv(csv_path, metriques):
    """Calcule les métriques à partir d'un fichier csv contenant résultats et prédictions

    Arguments:
        df {DataFrame} -- un dataframe avec deux colomnes: la première contient les résultats réels d'une course,
        la deuxième contient les prédictions
        metriques {list} -- listes de noms de métriques, qui évaluent les prédictions du modèle

    """
    df = pd.read_csv(csv_path, header=None, columns=["results", "preds"])
    return evaluate_from_df(df, metriques)


def evaluate_from_array(array, metriques):
    """Calcule les métriques à partir d'un tableau 2D contenant les résultats des courses et leur prédictions calculés par un modèle

    Arguments:
        df {DataFrame} -- un dataframe avec deux colomnes: la première contient les résultats réels d'une course,
        la deuxième contient les prédictions
        metriques {list} -- listes de noms de métriques, qui évaluent les prédictions du modèle

    Returns:
        {Numpy array} -- Un array avec les moyenens des métriques, dans l'odre de l'entrée métriques
    """
    df = pd.DataFrame(array, columns=["results", "preds"])
    return evaluate_from_df(df, metriques)


def evaluate_from_df(df, metriques):
    """Calcule les métriques à partir d'un dataframe contenant les résultats des courses et leur prédictions calculés par un modèle

    Arguments:
        df {DataFrame} -- un dataframe avec deux colomnes: la première contient les résultats réels d'une course,
        la deuxième contient les prédictions
        metriques {list} -- listes de noms de métriques, qui évaluent les prédictions du modèle

    Returns:
        {Numpy array} -- Un array avec les moyenens des métriques, dans l'odre de l'entrée métriques
    """
    for metrique in metriques_from_names(metriques):
        df[metrique.__name__] = df.apply(
            lambda row: metrique(
                transforme_preds_classement(row["results"], row["preds"])
            ),
            axis=1,
        )
    return df.mean(axis=0)


def metriques_from_names(names):
    """Transforme une liste de noms de métriques en la liste de métriques correspondante

    Arguments:
        names {list} -- liste des noms des métriques
    Returns:
        {list} -- liste des fonctions (métriques) associées
    """
    return [getattr(nom) for nom in names]
