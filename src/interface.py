import random
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton
)
from solitaire import (
    chiffrer_msg,
    dechiffrer_msg
)

class Fenetre(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini-projet crypto")
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout()
        widget_central.setLayout(layout_principal)
        
        self.label_saisie = QLabel("Tapez votre message :")
        self.input_message = QTextEdit()
        layout_principal.addWidget(self.label_saisie)
        layout_principal.addWidget(self.input_message)
        
        layout_boutons = QHBoxLayout()
        self.bouton_chiffrer = QPushButton("Chiffrer")
        self.bouton_dechiffrer = QPushButton("Déchiffrer")
        layout_boutons.addWidget(self.bouton_chiffrer)
        layout_boutons.addWidget(self.bouton_dechiffrer)
        layout_principal.addLayout(layout_boutons)
        
        self.label_resultat = QLabel("Résultat :")
        self.zone_resultat = QTextEdit()
        self.zone_resultat.setReadOnly(True)
        layout_principal.addWidget(self.label_resultat)
        layout_principal.addWidget(self.zone_resultat)
        
        self.label_log = QLabel("Détails de l'algo :")
        self.zone_log = QTextEdit()
        self.zone_log.setReadOnly(True)
        layout_principal.addWidget(self.label_log)
        layout_principal.addWidget(self.zone_log)
        
        self.bouton_chiffrer.clicked.connect(self.action_chiffrer)
        self.bouton_dechiffrer.clicked.connect(self.action_dechiffrer)
        
        cartes = list(range(1, 55))
        random.shuffle(cartes)
        self.jeu_initial = cartes

    def action_chiffrer(self):
        self.zone_log.clear()
        message_clair = self.input_message.toPlainText()
        deck_clone = self.jeu_initial[:] 
        texte_chiffre, log = chiffrer_msg(message_clair, deck_clone)
        self.zone_resultat.setHtml(f"<p><b>Résultat :</b> {texte_chiffre}</p>")
        self.zone_log.setHtml(log)

    def action_dechiffrer(self):
        self.zone_log.clear()
        message_chiffre = self.input_message.toPlainText()
        deck_clone = self.jeu_initial[:] 
        texte_dechiffré, log = dechiffrer_msg(message_chiffre, deck_clone)
        self.zone_resultat.setHtml(f"<p><b>Résultat :</b> {texte_dechiffré}</p>")
        self.zone_log.setHtml(log)
