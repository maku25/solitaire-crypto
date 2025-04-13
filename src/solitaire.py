#joker noir = 53 et rouge = 54

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def lettre_en_nombre(x):
    return alphabet.index(x.upper()) + 1

def nombre_en_lettre(x):
    return alphabet[x - 1]

def deplacer_joker_noir(jeu):
    """
    Déplace le Joker noir (=53) d'une position vers le bas.
    Si le Joker noir est en dernière position, il se déplace en deuxième position.
    """
    i = jeu.index(53)
    j = (i + 1) % len(jeu)
    jeu[i], jeu[j] = jeu[j], jeu[i]

def deplacer_joker_rouge(jeu):
    """
    Déplace le Joker rouge (=54) de deux positions vers le bas
    """
    i = jeu.index(54)
    for _ in range(2):
        j = (i + 1) % len(jeu)
        jeu[i], jeu[j] = jeu[j], jeu[i]
        i = j

def double_coupe(jeu):
    """
    On identifie les deux jokers et on divise le deck en trois 'mini-pacquets' :
      - Toutes les cartes avant le premier joker,
      - Les deux jokers et tout ce qui est entre eux,
      - Toutes les cartes après le second joker.
    Ensuite, on échange le premier et le dernier mini pacquet.
    """
    j1 = jeu.index(53)
    j2 = jeu.index(54)
    haut = min(j1, j2)
    bas = max(j1, j2)
    partie_haut = jeu[:haut]
    partie_milieu = jeu[haut:bas+1]
    partie_bas = jeu[bas+1:]
    jeu[:] = partie_bas + partie_milieu + partie_haut

def coupe_par_derniere_carte(jeu):
    """
    Effectue la coupe par rapport à la dernière carte n,
    On déplace les n premières cartes du haut du deck et on les insère
    juste avant la dernière carte.
    """
    derniere = jeu[-1]
    n = 53 if derniere >= 53 else derniere
    if n < 53:
        partie_sans_derniere = jeu[:-1]
        dessus = partie_sans_derniere[:n]
        reste = partie_sans_derniere[n:]
        jeu[:] = reste + dessus + [jeu[-1]]

def formatter_deck(jeu):
    """
    POUR L'AFFICHAGE
    Retourne une chaîne HTML représentant l'état du pacquet de carte.
    """
    formatted_cards = []
    for card in jeu:
        if card == 53:
            formatted_cards.append("<span style='color: black; font-weight: bolder';>53</span>")
        elif card == 54:
            formatted_cards.append("<span style='color: red; font-weight: bolder';>54</span>")
        else:
            formatted_cards.append(f"<span style='color: gray'>{card}</span>")
    return "[" + ", ".join(formatted_cards) + "]"

def lire_cle(jeu):
    """
    Effectue la lecture de la clé en détaillant les étapes :
      - Affiche la première carte du pacquet qui détermine l'indice.
      - Affiche la carte lue à cet indice.
      - Si cette carte > 26, on fait %26.
    Retourne un tuple (cle, log) où:
      - cle est la clé (entre 1 et 26) ou None si une erreur (joker) survient,
      - log est une liste de chaînes HTML détaillant le calcul (POUR L'AFFICHAGE).
    """
    log = []
    premiere = jeu[0]
    log.append(f"<b>première carte [0]</b> {premiere}")
    if premiere >= 53:
        log.append("<span style='color: red;'>première carte = joker → clé invalide (None)</span>")
        return None, log

    carte_lue = jeu[premiere]
    log.append(f"<b>carte lue à l'index {premiere}:</b> {carte_lue}")
    if carte_lue >= 53:
        log.append("<span style='color: red;'>carte lue = joker → clé invalide (None)</span>")
        return None, log

    if carte_lue > 26:
        nouvelle_valeur = carte_lue - 26
        log.append(f"<b>carte lue ({carte_lue}) > 26:</b> donc %26 = {nouvelle_valeur}")
        cle_finale = nouvelle_valeur
    else:
        log.append(f"carte lue ({carte_lue})")
        cle_finale = carte_lue

    log.append(f"<b>clé généré :</b> {cle_finale}")
    return cle_finale, log

