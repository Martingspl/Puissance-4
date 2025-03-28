import random
import pygame
import copy

def exploitation(possibilite,j,ia):
    """
    Entrée : Colonnes jouables + Joueur
    Sortie : Colonnes à jouer selon l'ia dans un tableau
    """
    h = copy.deepcopy(ia[0])
    for l in range(len(ia[0])):
        for i in range(6):
            for k in range(3):
                h[l][i][k] = ia[0][l][i][6-k]
                h[l][i][6-k] = ia[0][l][i][k]
    # Trouve la récompense pour chaque possibilite
    score = [0] * len(possibilite)
    for c in range(len(possibilite)):
        jouer(j,possibilite[c])
        for i in range(len(ia[0])):
            if g == ia[0][i] or g == h[i]:
                score[c] = ia[1][i]
                break
        retire_un_coup(possibilite[c])
    # Choisit la colonne avec la plus grande récompense
    meilleur_score = score[0]
    col_gagnante = []
    for i in range(len(possibilite)):
        if score[i] > meilleur_score:
            meilleur_score = score[i]
            col_gagnante = [possibilite[i]]
        elif meilleur_score == score[i]:
            col_gagnante.append(possibilite[i])
    if montrer == 1:
        print("Scores:               ",score)

    return col_gagnante

def rewards(partie,gain,j,ia):
    """
    Entrée : Partie d'un joueur + s'il a gagné ou non + son numéro
    Effets : Alimente l'ia
    """
    if len(partie) == 0:
        return
    # Échange les pions
    if j == 1:
        for i in range(len(partie)):
            for k in range(len(partie[i])):
                for l in range(len(partie[i][k])):
                    if partie[i][k][l] == 1:
                        partie[i][k][l] = 2
                    elif partie[i][k][l] == 2:
                        partie[i][k][l] = 1
    # Pour la première récompense
    if partie[-1] in ia[0]:
        for i in range(len(ia[0])):
            if partie[-1] == ia[0][i]:
                gain = ia[1][i] + learning_rate * (gain - ia[1][i])
                ia[1][i] = gain
    else:
        ia[0].append(partie[-1])
        ia[1].append(gain)
    # Pour le reste de la partie
    for m in range(len(partie) - 2, -1, -1):
        if partie[m] in ia[0]:
            for i in range(len(ia[0])):
                if partie[m] == ia[0][i]:
                    gain = ia[1][i] + learning_rate * (gain - ia[1][i])
                    ia[1][i] = gain
        else:
            ia[0].append(partie[m])
            ia[1].append(gain)
            gain = learning_rate * gain
            ia[1][-1] = gain
    return ia

def alimente_partie(j,c,g,partie_j1,partie_j2,apprendre,ia):
    """
    Entrée : Tout
    Effets : Alimente les parties
    Sortie : Renvoie le joueur s'il gagne
    """
    if victoire(j,c,g) == True:
        if apprendre == True and (len(partie_j1) and len(partie_j2)) > 0 :
            if j == 1:
                ia = rewards(partie_j1,1,1,ia)
                ia = rewards(partie_j2,-1,2,ia)
            else:
                ia = rewards(partie_j1,-1,1,ia)
                ia = rewards(partie_j2,1,2,ia)
        partie_j1 = []
        partie_j2 = []
        return j
    h = copy.deepcopy(g)
    if h not in ia[0]:
        for i in range(6):
            for k in range(3):
                h[i][k] = g[i][6-k]
                h[i][6-k] = g[i][k]
    if j == 1:
        partie_j1.append(h)
    else:
        partie_j2.append(h)
    return 0

def entrainement_ia(nb_exp,lr,ia,apprendre,exploite,anticipation):
    """
    Entrée : Nombre d'expérience + Learning rate + s'il apprend
    Sortie : Renvoie des états associés à une récompense
    """
    global learning_rate
    learning_rate = lr
    for i in range(nb_exp):
        g_vide()
        j = 1
        partie_ia1 = []
        partie_ia2 = []
        k = 0
        while k < 42:
            c = ia_j(j,exploite,g,anticipation)
            jouer(j,c)
            gagne = alimente_partie(j,c,g,partie_ia1,partie_ia2,apprendre,ia)
            if gagne != 0:
                break
            j = change_j(j)
            k += 1
            #print(k)
        print(i)
    #print("Temps de l'entrainement:", round(end - start, 1), "secondes")

