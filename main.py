#!/usr/bin/python3

import random
import re, operator 

print ("-----------------  WELCOME TO THE GAME NIM ----------------- " ) 

class player:
	name = ""
	bast_score = 0
	last_score = 0 
	scores = []

	 def __init__(self, name):
		self.name = name.strip()

	 def setScores(self, scores):
		self.scores = scores
		self.scores = scores
		self.best_score = max(scores)
		self.last_score = scores[0] 

	def addScore(self, new_score):
		self.scores = [new_score] + self.scores
		self.last_score = new_score
		if new_score > self.best_score:
		    self.best_score = new_score
	def show(self):
		print self.name + ", dernier score = " , self.last_score , ", meilleur score = ", self.best_score

	 def play(self, jeu):
		print self.name, ", c'est votre tour, introduisez <Numero du tas> - <Nombre de pierres a retirer>"
		while True:
		    user_input = raw_input()
		    if (not re.match("(\d+)\s*-?\s*(\d+)", user_input)):
		        print "le format specifié est incorrecte"
		        print "ressayez avec ce format : Numero du tas - Nombre de pierres a retirer"
		        continue
		    m = re.search("(\d+)\s*-?\s*(\d+)", user_input)

		    numero_de_tas = int(m.group(1))
		    nbr_pierres = int(m.group(2))
		    if jeu.try_to_play(numero_de_tas, nbr_pierres):
		        break
		    else:
		        print "redonnez <Numero du tas> - <Nombre de pierres a retirer>"

while True:
    jeu = Jeu("saves.txt")

    jeu.player1 = jeu.find_player(raw_input("Veuillez entrer le nom du joueur 1 : "))
    jeu.player2 = jeu.find_player(raw_input("Veuillez entrer le nom du joueur 2 : "))

    nbr_de_tas = random.randint(3, 7)
    for i in range(0, nbr_de_tas, 1):
        jeu.tas = jeu.tas + [random.randint(5, 23)]

print ("---------------------- le jeu commence ----------------------")
