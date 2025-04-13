# Mini-projet Crypto : Méthode Solitaire (Bruce Schneier)

KUT Kemal & KEITA Sidy Mahmoud 
TP1

Mini-projet de cryptographie implémentant la méthode Solitaire (conçue par Bruce Schneier), ainsi qu’une interface graphique réalisée avec PyQt5 pour tester le chiffrement et le déchiffrement de messages.

Solitaire est un algorithme de chiffrement par flux de clés générées à partir d’un simple jeu de cartes de 54 cartes (52 cartes standard + 2 jokers). Il permet de produire, pour chaque lettre du message, une valeur pseudo-aléatoire (1..26) et de l’additionner (mod 26) ou la soustraire (mod 26) au texte pour le chiffrer/déchiffrer.

