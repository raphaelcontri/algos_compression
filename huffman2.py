from classes import *
import copy
## je susi désolé pour le mauvais code, je n'ai pas eu le temps de le clean...
## les fonctions ne sont pas écrites dans l'ordre logique de leur utilisation...
## se référer au mini readme pour comprendre le fonctionnement global du code 




def creer_file_priorite(liste) :
    """ entrée : une liste de la forme [["a", 34], [" ", 231]...] qui contient les lettres de l'alphabet utilisé et leur occurrence
    sortie : une file de priorité dont le nombre d'élements est celui du nombre de lettres dans l'alphabet, et ayant des tas pour valeurs"""
    file = Tas(Empty(), Tas(Empty(), liste[0], Empty()), Empty())
    for e in liste[1:] :
        file = file.ajouter(Tas(Empty(), e, Empty())) ## on ajoute des tas en valeurs ! on devra accéder à ces valeurs en tapant par exemple file.val.val
    return file



def Huffman2(liste) :
    """ crée un algo de Huffman en partant d'une liste de lettres associées à leur occurrence dans un texte"""
    file = creer_file_priorite(liste)
    identifiants = [i for i in range(100, 500)] ## est utilisé pour identifier de manière unique les noeuds de l'arbre (sinon ça bug quand on convertit l'arbre en graphe...)
    while file.taille() != 1 :
        ## on prend les deux premierds elemets de la file, on les fusionne et o les réinsère dans la file

        ## on extrait les deux premiers élements de la file
        el1 = file.minimum()
        file = file.supprimer()
        el2 = file.minimum()
        file = file.supprimer()

        ## on les fusionne :
        somme = [identifiants.pop(0), el1.val[1] + el2.val[1]] ## calcul de la valeur de la racine

        ## on recrée l'arbre en insérant la plus petite valeur à gauche de la nouvelle racine somme
        if el1.val[1] < el2.val[1] :
            ## on oeut ajotuer directement les 0 et les 1
            el1.val.append(0)
            el2.val.append(1)
            el3 = Tas(el1, somme, el2)
        else :
            el1.val.append(1)
            el2.val.append(0)
            el3 = Tas(el2, somme, el1)


        ## on ajoute ensuite ce nouvel arbre el3 à la file file
        file = file.ajouter(el3)
    file.val.val.append(identifiants.pop(0))

    return file



def calcul_occurrences(t):
    dico = dict()
    
    # Parcourir chaque caractère dans le texte
    for e in t:
        if e in dico : 
            dico[e] += 1
        else :
            dico[e] = 0
    
    # Créer la liste de listes à partir du dictionnaire, avec les clés triées
    res = [[e, dico[e]] for e in dico]
    
    # Retourner le résultat
    return res



def treetograph(t, g, precedent = None) :
    """ transforme un arbre binaire en graphe dictionnaire
    je l'ai créé pour pouvoir récupérer tous les chemins de la racine aux feuilles.
    je n'ai pas trouvé d'autres manières de procéder... """
    if not isinstance(t, Empty) :

        if precedent is not None :
            g.ajouter_noeud(tuple(precedent)) ## on transforme tout en tuple car on ne peut pas mettre de listes en clés des dictionnaires 
            g.ajouter_arc(tuple(precedent), tuple(t.val))
        
        if not isinstance(t.gauche, Empty) : 
            treetograph(t.gauche, g, t.val)
        if not isinstance(t.droite, Empty) : 
            
            treetograph(t.droite, g, t.val)


def treetograph_wrapper(t) : 
    g = GraphD()
    treetograph(t, g)
    return g

def BFS(g, s) :
    """ parcours en largeur du graphe g à partir du point s, en itératif
    ce parcours ne compte pas de distance, mais associe à chaque noeud le noeud qui a permis de l'atteindre"""
    vus = dict() # chaque valeur sra la distance entre la clé et s

    courant = set()
    suivant = set()

    courant.add(s)
    vus[s] = None # s est à une distance 0 de s
    

    while len(courant) != 0 :
        s = list(courant)[0]
        courant.remove(list(courant)[0])

        if isinstance(s[0], int) : 
            for v in g.voisins(s) :
                if not v in vus :
                    suivant.add(v)
                    vus[v] = s

        if len(courant) == 0 :
            courant, suivant = suivant, courant

    return vus


def backtrack_paths(tree):
    # Identifier les feuilles : noeuds dont la valeur (index 0) n'est pas None
    leaves = [node for node in tree if node[0] not in [i for i in range(100, 500)]]

    paths = []

    for leaf in leaves:
        path = []
        current = leaf
        # Remonter jusqu'à la racine (dont le parent est None ou pas dans l'arbre)
        while current is not None:
            path.append(current)
            current = tree.get(current)
        path.reverse()  # Pour avoir de la racine vers la feuille
        paths.append(path)

    return paths

def recuperer_codes_lettres(chemins) :
    """ entrée : une liste de listes qui représentent le chemin de la racine à une feuille
    sortie : le code pour une lettre """
    res = dict()
    for e in chemins :
        res[e[len(e)-1][0]] = str()
        for f in e :
            if len(str(f[2])) != 3 :
                res[e[len(e)-1][0]] += str(f[2])
    return res
            

## ensuite, on doit écrire un code pour coder tout le texte

def encode_huffman(t) :
    """ entrée : un texte au format str
    sortie : sa version copressée et le tas, utile poiur décompresser le texte """
    liste = calcul_occurrences(t)

    c = Huffman2(liste).val



    a = treetograph_wrapper(c)
    


    b = BFS(a, tuple(c.val))
    d = backtrack_paths(b)

    e = recuperer_codes_lettres(d)

    ## ensuite, on encode :
    res = str()
    for f in t :
        res += e[f]
    return res, c ## on renvoie aussi l'arbre binaire ! 




def decode_huffman(code, a) :
    """ entrée :
        le code code sous forme de str, composé de 0 et de 1
        l'arbre a qui contient le chemin de la racine aux feuilles
        sortie :
        le code décodé

        le processus :
        tant que code n'est pas de longueur 0 :
        - on parcourt caractère par caractère le code code
        - en même temps, on s'oriente dans l'arbre
        - si on a un 0, on va a droite, sinon on va a gauche
        - quand on tombe sur une feuille, on l'ajoute à notre code décompressé
        """
    import copy
    a2 = copy.deepcopy(a)
    res = str()
    while len(code) != 0 :
        bit = code[0]
        code = code[1:]
        if bit == "1" :
            a2 = a2.droite
        else : ## si bit == 0
            a2 = a2.gauche

        #if a2.val[0] is not None :
        if isinstance(a2.val[0], str) : 
            res += a2.val[0]
            a2 = a ## on repart de la racine !
    return res
    
        
##  procédure de test           
def test(fichier) : 
    test = open(fichier, "r")
    txt = test.read()

    a = encode_huffman(txt)
    l = len(a[0])
    print("longueur du texte non encodé (en nombre de bits) : ", len(txt)*8, "\nlongueur du texte encodé par Huffman : ", len(a[0]), "\nle texte encodé est ", len(txt)*8/len(a[0]), " fois plus petit que le texte non encodé")
    
    return a