def generer_cle_solitaire(jeu):
    """
    Exécute les 5 opérations de l'algorithme Solitaire.
    Retourne (cle, log), où cle est la clé obtenue et log est le détail en HTML (pr l'affichage).
    """
    log = []
    log.append(f"<b>paquet de carte initial</b> {formatter_deck(jeu)}")
    
    deplacer_joker_noir(jeu)
    log.append(f"<b>joker noir --1</b> {formatter_deck(jeu)}")
    
    deplacer_joker_rouge(jeu)
    log.append(f"<b>joker rouge --2</b> {formatter_deck(jeu)}")
    
    double_coupe(jeu)
    log.append(f"<b>double coupe</b> {formatter_deck(jeu)}")
    
    coupe_par_derniere_carte(jeu)
    log.append(f"<b>coupe simple</b> {formatter_deck(jeu)}")
    
    cle, log_calcul = lire_cle(jeu)
    log.extend(log_calcul)
    
    return cle, log

def generer_flux_cles(jeu, longueur):
    """
    Génère le flux de clés nécessaire pour chiffrer ou déchiffrer un message.
    Retourne (flux, full_log) où:
      - flux est une liste contenant la même clé répétée 'longueur' fois,
      - full_log est le log détaillé (HTML) du calcul de la clé.
    """
    flux = []
    full_log = []
    deck_temp = jeu[:] 
    cle, log = generer_cle_solitaire(deck_temp)
    full_log.extend(log)
    if cle is not None:
        flux = [cle] * longueur
    return flux, full_log

def chiffrer_msg(message, jeu):
    """
    Chiffre un message en utilisant l'algorithme Solitaire.
    """
    message_maj = message.upper()
    lettres = [c for c in message_maj if 'A' <= c <= 'Z']
    msg_filtre = "".join(lettres)
    
    cles, log_global = generer_flux_cles(jeu, len(msg_filtre))
    
    resultat = []
    log_detail = []
    cle = cles[0] if cles else None
    for i, lettre in enumerate(msg_filtre):
        val_lettre = lettre_en_nombre(lettre)
        calcul = f"{val_lettre} (<b>{lettre}</b>) + {cle} (clé)"
        somme = val_lettre + cle
        if somme > 26:
            calcul += f" = {somme} → %26 {somme - 26}"
            somme -= 26
        else:
            calcul += f" = {somme}"
        lettre_result = nombre_en_lettre(somme)
        calcul += f"=> <b>'{lettre_result}'</b>"
        log_detail.append(f"<p style='margin:2px;'><span style='color: blue;'>Lettre {i+1} :</span> {calcul}</p>")
        resultat.append(lettre_result)
    
    texte_chiffre = "".join(resultat)
    log_global.append(f"<p><b>msg: <b> {msg_filtre}</p>")
    log_global.append(f"<p><b>msg chiffré</b> {texte_chiffre}</p>")
    full_log_combined = "<br>".join(log_global + log_detail)
    
    return texte_chiffre, full_log_combined

def dechiffrer_msg(message_chiffre, jeu):
    """
    Déchiffre le message
    """
    msg_c = "".join(c for c in message_chiffre.upper() if 'A' <= c <= 'Z')
    cles, log_global = generer_flux_cles(jeu, len(msg_c))
    
    resultat = []
    log_detail = []
    cle = cles[0] if cles else None
    for i, lettre in enumerate(msg_c):
        val_chiffre = lettre_en_nombre(lettre)
        calcul = f"{val_chiffre} (<b>'{lettre}'</b>) - {cle}"
        diff = val_chiffre - cle
        if diff < 1:
            calcul += f" = {diff} → %26 {diff + 26}"
            diff += 26
        else:
            calcul += f" = {diff}"
        lettre_result = nombre_en_lettre(diff)
        calcul += f"=> <b>'{lettre_result}'</b>"
        log_detail.append(f"<p style='margin:2px;'><span style='color: blue;'>Lettre {i+1} :</span> {calcul}</p>")
        resultat.append(lettre_result)
    
    texte_dechiffré = "".join(resultat)
    log_global.append(f"<p><b>msg chiffré:</b> {msg_c}</p>")
    log_global.append(f"<p><b>msg déchiffré:</b> {texte_dechiffré}</p>")
    full_log_combined = "<br>".join(log_global + log_detail)
    
    return texte_dechiffré, full_log_combined