def g_vide():
    global g
    g = [[0 for j in range (7)]for i in range (6)]
    global cases_vides
    cases_vides = [6,6,6,6,6,6,6]

def jouer(j,c):
    g[cases_vides[c]-1][c] = j
    cases_vides[c] -= 1

def change_j(j):
    if j == 1:
        return 2
    return 1

def victoire(j,c,g):
    """
    Entrée : Joueur + Colonne
    Sortie : Test si le joueur gagne en ayant joué cette colonne
    """
    l = cases_vides[c]
    for i in range(4):
        if g[l][i] == j and g[l][i+1] == j and g[l][i+2] == j and g[l][i+3] == j or l-3+i >= 0 and c-3+i >= 0 and l+i <= 5 and c+i <= 6 and g[l-3+i][c-3+i] == j and g[l-2+i][c-2+i] == j and g[l-1+i][c-1+i] == j and g[l+i][c+i] == j or l-3+i >= 0 and c+3-i <= 6 and l+i <= 5 and c-i >= 0 and g[l-3+i][c+3-i] == j and g[l-2+i][c+2-i] == j and g[l-1+i][c+1-i] == j and g[l+i][c-i] == j :
            return True
    for i in range(3):
        if g[i][c] == j and g[i+1][c] == j and g[i+2][c] == j and g[i+3][c] == j :
            return True
    return False

def retire_un_coup(c):
    """
    Entrée : une colonne
    Effet : retire le dernier pion de la colonne
    """
    g[cases_vides[c]][c] = 0
    cases_vides[c] += 1

def affiche(g):
    print("1 2 3 4 5 6 7")
    for i in range (6):
        for j in range (7):
            if g[i][j] == 0 :
                print(". ", end="")
            if g[i][j] == 1 :
                print("O ", end="")
            if g[i][j] == 2 :
                print("X ", end="")
        print()
    print()
    return g

def puissance_4_pygame(apprendre,exploite,ia,anticipation):
    """
    Effets : Permet de jouer au puissance 4
    """
    pygame.init()
    plateau = pygame.display.set_mode((900,600))
    plateau.fill((250,250,250))
    pygame.display.flip()
    pygame.display.set_caption("Puissance 4")

    global g
    global cases_vides
    g_vide()
    j = 1
    jeu = 2
    gagne = 0
    sauvegarde = [[copy.deepcopy(g),j,copy.deepcopy(cases_vides)]]
    partie_j1 = []
    partie_j2 = []

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                c = event.pos[0]//100
                if event.pos[0] < 700 and cases_vides[c] > 0 and gagne == 0:
                    sauvegarde.append([copy.deepcopy(g),j,copy.deepcopy(cases_vides)])
                    if jeu == 1:
                        jouer(1,c)
                        gagne = alimente_partie(1,c,g,partie_j1,partie_j2,apprendre,ia)
                        if gagne == 0 and cases_vides != [0,0,0,0,0,0,0]:
                            c = ia_j(2,exploite,g,anticipation)
                            jouer(2,c)
                            gagne = alimente_partie(2,c,g,partie_j1,partie_j2,apprendre,ia)
                    else:
                        jouer(j,c)
                        gagne = alimente_partie(j,c,g,partie_j1,partie_j2,apprendre,ia)
                        j = change_j(j)

                elif event.pos[0] > 730 and event.pos[0] < 870 and event.pos[1] > 475 and event.pos[1] < 550:
                    if gagne == 0 and cases_vides != [0,0,0,0,0,0,0] and jeu == 2:
                        sauvegarde.append([copy.deepcopy(g),j,copy.deepcopy(cases_vides)])
                        c = ia_j(j,exploite,g,anticipation)
                        jouer(j,c)
                        gagne = alimente_partie(j,c,g,partie_j1,partie_j2,apprendre,ia)
                        j = change_j(j)

                elif event.pos[0] > 730 and event.pos[0] < 870 and ((event.pos[1] > 25 and event.pos[1] < 100) or (event.pos[1] > 125 and event.pos[1] < 200) or (event.pos[1] > 225 and event.pos[1] < 300) or (event.pos[1] > 350 and event.pos[1] < 425)):
                    partie_j1 = []
                    partie_j2 = []
                    gagne = 0
                    if event.pos[1] > 350 and event.pos[1] < 425 :
                        g = copy.deepcopy(sauvegarde[-1][0])
                        j = sauvegarde[-1][1]
                        cases_vides = copy.deepcopy(sauvegarde[-1][2])
                        if len(sauvegarde) > 1 :
                            sauvegarde.remove(sauvegarde[-1])
                        else:
                            sauvegarde = [[[[0 for j in range (7)]for i in range (6)],1,[6 for i in range(7)]]]
                    else:
                        jeu = 1
                        g = [[0 for j in range (7)]for i in range (6)]
                        cases_vides = [6,6,6,6,6,6,6]
                        if event.pos[1] > 125 and event.pos[1] < 200 :
                            jouer(2,ia_j(2,exploite,g,anticipation))
                            if apprendre == True:
                                partie_j2.append(copy.deepcopy(g))
                        elif event.pos[1] > 225 and event.pos[1] < 300 :
                            jeu = 2
        affiche_pygame(plateau,g,gagne)
        pygame.display.update()
    pygame.quit()
    quit()

