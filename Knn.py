from math import sqrt
from matplotlib import pyplot as ppl
from random import shuffle

def loadData(path):
    with open(path,"r") as fil:
        return [l.replace("\n","").split(";") for l in fil]


k = 6

def knn(dataTest,dataApp):
    res = list()

    for t in dataTest:
        d = [(sqrt(sum((float(t[i]) - float(da[i]))**2 for i in range(4))),da[4]) for da in dataApp]
        d.sort(key = lambda x:x[0])
        d = d[0:k]
        res.append(int(max(d, key = lambda x: [e[1] for e in d].count(x[1]))[1] == t[4]))

    print(res.count(1)/len(res))
    ppl.hist(res)
    ppl.show()

eps = 0.5
minPts = 1

def dbscan_Model(dataApp):

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

    def epsVoisin(p):
        return [e 
        for e in dataApp
        if sqrt(sum((float(p[i]) - float(e[i]))**2
        for i in range(4))) < eps]


    c = 0
    clusters = list()
    clustered = list()

    for p in dataApp:
        if p not in clustered:
            voisins = epsVoisin(p)

            if len(voisins) > minPts:
                clusters.append(list())
                etendreCluster(p, voisins, clusters[c])
                c = c+1

    clustLabeled = list()
    for cl in clusters:
        ls = [e[4] for e in cl]
        label = max(ls, key= lambda x: ls.count(x))
        clustLabeled.append((cl,label))
    
    return clustLabeled

def dbscan_Stat(labeledPoints, originalData):
    res = list()
    for i in range(len(labeledPoints)):
        res.append(int(labeledPoints[i][4] == originalData[i][4]))

    print("Min voisin", minPts, "Epsilon", eps)
    print("Nb learning data", len(originalData))
    print("Nb Labeled data", len(labeledPoints))
    print("% réussite", res.count(1)/len(res) * 100)
    ppl.hist(res)
    ppl.show()

def dbscan_Apply(clusters, data):
    def NearestClusterLabel(p):
        vects = [e[0] for e in clusters]
        centres = None
        nearest = min(centres, key = lambda x : sum(float(p[i]) - float(x[0][i])**2 for i in range(4)))
        return nearest[1]

    labeledP = list()
    for p in data:
        l = NearestClusterLabel(p)
        labeledP.append(p[:] + [l])


if __name__ == "__main__":
    data = loadData("data.csv") #Training dataset
    shuffle(data)
    datat = data[0::2][0:4]
    dataa = data[1::2]

    clusters = dbscan_Model(dataa)

    data = loadData("preTest.csv")
    shuffle(data)