#Td réalisé en binome avec Tristan Lamouric
from math import sqrt
from matplotlib import pyplot as ppl

def loadData(path):
    with open(path,"r") as fil:
        return [l.replace("\n","").split(",") for l in fil]

data = loadData("iris.data") #sepal length,sepal width, petal length, petal width
datat = data[0::2]
dataa = data[1::2]
k = 5

def knn():
    res = list()

    for t in datat:
        d = [(sqrt(sum((float(t[i]) - float(da[i]))**2 for i in range(4))),da[4]) for da in dataa]
        d.sort(key = lambda x:x[0])
        d = d[0:k]
        res.append(int(max(d, key = lambda x: [e[1] for e in d].count(x[1]))[1] == t[4]))

    print(res)
    ppl.hist(res)
    ppl.show()

eps = 0.2
minPts = 2

def dbscan():

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
        return [e for e in data if sqrt(sum((float(p[i]) - float(e[i]))**2 for i in range(4))) < eps]


    c = 0
    clusters = list()
    clustered = list()

    for p in data:
        if p not in clustered:
            voisins = epsVoisin(p)

            if len(voisins) > minPts:
                clusters.append(list())
                etendreCluster(p, voisins, clusters[c])
                c = c+1

    clust = list()
    for c in clusters:
        ls = [e[4] for e in c]
        label = max(ls, key= lambda x: ls.count(x))
        clust.append((c,label))

    res = list()
    for c,l in clust:
        for p in c:
            res.append(int(p[4]==l))

    print("Nb cluster", len(clust))
    print("% nb cluster / nb data", len(clust)/len(data) * 100)
    print("% bruit", len(res)/len(data) * 100)
    ppl.hist(res)
    ppl.show()

if __name__ == "__main__":
    knn()
    dbscan()