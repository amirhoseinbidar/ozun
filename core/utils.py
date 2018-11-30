def find_in_dict(element,dictionary):
    for val in dictionary:
        if element == val[1] or element == val[0]:
            return val[0]
    return None