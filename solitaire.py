ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def lettre_en_nombre(x):
    return ALPHABET.index(x.upper()) + 1

def nombre_en_lettre(x):
    return ALPHABET[x - 1]

def deplacer_joker_noir(jeu):
    i = jeu.index(53)
    j = (i + 1) % len(jeu)
    jeu[i], jeu[j] = jeu[j], jeu[i]

def deplacer_joker_rouge(jeu):
    i = jeu.index(54)
    for _ in range(2):
        j = (i + 1) % len(jeu)
        jeu[i], jeu[j] = jeu[j], jeu[i]
        i = j

def double_coupe(jeu):
    j1 = jeu.index(53)
    j2 = jeu.index(54)
    haut = min(j1, j2)
    bas = max(j1, j2)

    partie_haut = jeu[:haut]
    partie_milieu = jeu[haut:bas+1]
    partie_bas = jeu[bas+1:]

    jeu[:] = partie_bas + partie_milieu + partie_haut

def coupe_par_derniere_carte(jeu):
    derniere = jeu[-1]
    if derniere >= 53:
        n = 53
    else:
        n = derniere

    if n < 53:
        partie_sans_derniere = jeu[:-1]
        dessus = partie_sans_derniere[:n]
        reste = partie_sans_derniere[n:]
        jeu[:] = reste + dessus + [jeu[-1]]

def lire_cle(jeu):
    premiere = jeu[0]
    if premiere >= 53:
        return None

    carte_lue = jeu[premiere]
    if carte_lue >= 53:
        return None
    
    if carte_lue > 26:
        carte_lue -= 26
    
    return carte_lue

def generer_cle_solitaire(jeu):
    deplacer_joker_noir(jeu)
    deplacer_joker_rouge(jeu)
    double_coupe(jeu)
    coupe_par_derniere_carte(jeu)
    return lire_cle(jeu)

def generer_flux_cles(jeu, longueur):
    flux = []
    while len(flux) < longueur:
        cle = generer_cle_solitaire(jeu)
        if cle is not None:
            flux.append(cle)
    return flux

def chiffrer_msg(message, jeu):
    message_maj = message.upper()
    lettres = [c for c in message_maj if 'A' <= c <= 'Z']
    msg_filtre = "".join(lettres)
    
    cles = generer_flux_cles(jeu, len(msg_filtre))
    resultat = []
    for i, lettre in enumerate(msg_filtre):
        val_lettre = lettre_en_nombre(lettre)
        val_cle = cles[i]
        s = val_lettre + val_cle
        if s > 26:
            s -= 26
        resultat.append(nombre_en_lettre(s))
    return "".join(resultat)

def dechiffrer_msg(message_chiffre, jeu):
    msg_c = "".join(c for c in message_chiffre.upper() if 'A' <= c <= 'Z')
    cles = generer_flux_cles(jeu, len(msg_c))
    resultat = []
    for i, lettre in enumerate(msg_c):
        val_chiffre = lettre_en_nombre(lettre)
        val_cle = cles[i]
        p = val_chiffre - val_cle
        if p < 1:
            p += 26
        resultat.append(nombre_en_lettre(p))
    return "".join(resultat)