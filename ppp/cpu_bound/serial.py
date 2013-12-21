from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import DATA_FILENAME


target_list = []
remove_indexes = []


@timing
def proc():
    for i, t in enumerate(target_list):
        if i in remove_indexes:
            continue
        for j in range(i + 1, len(target_list)):
            # Record duplicates to be removed
            if t[0] == target_list[j][0] and t[1] == target_list[j][1]:
                remove_indexes.append(j)
            # Fix reverse distance
            elif t[0] == target_list[j][1] and t[1] == target_list[j][0]:
                target_list[j][2] = t[2]

    # Remove duplicates by popping
    count = 0
    remove_indexes.sort()
    for i in remove_indexes:
        index = i - count
        target_list.pop(index)
        count += 1


def main():
    global target_list
    target_list = db.read_data(DATA_FILENAME)
    proc()
    output_filename = db.get_output_path(DATA_FILENAME, 'output_serial')
    db.write_data(output_filename, target_list)
