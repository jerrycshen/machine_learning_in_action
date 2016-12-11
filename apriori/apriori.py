# -*- coding: utf-8 -*-

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


def createC1(dataSet):
    C1 = []
    for transcation in dataSet:
        for item in transcation:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    # 这里用frozenset的目的是确保set集合不可变，才能作为dict键
    return map(frozenset,C1)


def scanD(D, Ck, minSupport):
    """
    扫描数据集，找出频繁项集
    :param D: 数据集
    :param Ck: 候选集
    :param minSupport:
    :return:
    """
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = [] # 频繁项集
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):
    """

    :param Lk: 频繁项集
    :param k:
    :return:
    """
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i][:,k-2])
            L2 = list(Lk[j][:,k-2])
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0 :
        Ck = aprioriGen(L[k-2],k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf =0.7):
    pass


def calcConf(freSet, H, supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freSet] / supportData[freSet - conseq]
        if conf >= minConf:
            print freSet-conseq, '-->',conseq,'conf:',conf
            br1.append((freSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH