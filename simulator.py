from argparse import ArgumentParser
from random import random
from collections import OrderedDict


def dummyEventList(n, type_data, dim):
    event_list = {}
    t_l = 0
    for k in range(n):
        t = t_l+random()
        event_list[t] = [type_data, [random() for x in range(dim)]]
        t_l = t
    return event_list


def dummyRiskMap(pos):
    if random() > 0.5:
        return True
    else:
        return False

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
    args = ArgumentParser()
    args.add_argument("gps_sim_file", type=str)

    parser = args.parse_args()

    gps_sim = dummyEventList(10, "GPS", 2)
    print(gps_sim)

    accel_sim = dummyEventList(10, "Accelerometer", 3)
    print(accel_sim)

    event_sim = mergeEventList(gps_sim, accel_sim)
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
        
        dummyPosStatus = dummyRiskMap(pos)
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
