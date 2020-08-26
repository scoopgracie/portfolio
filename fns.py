def fns(data):
    data = sorted(data)
    minimum = min(data)
    if len(data) % 2 == 1:
        median = data[(len(data)-1)//2]
    else:
        first_median = data[(len(data)-1)//2]
        second_median = data[(len(data)-1)//2 + 1]
        median = (first_median + second_median)/2
    first_half = [i for i in data if i < median]
