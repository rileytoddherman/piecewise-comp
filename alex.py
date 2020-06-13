import itertools
import csv

alpha = 0.05

def get_data():
    data = []
    input_data = csv.DictReader(open("data.csv"))
    for datum in input_data:
        new_datum = {'samples': (
            datum['sample1'], datum['sample2']), 'adjsig': float(datum['adjsig'])}
        data.append(new_datum)
    return data

def write_data(data):
    with open('output.csv', 'w', newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for datum in data:
            w.writerow(datum)

def get_groups(data):
    sample_list = []
    groups = []
    for datum in data:
        for sample in datum['samples']:
            if sample not in sample_list:
                sample_list.append(sample)
    for i in range(2, len(sample_list)):
        tmp = list(itertools.combinations(sample_list, i))
        for t in tmp:
            groups.append(t)
    groups.append(tuple(sample_list))
    return groups

def slim(groups):
    fat = []
    for group_i in groups:
        for group_j in groups:
            if group_i is not group_j and all(j in group_i for j in group_j):
                fat.append(group_j)
    return list(filter(lambda g: g not in fat, groups))

def get_datum(sample1, sample2, data):
    for datum in data:
        if datum['samples'] == (sample1, sample2) or datum['samples'] == (sample2, sample1):
            return datum['adjsig']
    return None


def is_non_significant(group, data):
    for i in range(len(group)):
        for j in range(i, len(group)):
            adjsig = get_datum(group[i], group[j], data)
            if adjsig is not None and adjsig < alpha:
                return False
    return True


def main():
    data = get_data()
    groups = get_groups(data)
    non_sig_groups = []
    for group in groups:
        if is_non_significant(group, data):
            non_sig_groups.append(group)
    non_sig_groups = slim(non_sig_groups)
    print(non_sig_groups)
    write_data(non_sig_groups)

main()
