import pandas as pd
import json
import timeit
import os
from utils import flatten_dic

data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "2010-2019-races"))


def races_json_to_df(output):
    """
    Write a csv file with relevant fields containing all 2010-2019 race data
    Args:
        output -- a string, used as path output starting from /databases
    """
    print(
        "Il y a %d fichiers de course dans le dossier %s"
        % (len(os.listdir(data_path)), data_path)
    )
    frames = []

    for file in os.listdir(data_path):
        # if not file.startswith('2010'):
        #    break
        with open(os.path.join(data_path, file), encoding="utf-8") as json_file:
            data = json.load(json_file)
        selected_fields = list(data.keys())
        selected_fields.remove("partants")
        selected_fields.remove("nonPartants")
        flattened_dic = flatten_dic(
            {donnee: data[donnee] for donnee in selected_fields}
        )
        flattened_dic["name_race"] = file.split(sep=".")[0]
        df = pd.DataFrame(flattened_dic, index=[0])
        frames += [df]

    result = pd.concat(frames, ignore_index=True)
    result.to_csv(
        os.path.join(os.getcwd(), "databases", output), encoding="utf-8", sep=","
    )


def main():
    races_json_to_df("courses.csv")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(
        "CSV created at path %s" % os.path.join(os.getcwd(), "databases", "courses.csv")
    )
    print("Time to process:", stop - start)
