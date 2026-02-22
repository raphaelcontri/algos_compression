# algos_compression

cette archive contient deux algorithmes de compression de textes : 


1. Huffman : 
Les fonctions à utliser sont encode_huffman et decode_huffman. 
Le fonctionnement de huffman : 
1 : on calcule les occurrences de chaque caractère utilisé dans le texte
2 : on initialise une file de priorité qui contient des tas de taille 1 donc la seule valeur est une lettre et son nombre d'occurrences associée
3 : on fait tourner l'algo de huffman : a chaque itération on prend les deux tas en haut de la file et on aditionne leur valeur. Ces deux tas deviennent sous tas d'une racine donc la valeur est la somme des valeurs des deux sous tas. En même teps, on ajoute les 0 et les 1 qui permettront d'encoder les caractères
4. Ensuite, on transforme cette file de priorité en un graphe dictionnaire
5. On fait un BFS sur ce graphe, on obtient donc un dictionnaire avec en clé les noeuds du graphe et en valeur le noeud qui a permis de l'atteindre
6. De cette façon, on peut récupérer le chemin d'une racine de l'arbre à une feuille, et ainsi reconstruire le code poiur chaque caractère du texte.
7. Finalement, on encode chaque lettre du texte et on renvoie le texte codé ainsi que le tas qui a permis d'encoder chaque lettre. 

Pour décoder, on utilise decode_huffman, avec en paramètre le code et l'arbre fourni a l'encodage. Le décodage est beaucoup plus simple et est décrit dans la docstring de la fonction. 



2. LZW : 
Les fonctions encode_lzw et decode_lzw sont commentées. 




3. Les résultats : comparaison des compressions avec les livres du tour du monde en 80 jours et roméo & juliet

pour le roman de jules verne : 

- avec Huffman, j'ai obtenu : 
longueur du texte non encodé (en nombre de bits) :  6798096 
longueur du texte encodé par Huffman :  3881104 
le texte encodé est  1.751588207891363  fois plus petit que le texte non encodé


Avec LZW : 
longueur du texte non encodé :  849762 
longueur du texte encodé par LZW :  154967 
le texte encodé est  5.483502939335471  fois plus petit que le texte non encodé





Pour roméo et Juliette, j'ai obtenu : 


avec Huffman
longueur du texte non encodé (en nombre de bits) :  1133560 
longueur du texte encodé par Huffman :  681852 
le texte encodé est  1.6624722080451477  fois plus petit que le texte non encodé


- avec LZW, j'ai obtenu : 
longueur du texte non encodé :  141695 
longueur du texte encodé par LZW :  35874 
le texte encodé est  3.9497965100072476  fois plus petit que le texte non encodé









==> conclusion : Huffman compresse beaucoup moins que LZW
En revanche, en ce qui concerne le temps d'execution, Huffman est beaucoup plus rapide (répond quasi instantannément) que LZW (presque une minute pour le plus plus gros livre)
De plus, on peut émettre l'hypothèse que plus le texte est long, plus la différence de pourcentage compressé augente entre les deux algorithmes. 

