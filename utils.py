import csv
import geopy.distance
import datetime

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
    # print(hour, week_day)
    return hour, week_day

def load_taxi_meta_data():
    taxi_stand_id_to_lat_lon = {}
    with open('data/metaData_taxistandsID_name_GPSlocation.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(row)
                line_count += 1
                continue
            else:
                taxi_stand_id_to_lat_lon[int(row[0])] = [float(row[2]), float(row[3])]

        print(f'Processed {line_count} lines.')
        return taxi_stand_id_to_lat_lon


def load_training_data():
    taxi_stand_id_to_lat_lon = load_taxi_meta_data()
    trip_metrics = []
    target_distance_yi = []
    with open('data/train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(row)
                line_count += 1
            elif line_count == 100000:
                break
            else:
                if row[7] == "True" or row[1] == "A" or row[1] == "C" or row[3] == '':
                    continue
                timestamp = int(row[5])
                hour, weekday = from_unix_timestamp(timestamp)
                origin_stand_lat = taxi_stand_id_to_lat_lon[int(row[3])][0]
                origin_stand_lon = taxi_stand_id_to_lat_lon[int(row[3])][1]
                distance_yi = distance_from_polyline(list_from_polyline_string(row[8]))

                trip_metrics.append([hour, weekday, origin_stand_lat, origin_stand_lon])
                target_distance_yi.append(distance_yi)
                line_count += 1
                print(line_count)

        print(f'Processed {line_count} lines.')
        return trip_metrics, target_distance_yi



print(time_from_polyline([[-8.639847,41.159826],[-8.640351,41.159871],[-8.642196,41.160114],[-8.644455,41.160492],[-8.646921,41.160951],[-8.649999,41.161491],[-8.653167,41.162031],[-8.656434,41.16258],[-8.660178,41.163192],[-8.663112,41.163687],[-8.666235,41.1642],[-8.669169,41.164704],[-8.670852,41.165136],[-8.670942,41.166576],[-8.66961,41.167962],[-8.668098,41.168988],[-8.66664,41.170005],[-8.665767,41.170635],[-8.66574,41.170671]]))

print(from_unix_timestamp(1372637303))
print(distance_from_polyline([[-8.639847,41.159826],[-8.640351,41.159871],[-8.642196,41.160114],[-8.644455,41.160492],[-8.646921,41.160951],[-8.649999,41.161491],[-8.653167,41.162031],[-8.656434,41.16258],[-8.660178,41.163192],[-8.663112,41.163687],[-8.666235,41.1642],[-8.669169,41.164704],[-8.670852,41.165136],[-8.670942,41.166576],[-8.66961,41.167962],[-8.668098,41.168988],[-8.66664,41.170005],[-8.665767,41.170635],[-8.66574,41.170671]]))
[41.1599801853,-8.64198392478]

























