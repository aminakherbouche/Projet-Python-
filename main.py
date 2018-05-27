
import random   
import re, operator  


class Player:
    name = ""
    best_score = 0
    last_score = 0
    scores = []
    coups = 0     # nombre de coups jouees

    def __init__(self, name):
        self.name = name.strip()  # effacer les  espaces   

    def setScores(self, scores):
        self.scores = scores
        self.scores = scores
        self.best_score = max(scores)
        self.last_score = scores[0]  # last score = first element in scores list

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
                print "le format specifie est incorrecte"
                print "ressayez avec ce format : Numero du tas - Nombre de pierres a retirer"
                continue
            m = re.search("(\d+)\s*-?\s*(\d+)", user_input)

            numero_de_tas = int(m.group(1))
            nbr_pierres = int(m.group(2))
            if jeu.try_to_play(numero_de_tas, nbr_pierres):
                break
            else:
                print "redonnez <Numero du tas> - <Nombre de pierres a retirer>"
        self.coups += 1 # nombre de coups jouees

class Jeu:
    round = 0
    tas = []
    player1 = Player
    player2 = Player

    saves_file = "saves.txt"
    players = []

    def __init__(self, saves_file_name):
        self.saves_file = saves_file_name
        try:
            saves = open(saves_file_name, 'r')
        except:
            saves = open(saves_file_name, 'w')
            saves.close()
            saves = open(saves_file_name, 'r')

        lines = saves.readlines()
        for line in lines:
            if (not re.match("([\w_]+)(.*)", line)):
                continue
            m = re.search("([\w_]+)(.*)", line)
            player = Player(m.group(1))
            line = m.group(2)
            line.replace(player.name, "")
            scores = line.split(' ')
            scores = [int(x) for x in scores if x != " " and x != ""]  # filtrer les espaces
            player.setScores(scores)
            self.players.append(player)

        saves.close()

    def find_player(self, player_name):
        for x in self.players:
            if x.name == player_name:
                x.show()
                return x
        # si le joueur est non trouve
        player = Player(player_name)
        self.players.append(player)
        return player

    def try_to_play(self, numero_de_tas, nbr_pierres):
        if len(self.tas) < numero_de_tas:
            print "numero de tas tres grand (maximum ", len(self.tas),")"
            return False
        elif numero_de_tas < 0:
            print "numero de tas negatif !"
            return False
        elif nbr_pierres < 1:
            print "nombre de pierres doit etre 1 ou plus"
            return False
        elif self.tas[numero_de_tas-1] == 0:
            print "ce tas (numero ",numero_de_tas,") est vide, prennez d'un autre tas"
            return False
        else:
            self.tas[numero_de_tas-1] -= min([nbr_pierres, self.tas[numero_de_tas-1]])
            return True


    def afficher_etat(self):
        print self.player1.name + " vs " + self.player2.name
        max_nbr_pierres = max(self.tas)
        i = 1
        for nbr_pierres in self.tas:
            print i , "| " , "*" * nbr_pierres , " " * (max_nbr_pierres - nbr_pierres) , " |", nbr_pierres
            i = i + 1

    def fini(self):
        if sum(self.tas) <= 1:
            return True
        else:
            return False

    def next_round(self):
        if self.round == 0:
            self.player1.play(self)
            self.round = 1
        elif self.round == 1:
            self.player2.play(self)
            self.round = 0

    def calculer_scores(self):
        score = ""
        for i in range(0,self.winner().coups+1): # methode plus optimisee : les scores sont du format 543210, 43210, 210 ... etc
            score = str(i)+score

        if self.round == 1:
            self.player2.addScore(0) #ajouter un score nul
            self.player1.addScore(int(score))
            print "score = ", int(score), "(coups joues = ", self.winner().coups, ")"
        else:
            self.player1.addScore(0)  # ajouter un score nul
            self.player2.addScore(int(score))
            print "score = ", int(score), "(coups joues = ", self.winner().coups, ")"

    def fermer_et_sauvegarder(self):
        saves = open(self.saves_file,'w')
        saves.truncate()
        for player in self.players:
            saves.write(player.name)
            for score in player.scores:
                saves.write(" "+str(score))
            saves.write("\n")
        saves.close()


    def show_winner(self):
        if self.round == 1:
            print "le gagnant est ", self.player1.name
        elif self.round == 0:
            print "le gagnant est ", self.player2.name

    def winner(self):
        if self.round == 1:
            return self.player1
        elif self.round == 0:
            return self.player2

    def looser(self):
        if self.round == 1:
            return self.player2
        elif self.round == 0:
            return self.player1

    def show_best_10_scores(self):
        best_scores = {}
        for p in self.players:
            for score in p.scores:
                best_scores[p.name+','+str(score)] = score


        i = 1
        print "meilleurs 10 scores"
        for name, score in sorted(best_scores.items(), key=operator.itemgetter(1), reverse=True):
            if i > 10 :
                break
            print i,". ",str(name).split(',')[0] , "\t : ", score
            i += 1




# ================================================================================
while True:
    jeu = Jeu("saves.txt")
    print ("\n \n ------------------  WELCOME TO THE GAME NIM ----------------- \n \n"  )
    jeu.player1 = jeu.find_player(raw_input("donnez le nom du premier joueur : "))
    jeu.player2 = jeu.find_player(raw_input("donnez le nom de deuxieme joueur : "))

    nbr_de_tas = random.randint(3, 7)
    for i in range(0, nbr_de_tas, 1):
        jeu.tas = jeu.tas + [random.randint(5, 23)]

    print "\n ---------------------- le jeu commence ---------------------- \n"
  
    jeu.afficher_etat()
    

    while not jeu.fini():
        jeu.next_round()
        jeu.afficher_etat()
    print "\n---------------------- le jeu est fini ----------------------\n"
    jeu.show_winner()
    jeu.calculer_scores()
    jeu.fermer_et_sauvegarder()
    print "\n--------------------------------------------"
    jeu.show_best_10_scores()

    if(raw_input("voulez vous rejouer ? <1> oui,  <0> non  : ").strip() in ["0","n","non"]):
        break


    
# ================================================================================
