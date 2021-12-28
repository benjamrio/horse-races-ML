import numpy as np
from tabulate import tabulate
from metriques import NDCG, NeDCG, winner


def all_perms(elements):
    """
    Entrée : elements -- un tableau de nombre
    Sortie: un générateur contenant toutes les permutations (listes) du tableau en entrée
    """
    if len(elements) <= 1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]


def print_array_perm2(n, metrics, sort=False):
    """
  Affiche et renvoie une liste de toutes les permutations de [1,n] et les évalue selon les metriques
  Entrée :
    n -- Entier
    metrics -- un tableau de string avec les noms des metrics
    sorted -- indique si l'on veut sort selon le première métrique du tableau metrics (du plus grand au plus petit)
  Sortie : 
    array_metrics -- Un tableau de taille (2**n, m+1) où m est la taille du tableau metrics 
  """
    array_1n = list(range(1, n + 1))
    array_perm = list(all_perms(array_1n))

    m = len(metrics)
    array_metrics = np.array(
        [[str(perm)] + [metric(perm) for metric in metrics] for perm in array_perm]
    )

    if sort:
        array_metrics1 = array_metrics[
            np.argsort(list(map(float, array_metrics[:, 1])))[::-1]
        ]

    titles = ["Ordre d'arrivée"] + [metric.__name__ for metric in metrics]
    print(tabulate(array_metrics1, headers=titles))
    return (array_perm, array_metrics)


if __name__ == "__main__":
    print_array_perm2(4, metrics=[NeDCG, NDCG, winner], sort=True)
