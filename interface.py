from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton
)
from solitaire import chiffrer_msg, dechiffrer_msg

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
        self.input_message.setPlaceholderText("Saisissez un message ici...")
        
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
        
        self.bouton_chiffrer.clicked.connect(self.action_chiffrer)
        self.bouton_dechiffrer.clicked.connect(self.action_dechiffrer)
        
        self.jeu_initial = list(range(1, 55))
    
    def action_chiffrer(self):
        message_clair = self.input_message.toPlainText()
        jeu_pour_chiffrement = self.jeu_initial[:]
        
        texte_chiffre = chiffrer_msg(message_clair, jeu_pour_chiffrement)
        self.zone_resultat.setText(texte_chiffre)
    
    def action_dechiffrer(self):
        message_chiffre = self.input_message.toPlainText()
        jeu_pour_dechiffrement = self.jeu_initial[:]
        
        texte_dechiffre = dechiffrer_msg(message_chiffre, jeu_pour_dechiffrement)
        self.zone_resultat.setText(texte_dechiffre)
