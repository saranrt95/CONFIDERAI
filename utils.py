
# from list of lists to list
def flatten(t):
    return [item for sublist in t for item in sublist]


# find indices of all occurrences of a substring (sub) in string a_str 
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches
