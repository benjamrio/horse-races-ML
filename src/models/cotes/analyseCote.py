import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pprint as pp

import json
import os
import timeit
from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVR, SVR, SVC
from sklearn import svm
dir_path = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(dir_path+"/data/cleanData/horsesData.csv", index_col=False)



#liste des courses de chevaux
listeUniqueRaceId = df['raceId'].unique()

#liste des noms de colonnes des ratios
ratioNames = ['odds_pmu_chronological_'+str(i)+'_ratio' for i in range(12)]

#liste des noms de colonnes des epochs
epochNames = ["odds_pmu_chronological_"+str(i)+"_epoch" for i in range(12)]

def checkCount():
#check if ratios and epochs have same NaN
    for i in range(len(ratioNames)):
        assert df[ratioNames[i]].count() == df[epochNames[i]].count()
checkCount()


dfCotes = df[["raceId","horse_name"]+ratioNames+epochNames].dropna()
dfCotesGrouped = dfCotes.groupby(by="raceId")



def coteCourse(i):
    '''
    Plot l'évolution des cotes de tous les chevaux de la course à l'index i 
    '''
    dfCourseCote = dfCotesGrouped.get_group(name=listeUniqueRaceId[i])
    for index,row in dfCourseCote.iterrows():
        ratios = dfCourseCote.loc[df.index[index], ratioNames]
        epochs = dfCourseCote.loc[df.index[index], epochNames]
        plt.plot( epochs, ratios, label=row["horse_name"])
    plt.show()


#coteCourse(-1)
                


def segregationEvolution():
    '''
    plot la variation de la cote en fonction de la cote initiale : nuage de points
    '''
    variationArray= []
    dfCotesInit = dfCotes["odds_pmu_chronological_"+str(0)+"_ratio"].dropna()
    for index, row in dfCotes.iterrows():
        #recherche du dernier epoch
        for i in list(range(11,0, -1)):
            coteFin = dfCotes.loc[df.index[index], "odds_pmu_chronological_"+str(i)+"_ratio"]
            if coteFin and not pd.isnull(coteFin):
                break
        coteDebut = dfCotesInit.at[index]
        variation = coteFin - coteDebut
        variationArray.append(variation)
   
    
    X = np.array(dfCotesInit.tolist()).reshape(-1,1)
    print(X)
    y = np.array(variationArray).reshape(-1,1)
    print(X.shape)
    assert X.shape == y.shape

    plt.scatter(X, y)

    for modelName in ['linearReg', 'lsvr', 'svr']:
        preds = predsModel(modelName, X, y)
        plt.plot(X, preds)
    
    plt.xlabel("cotes initiales")
    plt.ylabel("variation de la cote (finale-initiale)")
    plt.show()
    

def predsModel(modelName,X,y):
    '''
    Renvoie des pred
    args : 
        - modelName : string, parmi 'linearReg', 'lsvr', 'svr'
        - X : inputs
        - y : outputs
    '''
    if modelName == "linearReg":
        model = LinearRegression()
    elif modelName == "lsvr":
        model = LinearSVR()
    elif modelName == 'svr':
        model = SVR(kernel='rbf', C=50, gamma=0.1, epsilon=.1)
    model.fit(X, y)
    score = model.score(X, y)
    print(score)
    preds = model.predict(X)
    return preds

#segregationEvolution()
#plt.show()
# html = df[ratios+epochs].describe().to_html()
# text_file = open("index.html", "w")
# text_file.write(html)
# text_file.close()

#On regarde toutes les données concernant les cotes de pu
filterCol = [col for col in df if col.startswith('odds_pmu')]
filterCol += ['raceId', 'horse_name']
ratioNames = [col for col in filterCol if col.endswith('ratio')]
epochNames = [col for col in filterCol if col.endswith('epoch') or col.endswith('epochMs')]
ratioNames.remove('odds_pmu_reference10h_ratio')
print("\n Nom des colomnes des ratio:", ratioNames, "\n \n Nom des colomnes des epochs: ",  epochNames, "\n")

assert len(ratioNames) == len(epochNames)

dfShow = df[filterCol]
print(dfShow.head())
