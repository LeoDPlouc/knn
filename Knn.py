from math import sqrt
from matplotlib import pyplot as ppl
from random import shuffle

#Charge les données sous forme de tableau sous le format [x1,x2,x3,x4,label]
def loadData(path):
    with open(path,"r") as fil:
        return [l.replace("\n","").split(";") for l in fil]

#Sauvegarde les données dans un fichier au format "x1;x2;x3;x4;label\n"
def saveData(path, data):
    s = list()
    for d in data:
        a = d[0][:]
        a.append(d[1])
        if(len(a) != 5):
            print("")
        a = ";".join(a)
        s.append(a + "\n")
    with open(path, "w") as fil:
        fil.writelines(s)

#Paramettre k pour la fonction knn
k = 6

#Alogrithme knn
def knn(dataTest,dataApp):
    res = list()

    for t in dataTest:

        #Classe les points selon la distance au points observé
        d = [(sqrt(sum((float(t[i]) - float(da[i]))**2 for i in range(4))),da[4]) for da in dataApp]
        d.sort(key = lambda x:x[0])

        #Crée un cluster contenant les k plus proches voisins
        d = d[0:k]
        res.append(int(max(d, key = lambda x: [e[1] for e in d].count(x[1]))[1] == t[4]))

    print(res.count(1)/len(res))
    ppl.hist(res)
    ppl.show()

#Parametre Epsilon et nombre minimum de points pour la fonction dbscan
eps = 0.04
minPts = 2

def dbscan_Model(dataApp):

    #Etend le cluster avec les points voisins
    def etendreCluster(p, voisins, cluster):
        cluster.append(p)
        clustered.append(p)
        for v in voisins:
            if v not in clustered:
                voisins2 = epsVoisin(v)
                if len(voisins2) > minPts:
                    voisins.extend(voisins2)
                cluster.append(v)
                clustered.append(v)

    #Retourne une liste des voisins a une distance infereur a epsilon
    def epsVoisin(p):
        return [e 
        for e in dataApp
        if sqrt(sum((float(p[i]) - float(e[i]))**2
        for i in range(4))) < eps]

    clusters = list()
    clustered = list()

    for p in dataApp:
        if p not in clustered:
            #Recuperation des voisins du points
            voisins = epsVoisin(p)

            #Si le nombre de voisin est suffisant on etent le cluster
            if len(voisins) > minPts:
                cl = list()
                etendreCluster(p, voisins, cl)
                clusters.append(cl)

    clustLabeled = list()

    #Le label du cluster est determine par le label le plus frequent parmis les points qu'il contient
    for cl in clusters:
        ls = [e[4] for e in cl]
        label = max(ls, key= lambda x: ls.count(x))
        clustLabeled.append([cl,label])
    
    return clustLabeled

def dbscan_Stat(labeledPoints, originalData):
    res = list()
    for i in range(len(labeledPoints)):
        res.append(int(labeledPoints[i][1] == originalData[i][4]))

    print("Min voisin", minPts, "Epsilon", eps)
    print("Nb learning data", len(originalData))
    print("Nb Labeled data", len(labeledPoints))
    print("% réussite", res.count(1)/len(res) * 100)
    ppl.hist(res)
    ppl.show()

def dbscan_Apply(clusters, data):
    def gravityCentre(c):
        l = c[1]
        pts = c[0]
        return [sum([float(p[j]) for p in pts])/len(pts) for j in range(4)], l

    centres = [gravityCentre(c) for c in clusters]

    

    labeledP = list()
    for p in data:
        nearestCluster = min(centres, key=lambda x : sum([(float(x[0][i])-float(p[i]))**2 for i in range(4)]))
        labeledP.append([p,nearestCluster[1]])

    return labeledP


if __name__ == "__main__":
    #Chargement et melange des donnees
    data = loadData("data.csv") #Training dataset
    shuffle(data)

    #Creation des clusters avec les donnees d'entrainement, affichage du taux de reussite
    clusters = dbscan_Model(data)
    results = dbscan_Apply(clusters, data)
    dbscan_Stat(results, data)

    #Classification des donnees de test avec les clusters trouves avec les donnees d'entrainement, affichage du taux de reussite
    data = loadData("preTest.csv")
    results = dbscan_Apply(clusters, data)
    dbscan_Stat(results, data)

    #Classification des donnees finales avec les clusters trouves avec les donnees d'entrainement
    data = loadData("finalTest.csv")
    results = dbscan_Apply(clusters, data)
    saveData("test.csv",results)