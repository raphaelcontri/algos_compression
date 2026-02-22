def encode_lzw(t) :
    ## on crée un dictionnaire composé des lettres :
    alphabet = set(t)
    dictionnaire = dict()
    code = list()
    for e in alphabet :
        dictionnaire[e] = ord(e)

    ## on parcourt ensuite tout notre texte :
    i = 0
    sous_mot_non_present = t[0:2]
    while i <= len(t) - len(sous_mot_non_present): 
        ## on cherche le plus long sous mot encore non présent 
        sous_mot_non_present = trouver_plus_long_sous_mot(dictionnaire, t, i)

        ## on ajoute ce sous mot dans le dictionnaire 
        dictionnaire[sous_mot_non_present] = max(dictionnaire.values()) + 1

        ## ensuite, on encore le sous mot[:-1], cad le sous mot qui existe déjà dans le dictionnaire
        code.append(dictionnaire[sous_mot_non_present[:-1]])
        i += len(sous_mot_non_present[:-1])
    #code.append(dictionnaire[t[i:len(t)]])
    return code, dictionnaire


def trouver_plus_long_sous_mot(dico, t, i) :
    """ renvoie le plus long sous mot non encore présent dans le dictionnaire dico à partir de l'indice i"""
    j = i
    sous_mot = t[j]
    while sous_mot in dico.keys() and j < len(t)-1 :
        j += 1
        sous_mot += t[j]
    return sous_mot

## decode :
def decode_lzw(t, alphabet) :
    
    dictionnaire = dict()
    for e in alphabet :
        dictionnaire[ord(e)] = e
    texte = dictionnaire[t[0]]
    for i in range(1, len(t)) :
        if t[i] in dictionnaire : 
            texte += dictionnaire[t[i]] # on ajoute le sous mot décodé à texte, le résultat en construction
            sous_mot = dictionnaire[t[i-1]] + dictionnaire[t[i]][0] ## on trouve le plus long sous mot encore non présent dans le dictionnaire
            dictionnaire[max(dictionnaire.keys()) + 1] = sous_mot ## on ajoute ce sous mot au ddictionnaire
        else : ## dans certains cas, t[i] n'est pas dans dictionnaire. On procède alors différement. 
            texte += dictionnaire[t[i-1]] + dictionnaire[t[i-1]][0]
            sous_mot = dictionnaire[t[i-1]] + dictionnaire[t[i-1]][0]
            dictionnaire[max(dictionnaire.keys()) + 1] = sous_mot
    return texte, dictionnaire


## procédure de test :

def test(fichier) : 
    test = open(fichier, "r")
    txt = test.read()

    a = encode_lzw(txt)
    l = len(a[0])
    print("longueur du texte non encodé : ", len(txt), "\nlongueur du texte encodé par LZW : ", len(a[0]), "\nle texte encodé est ", len(txt)/len(a[0]), " fois plus petit que le texte non encodé")
    



        
        

        