def affiche_pygame(plateau,g,gagne):
    """
    Effets : Affiche l'interface du puissance 4
    """
    pygame.draw.rect(plateau, (0,170,0), (730, 25, 140, 75))
    a = pygame.font.SysFont('Arial', 45)
    a = a.render("1 joueur", 5, (0,0,0))
    plateau.blit(a, (730, 35))
    pygame.draw.rect(plateau, (0,170,0), (730, 125, 140, 75))
    a = pygame.font.SysFont('Arial', 35)
    a = a.render("1 joueur", 5, (0,0,0))
    plateau.blit(a, (745, 125))
    a = pygame.font.SysFont('Arial', 28)
    a = a.render("ia commence", 5, (0,0,0))
    plateau.blit(a, (732, 160))
    pygame.draw.rect(plateau, (255,128,0), (730, 225, 140, 75))
    a = pygame.font.SysFont('Arial', 40)
    a = a.render("2 joueurs", 5, (0,0,0))
    plateau.blit(a, (733, 236))
    pygame.draw.rect(plateau, (200,200,200), (730, 350, 140, 75))
    a = pygame.font.SysFont('Arial', 50)
    a = a.render("Retour", 5, (0,0,0))
    plateau.blit(a, (738, 356))
    pygame.draw.rect(plateau, (62, 222, 240), (730, 475, 140, 75))
    a = pygame.font.SysFont('Bookman Old Style', 70)
    a = a.render("IA", 5, (0,0,0))
    plateau.blit(a, (765, 470))
    if gagne == 0 :
        pygame.draw.rect(plateau, (250,250,250), (150, 50, 400, 100))
    for i in range(6):
        for j in range(7):
            if g[i][j] == 0 :
                pygame.draw.rect(plateau, (250,250,250), (j * 100, i * 100, 100, 100))
            if g[i][j] == 1 :
                a = pygame.font.SysFont('Arial', 150)
                a = a.render("●", 5, (255,200,0))
                plateau.blit(a, (j * 100 + 6, i * 100 - 45))
            if g[i][j] == 2 :
                a = pygame.font.SysFont('Arial', 150)
                a = a.render("●", 5, (255,0,0))
                plateau.blit(a, (j * 100 + 6, i * 100 - 45))
    pygame.draw.line(plateau, (0,0,150), (1, 1), (1, 600 ), 5)
    pygame.draw.line(plateau, (0,0,150), (1, 1), (698, 1), 5)
    pygame.draw.line(plateau, (0,0,150), (698, 1), (698, 600), 5)
    pygame.draw.line(plateau, (0,0,150), (0, 598), (698, 598), 5)
    for i in range (6) :
        pygame.draw.line(plateau, (0,0,150), ((i + 1) * 100, 0), (( i + 1) * 100, 600), 5)
    for i in range (5) :
        pygame.draw.line(plateau, (0,0,150), (0, (i + 1) * 100), (700, (i + 1) * 100), 5)
    if gagne == 1 :
        pygame.draw.rect(plateau, (250,250,250), (150, 50, 400, 100))
        a = pygame.font.SysFont('Arial', 50)
        a = a.render("Victoire des jaunes !", 5, (0,0,0))
        plateau.blit(a, (162, 75))
    elif gagne == 2 :
        pygame.draw.rect(plateau, (250,250,250), (150, 50, 400, 100))
        a = pygame.font.SysFont('Arial', 50)
        a = a.render("Victoire des rouges !", 5, (0,0,0))
        plateau.blit(a, (162, 75))
    elif gagne == 0 and cases_vides == [0,0,0,0,0,0,0] :
        pygame.draw.rect(plateau, (250,250,250), (250, 50, 200, 100))
        a = pygame.font.SysFont('Arial', 50)
        a = a.render("Match nul", 5, (0,0,0))
        plateau.blit(a, (260, 70))

