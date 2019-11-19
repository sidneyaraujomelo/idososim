from random import random
from collections import OrderedDict
from sklearn.neural_network import MLPClassifier
from deviceeventsim import DeviceEventSim
import numpy as np


def dummyEventList(n, type_data, dim):
    event_list = {}
    t_l = 0
    for k in range(n):
        t = t_l+random()
        event_list[t] = [type_data, [random() for x in range(dim)]]
        t_l = t
    return event_list

def trainRiskMap():
    poss = []
    labels = []
    with open('walks.txt', 'r') as f:
        for l in f.readlines():
            poss.append([int(x) for x in l.split('\t')[:15]])
            labels.append(int(l.split('\t')[-1]))
    
    model = MLPClassifier(max_iter=1000)
    model.fit(poss, labels)

    return model

def dummyRiskMap(pos, model):
    return model.predict(np.array(pos).reshape(1, -1))[0]

def dummyAccelClassifier(accel_list):
    if random() > 0.9:
        return True
    else:
        return False


def mergeEventList(a, b):
    merged_list = a
    merged_list.update(b.items())
    sorted_merged_list = OrderedDict(sorted(merged_list.items()))
    return sorted_merged_list


def updateWindow(window, k, v, delta):
    window[k] = v
    wk = list(window.keys())
    i = 0
    if (wk[-1] - wk[i]) > delta:
        while (wk[-1] - wk[i]) > delta:
            i=i+1
        for r in range(i):
            window.pop(wk[r])
    return window


def main():
    gps_sim = DeviceEventSim(10, "GPS", 3)
    print(gps_sim.dict)

    accel_sim = DeviceEventSim(10, "Accelerometer", 4)
    print(accel_sim.dict)
    
    event_sim = mergeEventList(gps_sim.dict, accel_sim.dict)
    
    print(event_sim)
    pos = None
    window = OrderedDict()
    max_delta_window = 0.5
    report = OrderedDict()
    for k,v in event_sim.items():
        print(f"=========== Timestamp: {k} ===========")
        if v[0] == "GPS":
            pos = v[1]
        else:
            window = updateWindow(window, k, v, max_delta_window)
        print(f"Position: {pos}")
        print(f"Accelerometer window:")
        for wk, wv in window.items():
            print(f"\t{wk}: {wv[1]}")
        pos = [0,17,22,7,15,18,21,6,14,19,16,9,10,4,5] # NO CAMINHO
        # pos = [0,17,22,7,15,40,21,31,14,25,16,9,52,4,5] # FORA DO CAMINHO
        model = trainRiskMap()
        dummyPosStatus = not(dummyRiskMap(pos, model))
        dummyAccelStatus = dummyAccelClassifier(window.values())
        
        if dummyPosStatus and dummyAccelStatus:
            report[k] = "Risco alto! Queda em ambiente inseguro detectada!"
        elif dummyPosStatus:
            report[k] = "Idoso em local inseguro!"
        elif dummyAccelStatus:
            report[k] = "Atenção! Queda detectada!"
        else:
            report[k] = "OK."
    with open("report.txt", "w+") as fp:
        for k,v in report.items():
            fp.write(f"{k:.2f}: {v}\n")

if __name__ == "__main__":
    main()
