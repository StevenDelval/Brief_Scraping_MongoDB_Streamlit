import re
def convertion_duree(s):
    
    split_cell = re.split("\s", s)
    duree = 0
    for elt in split_cell:
        if "h" in elt:
            duree = int(re.split("h", elt)[0]) *60 +duree
        elif "m" in elt:
            duree =int(re.split("m", elt)[0]) +duree
    return duree