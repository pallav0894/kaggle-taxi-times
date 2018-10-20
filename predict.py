import csv
import geopy.distance
import datetime
import re
import numpy as np
from sklearn import datasets, linear_model, metrics
from sklearn.metrics import mean_squared_error
import pandas as pd


def csv_from_pandas():
    training_data = pd.read_csv(open('data/train.csv'), nrows=100000)
    train_call_type_a = training_data[training_data['CALL_TYPE'] == "A"]
    train_call_type_b = training_data[training_data['CALL_TYPE'] == "B"]
    train_call_type_c = training_data[training_data['CALL_TYPE'] == "C"]
    print(train_call_type_a.head(1000))


def load_taxi_meta_data():
    taxi_stand_id_to_lat_lon = {}
    with open('data/metaData_taxistandsID_name_GPSlocation.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(row)
                line_count += 1
                next
            else:
                taxi_stand_id_to_lat_lon[int(row[0])] = [float(row[2]), float(row[3])]

        print(f'Processed {line_count} lines.')
        return taxi_stand_id_to_lat_lon


def csv_processing():
    taxi_stand_id_to_lat_lon = load_taxi_meta_data()
    trip_metrics = []
    target_distance_yi = []
    with open('data/train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(row)
                line_count += 1
                next
            elif line_count == 10000:
                break
            else:
                if row[7] == "True" or row[1] == "A" or row[1] == "C":
                    next
                timestamp = int(row[5])
                hour, weekday = from_unix_timestamp(timestamp)
                origin_stand_lat = taxi_stand_id_to_lat_lon[int(row[3])][0]
                origin_stand_lon = taxi_stand_id_to_lat_lon[int(row[3])][1]
                distance_yi = distance_from_polyline(list_from_polyline_string(row[8]))

                trip_metrics.append([hour, weekday, origin_stand_lat, origin_stand_lon])
                target_distance_yi.append(distance_yi)
                line_count += 1

        print(f'Processed {line_count} lines.')
        return trip_metrics, target_distance_yi


def main():
    trip_metrics = csv_processing()
    xi = np.array(trip_metrics)


def time_from_polyline(polyline):
    if len(polyline) == 0:
        return 0
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
    final_dist = 0.00
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
    minute = dt.minute
    # print(hour, week_day)
    # return [hour, minute]
    return dt


# from_unix_timestamp(1372637303)

def hours_from_test_set():
    hours = []
    with open('data/test_public.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(row)
                line_count += 1

            else:

                hours += [from_unix_timestamp(int(row[5]))]

        print(f'Processed {line_count} lines.')

    hr_set = [x[0] for x in hours]
    hours.sort(key= lambda x: x[0])
    print(hours)
    print(sorted(hr_set))



# hours_from_test_set()