def coup_aleatoire(possibilite):
    """
    Entrée : Tableau des colonnes jouables
    Sortie : Une colonne aléatoire du tableau
    """
    c = random.choice(possibilite)
    while cases_vides[c] == 0 :
        c = random.choice(possibilite)
    return c

def test_recursif(j,anticipation):
    """
    Sortie : la colonne où il faut jouer
    """
    possibilite = []
    for c in range(7):
        if cases_vides[c] > 0:
            jouer(j,c)

            compteur[0] += 1

            if victoire(j,c,g) == True:
                retire_un_coup(c)
                return [c], True
            elif anticipation > 0:

                resultat, force = test_recursif(change_j(j),anticipation-1)

                if len(resultat) == 0:
                    retire_un_coup(c)
                    return [c], True
                elif len(resultat) > 1 or force == False :
                    possibilite.append(c)
            else:
                possibilite.append(c)
            retire_un_coup(c)
    return possibilite, False

def ia_j(j,exploite,g,anticipation):
    """
    Sortie : la colonne où il faut jouer
    """
    if cases_vides == [6,6,6,6,6,6,6]:
        return 3

    trous = 0
    for i in range(7):
        trous += cases_vides[i]

    global compteur
    compteur = [0]

    possibilite, force = test_recursif(j,anticipation + (42-trous)//7)

    # Empêche de gacher un avantage
    for col in range(7):
        if col in possibilite and len(possibilite) > 1 and cases_vides[col] > 1:
            cases_vides[col] -= 1
            jouer(j,col)
            if victoire(j,col,g) == True:
                possibilite.remove(col)
            retire_un_coup(col)
            cases_vides[col] += 1

    # S'assure de ne pas donner la victoire car l'adversaire peut faire une erreur
    if possibilite == []:
        while anticipation > 0 and possibilite == []:
            anticipation -= 1
            possibilite, force = test_recursif(j,anticipation)
        if anticipation == 0:
            possibilite, force = test_recursif(change_j(j),anticipation)
        elif possibilite == []:
            possibilite = [0,1,2,3,4,5,6,7]

    # Choix final
    if exploite == True:
        possibilite = exploitation(possibilite,j,ia)
    choix = [0,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,5,6]
    c = coup_aleatoire(choix)
    while c not in possibilite:
        c = coup_aleatoire(choix)
    return c


ia = [[],[]]
global montrer
montrer = 0

entrainement_ia(0,0.25,ia,True,False,3)

montrer = 0

puissance_4_pygame(True,True,ia,4)