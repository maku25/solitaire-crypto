#joker noir = 53 et rouge = 54

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def lettre_en_nombre(x):
    return alphabet.index(x.upper()) + 1

def nombre_en_lettre(x):
    return alphabet[x - 1]

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
    n = 53 if derniere >= 53 else derniere
    if n < 53:
        partie_sans_derniere = jeu[:-1]
        dessus = partie_sans_derniere[:n]
        reste = partie_sans_derniere[n:]
        jeu[:] = reste + dessus + [jeu[-1]]

def formatter_deck(jeu):
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

def generer_flux_cles_verbose(jeu, longueur):
    flux = []
    full_log = []
    deck_temp = jeu[:] 
    cle, log = generer_cle_solitaire(deck_temp)
    full_log.extend(log)
    if cle is not None:
        flux = [cle] * longueur
    return flux, full_log

def chiffrer_msg(message, jeu):
    message_maj = message.upper()
    lettres = [c for c in message_maj if 'A' <= c <= 'Z']
    msg_filtre = "".join(lettres)
    
    cles, log_global = generer_flux_cles_verbose(jeu, len(msg_filtre))
    
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
    msg_c = "".join(c for c in message_chiffre.upper() if 'A' <= c <= 'Z')
    cles, log_global = generer_flux_cles_verbose(jeu, len(msg_c))
    
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
