import re
def convertion_duree(str):
    
    split_liste = re.split("\s", str)
    duree = 0
    for elt in split_liste:
        if "h" in elt:
            duree = int(re.split("h", elt)[0]) *60 +duree
        elif "m" in elt:
            duree =int(re.split("m", elt)[0]) +duree
    return duree