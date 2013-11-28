from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import DATA_FILENAME


target_list = db.read_data(DATA_FILENAME)
points = {}
distances = {}
max_distance = -1
min_distance = -1


@timing
def proc():
    global max_distance, min_distance
    # Get max and min distance
    for row in target_list:
        # row[0]: origin; row[1]: destination; row[2]: distance
        if row[2] > max_distance:
            max_distance = row[2]
        if row[2] < min_distance or min_distance == -1:
            min_distance = row[2]

    # Get nearest distances
    for row in target_list:
        if row[0] not in distances or int(row[2]) < distances[row[0]]:
            points[row[0]] = row[1]
            distances[row[0]] = int(row[2])
    for row in target_list:
        if row[1] not in distances or int(row[2]) < distances[row[1]]:
            points[row[1]] = row[0]
            distances[row[1]] = int(row[2])


def main():
    proc()
    res = []
    for point in points:
        res.append([point, points[point], distances[point]])
    print max_distance, min_distance
    db.write_data('overhead-output_serial.txt', res)
