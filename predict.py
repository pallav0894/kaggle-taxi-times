import csv
import geopy.distance
import datetime
import re
import numpy as np
from sklearn import datasets, linear_model, metrics
from sklearn.metrics import mean_squared_error

def csv_processing():
    trip_metrics = []
    with open('data/train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(row)
                line_count += 1
                # next
            elif line_count == 10000:
                break
            else:
                trip_metrics += [row[5], row[8]]
                line_count += 1

        print(f'Processed {line_count} lines.')
        return trip_metrics

def main():
    trip_metrics = csv_processing()


def time_from_polyline(polyline):
    return (len(polyline)-1)*15


def list_from_polyline_string(polyline_str):
    final_polyline = []
    c = 0
    while c < len(polyline_str):
        if c == 0 or c == len(polyline_str)-1:
            c += 1
        else:
            coords = []
            if polyline_str[c] == "[":
                c += 1
                d = c
                while polyline_str[d] != ",":
                    d += 1
                coords.append(float(polyline_str[c:d]))
                d += 1
                c = d
                while polyline_str[d] != "]":
                    d += 1
                coords.append(float(polyline_str[c:d]))
                d += 1
                c = d

                final_polyline.append(coords)
                c += 1
            else:
                c += 1

    return final_polyline


def distance_gps_coordinates(c1, c2):
    return geopy.distance.vincenty(c1, c2).miles


def distance_from_polyline(polyline):
    final_dist = 0
    for i in range(len(polyline)):
        if i == len(polyline)-1:
            break
        else:
            final_dist += distance_gps_coordinates(polyline[i], polyline[i+1])

    return final_dist

# Returns hour and day of the week
def from_unix_timestamp(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    hour = dt.hour
    week_day = dt.weekday()
    print(hour, week_day)
    return hour, week_day


from_unix_timestamp(1372636858)
str = "[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]"
print(list_from_polyline_string(str))














