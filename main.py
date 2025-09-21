import random
import pygame
from os.path import join

# ATTENTION IL FAUT TAPER LA COMMANDE: "pip install pygame-ce" OU INSTALLER LE PACKAGE 'pygame-ce' DIRECTEMENT SI VOTRE IDE LE PERMET, CEST LA VERSION COMMUNAUTAIRE DE PYGAME QUI EST PLUS PERFORMENTE


WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
GRID_SIZE = 10
SHIPS_NBR = 5
ships_list = ["barque", "torpilleur", "sous_marin", "croiseur", "porte_avions"]
ships_size = [1, 2, 3, 4, 5]

#Creation de la classe joueur 1
class Player1:
    def __init__(self, grid):#Permet d'initialiser des valeurs qui sont propres a la classe Player1 et qui prend en argument une grille qui correspond Ã  la grille du joueur
        self.grid = grid
        self.can_shoot = True
        self.ships_sprite = pygame.sprite.Group() #on cree un group de sprite propre a la class afin de pouvoir regrouper des instance de class que l'on a declarer comme sprite ce qui permet de les manipuler plus facilement
        self.boat = Boat(self.ships_sprite) #on appele donc chaque class correspondant aux bateaux du joueur que l'on 'range' dans notre groupe de sprite
        self.torpedo = Torpedo(self.ships_sprite)
        self.submarine = Submarine(self.ships_sprite)
        self.cruiser = Cruiser(self.ships_sprite)
        self.aircraft = Aircraft(self.ships_sprite)

    def set_opponent_settings(self, grid, original_grid, boat, torpedo, submarine, cruiser, aircraft): #permet d'obtenir tt les donner adverse nécessaire, celles ci sont donnees en argument de cette fct
        self.opponent_grid = grid
        self.opponent_grid_original = original_grid
        self.opponent_boat = boat
        self.opponent_torpedo = torpedo
        self.opponent_submarine = submarine
        self.opponent_cruiser = cruiser
        self.opponent_aircraft = aircraft

    def place_ships(self, ship): #permet de verifier si l'on peut placer un bateau(qui est donner en argument) selon sa postion et sont axe dans la grille
        ok = True #le principe est de verifier si tt les case que prendra ce bateau sont bien dans la grille et que les cases en question ne sont pas deja utilisees, on par d'un ok vrai qui reste inchange si il n'y a pas de probleme, par la meme occasion un appelle direct de cette fonction place directement le bateau dans la grille du joueur
        for i in range(GRID_SIZE):
            if ship.pos_y == i:
                for j in range(GRID_SIZE):
                    if ship.pos_x == j:
                        if (ship.direction == 'H') or (ship.direction == 'h'):
                            for k in range(ship.size):
                                if not ((0 <= j + k <= (GRID_SIZE - 1)) and (self.grid[i][j + k] == 0)):
                                    ok = False
                            if ok:
                                for k in range(ship.size):
                                    self.grid[i][j + k] = ship.shape
                            else:
                                return (1)
                        else:
                            for k in range(ship.size):
                                if not ((0 <= i + k <= (GRID_SIZE - 1)) and (self.grid[i + k][j] == 0)):
                                    ok = False
                            if ok:
                                for k in range(ship.size):
                                    self.grid[i + k][j] = ship.shape
                            else:
                                return (1)
        return (0)

    def create_ships(self, ship_nbr, pos): # permet de placer un bateaux (dont l'identiter et la position sont donnees en arguments) sur la grille du joueur a l'aide de la fct place_ships et permet aussi de considerer le l'instance du bateau en question comme 'placé' ce qui permet dans la fct run de pouvoir placer definitivement le bateau sur l'ecran de manier visuelle et 'physique'
        while True:
            b_x = pos[0]
            b_y = pos[1]
            ok = True
            if ok:
                if ok:
                    if ship_nbr == 0:
                        self.boat.pos_y = pos[0]
                        self.boat.pos_x = pos[1]
                        if self.place_ships(self.boat) == 0:
                            self.place_ships(self.boat)
                            self.boat.is_placed = True
                            break
                        else:
                            self.boat.replace()
                            break
                    elif ship_nbr == 1:
                        self.torpedo.pos_y = pos[0]
                        self.torpedo.pos_x = pos[1]
                        if self.place_ships(self.torpedo) == 0:
                            self.place_ships(self.torpedo)
                            self.torpedo.is_placed = True
                            break
                        else:
                            self.torpedo.replace()
                            break
                    elif ship_nbr == 2:
                        self.submarine.pos_y = pos[0]
                        self.submarine.pos_x = pos[1]
                        if self.place_ships(self.submarine) == 0:
                            self.place_ships(self.submarine)
                            self.submarine.is_placed = True
                            break
                        else:
                            self.submarine.replace()
                            break
                    elif ship_nbr == 3:
                        self.cruiser.pos_y = pos[0]
                        self.cruiser.pos_x = pos[1]
                        if self.place_ships(self.cruiser) == 0:
                            self.place_ships(self.cruiser)
                            self.cruiser.is_placed = True
                            break
                        else:
                            self.cruiser.replace()
                            break
                    elif ship_nbr == 4:
                        self.aircraft.pos_y = pos[0]
                        self.aircraft.pos_x = pos[1]
                        if self.place_ships(self.aircraft) == 0:
                            self.place_ships(self.aircraft)
                            self.aircraft.is_placed = True
                            break
                        else:
                            self.aircraft.replace()
                            break
                else:
                    pass

    def shoot(self, pos): #meme principe que dans les version precedente mais les coordoner sont demander en argument
        while True:
            pos_x = pos[1]
            pos_y = pos[0]
            ok = True
            if ok:
                if (0 <= pos_x <= 9):
                    if (self.opponent_grid[pos_y][pos_x] == 0):
                        self.opponent_grid[pos_y][pos_x] = 1
                        self.can_shoot = False
                        break
                    elif ((self.opponent_grid[pos_y][pos_x] == 1) or (self.opponent_grid[pos_y][pos_x] == 2) or (
                            self.opponent_grid[pos_y][pos_x] == 3)):
                        self.can_shoot = True
                        break
                    else:
                        if self.opponent_grid[pos_y][pos_x] == self.opponent_boat.shape:
                            self.opponent_boat.get_damage()
                            if self.opponent_boat.alive == False:
                                for k in range(GRID_SIZE):
                                    for l in range(GRID_SIZE):
                                        if self.opponent_grid_original[k][l] == self.opponent_boat.shape:
                                            self.opponent_grid[k][l] = 3
                                self.can_shoot = True
                                break
                            else:
                                self.opponent_grid[pos_y][pos_x] = 2
                                self.can_shoot = True
                                break
                        elif self.opponent_grid[pos_y][pos_x] == self.opponent_torpedo.shape:
                            self.opponent_torpedo.get_damage()
                            if self.opponent_torpedo.alive == False:
                                for k in range(GRID_SIZE):
                                    for l in range(GRID_SIZE):
                                        if self.opponent_grid_original[k][l] == self.opponent_torpedo.shape:
                                            self.opponent_grid[k][l] = 3
                                self.can_shoot = True
                                break
                            else:
                                self.opponent_grid[pos_y][pos_x] = 2
                                self.can_shoot = True
                                break
                        elif self.opponent_grid[pos_y][pos_x] == self.opponent_submarine.shape:
                            self.opponent_submarine.get_damage()
                            if self.opponent_submarine.alive == False:
                                for k in range(GRID_SIZE):
                                    for l in range(GRID_SIZE):
                                        if self.opponent_grid_original[k][l] == self.opponent_submarine.shape:
                                            self.opponent_grid[k][l] = 3
                                self.can_shoot = True
                                break
                            else:
                                self.opponent_grid[pos_y][pos_x] = 2
                                self.can_shoot = True
                                break
                        elif self.opponent_grid[pos_y][pos_x] == self.opponent_cruiser.shape:
                            self.opponent_cruiser.get_damage()
                            if self.opponent_cruiser.alive == False:
                                for k in range(GRID_SIZE):
                                    for l in range(GRID_SIZE):
                                        if self.opponent_grid_original[k][l] == self.opponent_cruiser.shape:
                                            self.opponent_grid[k][l] = 3
                                self.can_shoot = True
                                break
                            else:
                                self.opponent_grid[pos_y][pos_x] = 2
                                self.can_shoot = True
                                break
                        elif self.opponent_grid[pos_y][pos_x] == self.opponent_aircraft.shape:
                            self.opponent_aircraft.get_damage()
                            if self.opponent_aircraft.alive == False:
                                for k in range(GRID_SIZE):
                                    for l in range(GRID_SIZE):
                                        if self.opponent_grid_original[k][l] == self.opponent_aircraft.shape:
                                            self.opponent_grid[k][l] = 3
                                self.can_shoot = True
                                break
                            else:
                                self.opponent_grid[pos_y][pos_x] = 2
                                self.can_shoot = True
                                break
                else:
                    pass

    def have_win(self):
        nbr_coule = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.opponent_grid[i][j] == 3:
                    nbr_coule += 1
        if nbr_coule == (ships_size[0] + ships_size[1] + ships_size[2] + ships_size[3] + ships_size[4]):
            return (True)
        else:
            return (False)


class Player2_IA: #meme principe que dans les version precedentes, la seul difference est le mode dans la fct shoot et l'ajout d'un temps d'attente entre chaque tire de l'ia
    def __init__(self, grid):
        self.grid = grid
        self.can_shoot = False
        self.cases_shoot = []
        self.touchs = []
        self.cooldown = 775
        self.current_time = 0

    def set_opponent_settings(self, grid, original_grid, boat, torpedo, submarine, cruiser,
                              aircraft):
        self.opponent_grid = grid
        self.opponent_grid_original = original_grid
        self.opponent_boat = boat
        self.opponent_torpedo = torpedo
        self.opponent_submarine = submarine
        self.opponent_cruiser = cruiser
        self.opponent_aircraft = aircraft

    def place_ships(self, ship):
        ok = True
        for i in range(GRID_SIZE):
            if ship.pos_y == i:
                for j in range(GRID_SIZE):
                    if ship.pos_x == j:
                        if ship.direction == 2:
                            for k in range(ship.size):
                                if not (self.grid[i][j + k] == 0):
                                    ok = False
                            if ok:
                                for k in range(ship.size):
                                    self.grid[i][j + k] = ship.shape
                            else:
                                return (1)
                        else:
                            for k in range(ship.size):
                                if not (self.grid[i + k][j] == 0):
                                    ok = False
                            if ok:
                                for k in range(ship.size):
                                    self.grid[i + k][j] = ship.shape
                            else:
                                return (1)
        return (0)

    def create_ships(self, ship_nbr):
        if (ship_nbr == 0):
            axe = random.randint(1, 2)
            if axe == 1:  # vertical
                pos_x = random.randint(0, GRID_SIZE - 1)
                pos_y = random.randint(0, ((GRID_SIZE - 1) - (ships_size[0]) + 1))

            else:
                pos_x = random.randint(0, ((GRID_SIZE - 1) - (ships_size[0]) + 1))
                pos_y = random.randint(0, GRID_SIZE - 1)
            self.boat = Opponent_boat(pos_x, pos_y, axe)
            self.place_ships(self.boat)
        elif (ship_nbr == 1):
            while True:
                axe = random.randint(1, 2)
                if axe == 1:  # vertical
                    pos_x = random.randint(0, GRID_SIZE - 1)
                    pos_y = random.randint(0, ((GRID_SIZE - 1) - (ships_size[1]) + 1))
                else:
                    pos_x = random.randint(0, ((GRID_SIZE - 1) - (ships_size[1]) + 1))
                    pos_y = random.randint(0, GRID_SIZE - 1)
                self.torpedo = Opponent_torpedo(pos_x, pos_y, axe)
                if self.place_ships(self.torpedo) == 0:
                    self.place_ships(self.torpedo)
                    break
        elif (ship_nbr == 2):
            while True:
                axe = random.randint(1, 2)
                if axe == 1:  # vertical
                    pos_x = random.randint(0, GRID_SIZE - 1)
                    pos_y = random.randint(0, ((GRID_SIZE - 1) - (ships_size[2]) + 1))
                else:
                    pos_x = random.randint(0, ((GRID_SIZE - 1) - (ships_size[2]) + 1))
                    pos_y = random.randint(0, GRID_SIZE - 1)
                self.submarine = Opponent_submarine(pos_x, pos_y, axe)
                if self.place_ships(self.submarine) == 0:
                    self.place_ships(self.submarine)
                    break
        elif (ship_nbr == 3):
            while True:
                axe = random.randint(1, 2)
                if axe == 1:  # vertical
                    pos_x = random.randint(0, GRID_SIZE - 1)
                    pos_y = random.randint(0, ((GRID_SIZE - 1) - (ships_size[3]) + 1))
                else:  # horizontal
                    pos_x = random.randint(0, ((GRID_SIZE - 1) - (ships_size[3]) + 1))
                    pos_y = random.randint(0, GRID_SIZE - 1)
                self.cruiser = Opponent_cruiser(pos_x, pos_y, axe)
                if self.place_ships(self.cruiser) == 0:
                    self.place_ships(self.cruiser)
                    break
        elif (ship_nbr == 4):
            while True:
                axe = random.randint(1, 2)
                if axe == 1:  # vertical
                    pos_x = random.randint(0, GRID_SIZE - 1)
                    pos_y = random.randint(0, ((GRID_SIZE - 1) - (ships_size[4]) + 1))
                else:
                    pos_x = random.randint(0, ((GRID_SIZE - 1) - (ships_size[4]) + 1))
                    pos_y = random.randint(0, GRID_SIZE - 1)
                self.aircraft = Opponent_aircraft(pos_x, pos_y, axe)
                if self.place_ships(self.aircraft) == 0:
                    self.place_ships(self.aircraft)
                    break

    def shoot_cooldown(self): # gere le temps d'attente entre les tire, return vrai si l'ia peut a nouveau tirer(d'un point de vue du temps uniquement)
        if self.current_time == 0: #cas initiale de la parti, lorsque l'ia n'a encore jamais tiré
            return (True)
        elif pygame.time.get_ticks() - self.current_time < self.cooldown: #  pygame.time.get_ticks() donne le temps actuelle du jeu et self.current_time donne le temps du jeu lorsque l'ia a effectué sont dernier tire, la difference des deux donne donc le temps ecoulé depuis le dernier tire de l'ia, ainsi on le compar au cooldown qu'on a fixé et si ce temps et superier ou egale au cooldown on return true
            return (False)
        else:
            return (True)

    def shoot(self, mode):
        while True:
            L = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0],
                 [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1],
                 [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2],
                 [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3],
                 [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4],
                 [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5],
                 [0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6], [8, 6], [9, 6],
                 [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7], [8, 7], [9, 7],
                 [0, 8], [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8],
                 [0, 9], [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9]]
            can_shoot = [vect for vect in L if vect not in self.cases_shoot]
            potential_target = []
            boats_cases = []
            torpedo_cases = []
            submarine_cases = []
            cruiser_cases = []
            aircraft_cases = []
            for vect in self.touchs:
                if vect[2] == self.opponent_boat.shape:
                    boats_cases.append(vect)
                elif vect[2] == self.opponent_torpedo.shape:
                    torpedo_cases.append(vect)
                elif vect[2] == self.opponent_submarine.shape:
                    submarine_cases.append(vect)
                elif vect[2] == self.opponent_cruiser.shape:
                    cruiser_cases.append(vect)
                elif vect[2] == self.opponent_aircraft.shape:
                    aircraft_cases.append(vect)
            if boats_cases:
                if (len(boats_cases) == 1):
                    if ((boats_cases[0][0] + 1 <= 9) and ([boats_cases[0][0] + 1, boats_cases[0][1]] != vect for vect in
                                                          self.cases_shoot)):
                        potential_target.append(boats_cases[0])
                    if ((boats_cases[0][0] - 1 >= 0) and ([boats_cases[0][0] - 1, boats_cases[0][1]] != vect for vect in
                                                          self.cases_shoot)):
                        potential_target.append(boats_cases[0])
                    if ((boats_cases[0][1] + 1 <= 9) and ([boats_cases[0][0], boats_cases[0][1] + 1] != vect for vect in
                                                          self.cases_shoot)):
                        potential_target.append(boats_cases[0])
                    if ((boats_cases[0][1] - 1 >= 0) and ([boats_cases[0][0], boats_cases[0][1] - 1] != vect for vect in
                                                          self.cases_shoot)):
                        potential_target.append(boats_cases[0])
                else:  # cela veut dire que l'ia a toucher au moins deux fois un la barque, on peut donc lui donner l'information de la direction de celle ci
                    if ((self.opponent_boat.direction == 'H') or (self.opponent_boat.direction == 'h')):
                        for vect in boats_cases:
                            if ((vect[0] + 1 <= 9) and ([vect[0] + 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append(vect)
                            if ((vect[0] - 1 >= 0) and ([vect[0] - 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append(vect)
                    else:
                        for vect in boats_cases:
                            if ((vect[1] + 1 <= 9) and ([vect[0], vect[1] + 1] != vects for vects in self.cases_shoot)):
                                potential_target.append(vect)
                            if ((vect[1] - 1 >= 0) and ([vect[0], vect[1] - 1] != vects for vects in self.cases_shoot)):
                                potential_target.append(vect)
            if torpedo_cases:
                if (len(torpedo_cases) == 1):
                    if ((torpedo_cases[0][0] + 1 <= 9) and ([torpedo_cases[0][0] + 1, torpedo_cases[0][1]] != vect for
                                                            vect in self.cases_shoot)):
                        potential_target.append([torpedo_cases[0][0] + 1, torpedo_cases[0][1]])
                    if ((torpedo_cases[0][0] - 1 >= 0) and ([torpedo_cases[0][0] - 1, torpedo_cases[0][1]] != vect for
                                                            vect in self.cases_shoot)):
                        potential_target.append([torpedo_cases[0][0] - 1, torpedo_cases[0][1]])
                    if ((torpedo_cases[0][1] + 1 <= 9) and ([torpedo_cases[0][0], torpedo_cases[0][1] + 1] != vect for
                                                            vect in self.cases_shoot)):
                        potential_target.append([torpedo_cases[0][0], torpedo_cases[0][1] + 1])
                    if ((torpedo_cases[0][1] - 1 >= 0) and ([torpedo_cases[0][0], torpedo_cases[0][1] - 1] != vect for
                                                            vect in self.cases_shoot)):
                        potential_target.append([torpedo_cases[0][0], torpedo_cases[0][1] - 1])
                else:  # cela veut dire que l'ia a toucher au moins deux fois, on peut donc lui donner l'information de la direction de celle ci
                    if ((self.opponent_torpedo.direction == 'H') or (self.opponent_torpedo.direction == 'h')):
                        for vect in torpedo_cases:
                            if ((vect[0] + 1 <= 9) and ([vect[0] + 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0] + 1, vect[1]])
                            if ((vect[0] - 1 >= 0) and ([vect[0] - 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0] - 1, vect[1]])
                    else:
                        for vect in torpedo_cases:
                            if ((vect[1] + 1 <= 9) and ([vect[0], vect[1] + 1] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0], vect[1] + 1])
                            if ((vect[1] - 1 >= 0) and ([vect[0], vect[1] - 1] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0], vect[1] - 1])
            if submarine_cases:
                if (len(submarine_cases) == 1):
                    if ((submarine_cases[0][0] + 1 <= 9) and ([submarine_cases[0][0] + 1, submarine_cases[0][1]] != vect
                                                              for vect in self.cases_shoot)):
                        potential_target.append([submarine_cases[0][0] + 1, submarine_cases[0][1]])
                    if ((submarine_cases[0][0] - 1 >= 0) and ([submarine_cases[0][0] - 1, submarine_cases[0][1]] != vect
                                                              for vect in self.cases_shoot)):
                        potential_target.append([submarine_cases[0][0] - 1, submarine_cases[0][1]])
                    if ((submarine_cases[0][1] + 1 <= 9) and ([submarine_cases[0][0], submarine_cases[0][1] + 1] != vect
                                                              for vect in self.cases_shoot)):
                        potential_target.append([submarine_cases[0][0], submarine_cases[0][1] + 1])
                    if ((submarine_cases[0][1] - 1 >= 0) and ([submarine_cases[0][0], submarine_cases[0][1] - 1] != vect
                                                              for vect in self.cases_shoot)):
                        potential_target.append([submarine_cases[0][0], submarine_cases[0][1] - 1])
                else:  # cela veut dire que l'ia a toucher au moins deux fois un la barque, on peut donc lui donner l'information de la direction de celle ci
                    if ((self.opponent_submarine.direction == 'H') or (self.opponent_submarine.direction == 'h')):
                        for vect in submarine_cases:
                            if ((vect[0] + 1 <= 9) and ([vect[0] + 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0] + 1, vect[1]])
                            if ((vect[0] - 1 >= 0) and ([vect[0] - 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0] - 1, vect[1]])
                    else:
                        for vect in submarine_cases:
                            if ((vect[1] + 1 <= 9) and ([vect[0], vect[1] + 1] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0], vect[1] + 1])
                            if ((vect[1] - 1 >= 0) and ([vect[0], vect[1] - 1] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0], vect[1] - 1])
            if cruiser_cases:
                if (len(cruiser_cases) == 1):
                    if ((cruiser_cases[0][0] + 1 <= 9) and ([cruiser_cases[0][0] + 1, cruiser_cases[0][1]] != vect for
                                                            vect in self.cases_shoot)):
                        potential_target.append([cruiser_cases[0][0] + 1, cruiser_cases[0][1]])
                    if ((cruiser_cases[0][0] - 1 >= 0) and ([cruiser_cases[0][0] - 1, cruiser_cases[0][1]] != vect for
                                                            vect in self.cases_shoot)):
                        potential_target.append([cruiser_cases[0][0] - 1, cruiser_cases[0][1]])
                    if ((cruiser_cases[0][1] + 1 <= 9) and ([cruiser_cases[0][0], cruiser_cases[0][1] + 1] != vect for
                                                            vect in self.cases_shoot)):
                        potential_target.append([cruiser_cases[0][0], cruiser_cases[0][1] + 1])
                    if ((cruiser_cases[0][1] - 1 >= 0) and ([cruiser_cases[0][0], cruiser_cases[0][1] - 1] != vect for
                                                            vect in self.cases_shoot)):
                        potential_target.append([cruiser_cases[0][0], cruiser_cases[0][1] - 1])
                else:  # cela veut dire que l'ia a toucher au moins deux fois un la barque, on peut donc lui donner l'information de la direction de celle ci
                    if ((self.opponent_cruiser.direction == 'H') or (self.opponent_cruiser.direction == 'h')):
                        for vect in cruiser_cases:
                            if ((vect[0] + 1 <= 9) and ([vect[0] + 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0] + 1, vect[1]])
                            if ((vect[0] - 1 >= 0) and ([vect[0] - 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0] - 1, vect[1]])
                    else:
                        for vect in cruiser_cases:
                            if ((vect[1] + 1 <= 9) and ([vect[0], vect[1] + 1] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0], vect[1] + 1])
                            if ((vect[1] - 1 >= 0) and ([vect[0], vect[1] - 1] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0], vect[1] - 1])
            if aircraft_cases:
                if (len(aircraft_cases) == 1):
                    if ((aircraft_cases[0][0] + 1 <= 9) and ([aircraft_cases[0][0] + 1, aircraft_cases[0][1]] != vect
                                                             for vect in self.cases_shoot)):
                        potential_target.append([aircraft_cases[0][0] + 1, aircraft_cases[0][1]])
                    if ((aircraft_cases[0][0] - 1 >= 0) and ([aircraft_cases[0][0] - 1, aircraft_cases[0][1]] != vect
                                                             for vect in self.cases_shoot)):
                        potential_target.append([aircraft_cases[0][0] - 1, aircraft_cases[0][1]])
                    if ((aircraft_cases[0][1] + 1 <= 9) and ([aircraft_cases[0][0], aircraft_cases[0][1] + 1] != vect
                                                             for vect in self.cases_shoot)):
                        potential_target.append([aircraft_cases[0][0], aircraft_cases[0][1] + 1])
                    if ((aircraft_cases[0][1] - 1 >= 0) and ([aircraft_cases[0][0], aircraft_cases[0][1] - 1] != vect
                                                             for vect in self.cases_shoot)):
                        potential_target.append([aircraft_cases[0][0], aircraft_cases[0][1] - 1])
                else:  # cela veut dire que l'ia a toucher au moins deux fois un la barque, on peut donc lui donner l'information de la direction de celle ci
                    if ((self.opponent_aircraft.direction == 'H') or (self.opponent_aircraft.direction == 'h')):
                        for vect in aircraft_cases:
                            if ((vect[0] + 1 <= 9) and ([vect[0] + 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0] + 1, vect[1]])
                            if ((vect[0] - 1 >= 0) and ([vect[0] - 1, vect[1]] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0] - 1, vect[1]])
                    else:
                        for vect in aircraft_cases:
                            if ((vect[1] + 1 <= 9) and ([vect[0], vect[1] + 1] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0], vect[1] + 1])
                            if ((vect[1] - 1 >= 0) and ([vect[0], vect[1] - 1] != vects for vects in self.cases_shoot)):
                                potential_target.append([vect[0], vect[1] - 1])
            if mode == 'simple': #dans ce cas on prend une case non 'tiré' au hasard comme dans la v2
                pos_vect = random.choice(can_shoot)
            elif mode == 'hard': #dans ce cas on prend d'abord si possible une case dans potential_target comme dans la v3
                if potential_target:
                    pos_vect = random.choice(potential_target)
                else:
                    pos_vect = random.choice(can_shoot)
            self.cases_shoot.append(pos_vect)
            pos_x = pos_vect[0]
            pos_y = pos_vect[1]
            if (self.opponent_grid[pos_y][pos_x] == 0):
                self.opponent_grid[pos_y][pos_x] = 1
                self.can_shoot = False
                break
            else:
                if self.opponent_grid[pos_y][pos_x] == self.opponent_boat.shape:
                    self.opponent_boat.get_damage()
                    if self.opponent_boat.alive == False:
                        for k in range(GRID_SIZE):
                            for l in range(GRID_SIZE):
                                if self.opponent_grid_original[k][l] == self.opponent_boat.shape:
                                    self.opponent_grid[k][l] = 3
                        self.touchs = [vect for vect in self.touchs if vect[
                            2] != self.opponent_boat.shape]  # permet de garder seulement les bateau toucher et non couler dans slef.touchs
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                    else:
                        self.opponent_grid[pos_y][pos_x] = 2
                        pos_vect.append(self.opponent_boat.shape)
                        self.touchs.append(pos_vect)
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                elif self.opponent_grid[pos_y][pos_x] == self.opponent_torpedo.shape:
                    self.opponent_torpedo.get_damage()
                    if self.opponent_torpedo.alive == False:
                        for k in range(GRID_SIZE):
                            for l in range(GRID_SIZE):
                                if self.opponent_grid_original[k][l] == self.opponent_torpedo.shape:
                                    self.opponent_grid[k][l] = 3
                        self.touchs = [vect for vect in self.touchs if vect[2] != self.opponent_torpedo.shape]
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                    else:
                        self.opponent_grid[pos_y][pos_x] = 2
                        pos_vect.append(self.opponent_torpedo.shape)
                        self.touchs.append(pos_vect)
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                elif self.opponent_grid[pos_y][pos_x] == self.opponent_submarine.shape:
                    self.opponent_submarine.get_damage()
                    if self.opponent_submarine.alive == False:
                        for k in range(GRID_SIZE):
                            for l in range(GRID_SIZE):
                                if self.opponent_grid_original[k][l] == self.opponent_submarine.shape:
                                    self.opponent_grid[k][l] = 3
                        self.touchs = [vect for vect in self.touchs if vect[2] != self.opponent_submarine.shape]
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                    else:
                        self.opponent_grid[pos_y][pos_x] = 2
                        pos_vect.append(self.opponent_submarine.shape)
                        self.touchs.append(pos_vect)
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                elif self.opponent_grid[pos_y][pos_x] == self.opponent_cruiser.shape:
                    self.opponent_cruiser.get_damage()
                    if self.opponent_cruiser.alive == False:
                        for k in range(GRID_SIZE):
                            for l in range(GRID_SIZE):
                                if self.opponent_grid_original[k][l] == self.opponent_cruiser.shape:
                                    self.opponent_grid[k][l] = 3
                        self.touchs = [vect for vect in self.touchs if vect[2] != self.opponent_cruiser.shape]
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                    else:
                        self.opponent_grid[pos_y][pos_x] = 2
                        pos_vect.append(self.opponent_cruiser.shape)
                        self.touchs.append(pos_vect)
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                elif self.opponent_grid[pos_y][pos_x] == self.opponent_aircraft.shape:
                    self.opponent_aircraft.get_damage()
                    if self.opponent_aircraft.alive == False:
                        for k in range(GRID_SIZE):
                            for l in range(GRID_SIZE):
                                if self.opponent_grid_original[k][l] == self.opponent_aircraft.shape:
                                    self.opponent_grid[k][l] = 3
                        self.touchs = [vect for vect in self.touchs if vect[2] != self.opponent_aircraft.shape]
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break
                    else:
                        self.opponent_grid[pos_y][pos_x] = 2
                        pos_vect.append(self.opponent_aircraft.shape)
                        self.touchs.append(pos_vect)
                        self.can_shoot = True
                        self.current_time = pygame.time.get_ticks()
                        break

    def have_win(self):
        nbr_coule = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.opponent_grid[i][j] == 3:
                    nbr_coule += 1
        if nbr_coule == (ships_size[0] + ships_size[1] + ships_size[2] + ships_size[3] + ships_size[4]):
            return (True)
        else:
            return (False)


class Boat(pygame.sprite.Sprite): #cette fois ci on conssidere les class des bateau du joueur comme des sprites, cela permet une manipulation plus simple des instances de ces class
    def __init__(self, groups): #on initalise tt les proprietees du bateau et on 'range' l'instance dans un groupe de sprite donné en argument
        super().__init__(groups)
        self.initial_pos = (4 * 1 / 36 * WINDOW_WIDTH, WINDOW_HEIGHT - 3 * 1 / 36 * WINDOW_WIDTH) #on affiche les bateau en bas de la grille, ce qui correspond a ces coordonnees
        self.direction = 'h'
        self.size = 1
        self.shape = 'B'
        self.touch = 0
        self.alive = True
        self.image = pygame.transform.scale(pygame.image.load(join('image', 'boat1.png')),
                                            (self.size / 36 * WINDOW_WIDTH, 1 / 36 * WINDOW_WIDTH))
        self.horizontal_image = self.image #image horizontale
        self.vertical_image = pygame.transform.rotate(self.image, -90) #image verticale qui correspond a l'originale tourner a -90 degres
        self.current_image = self.image #image qui sera afficher a l'ecran
        self.initial_rect = self.image.get_frect(topleft=self.initial_pos) #surface physique initial(correspond a celle lorsque le bateau est encore en bas de la grille)
        self.horizontal = True #initialisation basique de parametres
        self.is_clicked = False
        self.rect = self.initial_rect
        self.is_placed = False

    def place_ship(self, pos_x, pos_y): #demande les coodronees de la grille ou l'on veut mettre notre bateau et permet de positioner directement corner en haut a gauche de notre bateau a l'endroi en haut a gauche de la case dont les coordoner dans la grille sont celle que l'on a demandé (ce placement permet de placer le bateau peut importe sont axe(ceci grace aux fct rotate et update_pos qui change directement le rect du bateau selon sont axe))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.topleft = (int(((pos_x + 4) / 36) * WINDOW_WIDTH),
                             int((pos_y / 36) * WINDOW_WIDTH + (WINDOW_HEIGHT - ((10 / 36) * WINDOW_WIDTH)) / 2))
        self.is_placed = True

    def replace(self): #replace le bateau a sa position d'origine et de le considerer a nouveau comme 'non place', c'est a dire en dessou de la grille et horizontalement
        self.current_image = self.horizontal_image
        self.rect = self.initial_rect
        self.is_placed = False
        self.horizontal = True

    def click_collision(self, click_pos): # permet de verifier si le joueur a clicke sur le bateau, change self.is_clicked en consequence
        if self.initial_rect.collidepoint(click_pos):
            self.is_clicked = True
        else:
            self.is_clicked = False

    def update_pos(self, pos, display_surface): #et utiliser lorsque le joueur reste appuiller sur le bateau et souhaite le deplacer, l'argument pos correspont a la position de la sourie et display_surface est la surface sur laquelle ou dessine notre bateau
        if self.horizontal:
            self.direction = 'h'
            self.current_image = self.horizontal_image
            self.rect = self.current_image.get_frect(midleft=(pos[0] - 1 / 2 * 1 / 36 * WINDOW_WIDTH, pos[1]))
        else:
            self.direction = 'v'
            self.current_image = self.vertical_image
            self.rect = self.current_image.get_frect(midtop=(pos[0], pos[1] - 1 / 2 * 1 / 36 * WINDOW_WIDTH))
        display_surface.blit(self.current_image, self.rect)

    def display(self, display_surface): #affiche simplement le bateau sur la surface demander en argument
        display_surface.blit(self.current_image, self.rect)

    def rotate(self): #change l'axe du bateau, permet dans update_pos de pouvoir changer l'image et la surface 'physique' du bateau en consequence
        if self.horizontal:
            self.horizontal = False
        else:
            self.horizontal = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Torpedo(pygame.sprite.Sprite): #meme principe que pour la barque
    def __init__(self, groups):
        super().__init__(groups)
        self.initial_pos = (6 * 1 / 36 * WINDOW_WIDTH, WINDOW_HEIGHT - 3 * 1 / 36 * WINDOW_WIDTH)
        self.direction = 'h'
        self.size = 2
        self.shape = 'T'
        self.touch = 0
        self.alive = True
        self.image = pygame.transform.scale(pygame.image.load(join('image', 'boat1.png')),
                                            (self.size / 36 * WINDOW_WIDTH, 1 / 36 * WINDOW_WIDTH))
        self.horizontal_image = self.image
        self.vertical_image = pygame.transform.rotate(self.image, -90)
        self.current_image = self.image
        self.initial_rect = self.image.get_frect(topleft=self.initial_pos)
        self.horizontal = True
        self.is_clicked = False
        self.rect = self.initial_rect
        self.is_placed = False

    def place_ship(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.topleft = (int(((pos_x + 4) / 36) * WINDOW_WIDTH),
                             int((pos_y / 36) * WINDOW_WIDTH + (WINDOW_HEIGHT - ((10 / 36) * WINDOW_WIDTH)) / 2))
        self.is_placed = True

    def replace(self):
        self.current_image = self.horizontal_image
        self.rect = self.initial_rect
        self.is_placed = False
        self.horizontal = True

    def click_collision(self, click_pos):
        if self.initial_rect.collidepoint(click_pos):
            self.is_clicked = True
        else:
            self.is_clicked = False

    def update_pos(self, pos, display_surface):
        if self.horizontal:
            self.direction = 'h'
            self.current_image = self.horizontal_image
            self.rect = self.current_image.get_frect(midleft=(pos[0] - 1 / 2 * 1 / 36 * WINDOW_WIDTH, pos[1]))
        else:
            self.direction = 'v'
            self.current_image = self.vertical_image
            self.rect = self.current_image.get_frect(midtop=(pos[0], pos[1] - 1 / 2 * 1 / 36 * WINDOW_WIDTH))
        display_surface.blit(self.current_image, self.rect)

    def display(self, display_surface):
        display_surface.blit(self.current_image, self.rect)

    def rotate(self):
        if self.horizontal:
            self.horizontal = False
        else:
            self.horizontal = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Submarine(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.initial_pos = (9 * 1 / 36 * WINDOW_WIDTH, WINDOW_HEIGHT - 3 * 1 / 36 * WINDOW_WIDTH)
        self.direction = 'h'
        self.size = 3
        self.shape = 'S'
        self.touch = 0
        self.alive = True
        self.image = pygame.transform.scale(pygame.image.load(join('image', 'boat1.png')),
                                            (self.size / 36 * WINDOW_WIDTH, 1 / 36 * WINDOW_WIDTH))
        self.horizontal_image = self.image
        self.vertical_image = pygame.transform.rotate(self.image, -90)
        self.current_image = self.image
        self.initial_rect = self.image.get_frect(topleft=self.initial_pos)
        self.horizontal = True
        self.is_clicked = False
        self.rect = self.initial_rect
        self.is_placed = False

    def place_ship(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.topleft = (int(((pos_x + 4) / 36) * WINDOW_WIDTH),
                             int((pos_y / 36) * WINDOW_WIDTH + (WINDOW_HEIGHT - ((10 / 36) * WINDOW_WIDTH)) / 2))
        self.is_placed = True

    def replace(self):
        self.current_image = self.horizontal_image
        self.rect = self.initial_rect
        self.is_placed = False
        self.horizontal = True

    def click_collision(self, click_pos):
        if self.initial_rect.collidepoint(click_pos):
            self.is_clicked = True
        else:
            self.is_clicked = False

    def update_pos(self, pos, display_surface):
        if self.horizontal:
            self.direction = 'h'
            self.current_image = self.horizontal_image
            self.rect = self.current_image.get_frect(midleft=(pos[0] - 1 / 2 * 1 / 36 * WINDOW_WIDTH, pos[1]))
        else:
            self.direction = 'v'
            self.current_image = self.vertical_image
            self.rect = self.current_image.get_frect(midtop=(pos[0], pos[1] - 1 / 2 * 1 / 36 * WINDOW_WIDTH))
        display_surface.blit(self.current_image, self.rect)

    def display(self, display_surface):
        display_surface.blit(self.current_image, self.rect)

    def rotate(self):
        if self.horizontal:
            self.horizontal = False
        else:
            self.horizontal = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Cruiser(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.initial_pos = (13 * 1 / 36 * WINDOW_WIDTH, WINDOW_HEIGHT - 3 * 1 / 36 * WINDOW_WIDTH)
        self.direction = 'h'
        self.size = 4
        self.shape = 'C'
        self.touch = 0
        self.alive = True
        self.image = pygame.transform.scale(pygame.image.load(join('image', 'boat1.png')),
                                            (self.size / 36 * WINDOW_WIDTH, 1 / 36 * WINDOW_WIDTH))
        self.horizontal_image = self.image
        self.vertical_image = pygame.transform.rotate(self.image, -90)
        self.current_image = self.image
        self.initial_rect = self.image.get_frect(topleft=self.initial_pos)
        self.horizontal = True
        self.is_clicked = False
        self.rect = self.initial_rect
        self.is_placed = False

    def place_ship(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.topleft = (int(((pos_x + 4) / 36) * WINDOW_WIDTH),
                             int((pos_y / 36) * WINDOW_WIDTH + (WINDOW_HEIGHT - ((10 / 36) * WINDOW_WIDTH)) / 2))
        self.is_placed = True

    def replace(self):
        self.current_image = self.horizontal_image
        self.rect = self.initial_rect
        self.is_placed = False
        self.horizontal = True

    def click_collision(self, click_pos):
        if self.initial_rect.collidepoint(click_pos):
            self.is_clicked = True
        else:
            self.is_clicked = False

    def update_pos(self, pos, display_surface):
        if self.horizontal:
            self.direction = 'h'
            self.current_image = self.horizontal_image
            self.rect = self.current_image.get_frect(midleft=(pos[0] - 1 / 2 * 1 / 36 * WINDOW_WIDTH, pos[1]))
        else:
            self.direction = 'v'
            self.current_image = self.vertical_image
            self.rect = self.current_image.get_frect(midtop=(pos[0], pos[1] - 1 / 2 * 1 / 36 * WINDOW_WIDTH))
        display_surface.blit(self.current_image, self.rect)

    def display(self, display_surface):
        display_surface.blit(self.current_image, self.rect)

    def rotate(self):
        if self.horizontal:
            self.horizontal = False
        else:
            self.horizontal = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Aircraft(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.initial_pos = (18 * 1 / 36 * WINDOW_WIDTH, WINDOW_HEIGHT - 3 * 1 / 36 * WINDOW_WIDTH)
        self.direction = 'h'
        self.size = 5
        self.shape = 'A'
        self.touch = 0
        self.alive = True
        self.image = pygame.transform.scale(pygame.image.load(join('image', 'boat1.png')),
                                            (self.size / 36 * WINDOW_WIDTH, 1 / 36 * WINDOW_WIDTH))
        self.horizontal_image = self.image
        self.vertical_image = pygame.transform.rotate(self.image, -90)
        self.current_image = self.image
        self.initial_rect = self.image.get_frect(topleft=self.initial_pos)
        self.horizontal = True
        self.is_clicked = False
        self.rect = self.initial_rect
        self.is_placed = False

    def place_ship(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.topleft = (int(((pos_x + 4) / 36) * WINDOW_WIDTH),
                             int((pos_y / 36) * WINDOW_WIDTH + (WINDOW_HEIGHT - ((10 / 36) * WINDOW_WIDTH)) / 2))
        self.is_placed = True

    def replace(self):
        self.current_image = self.horizontal_image
        self.rect = self.initial_rect
        self.is_placed = False
        self.horizontal = True

    def click_collision(self, click_pos):
        if self.initial_rect.collidepoint(click_pos):
            self.is_clicked = True
        else:
            self.is_clicked = False

    def update_pos(self, pos, display_surface):
        if self.horizontal:
            self.direction = 'h'
            self.current_image = self.horizontal_image
            self.rect = self.current_image.get_frect(midleft=(pos[0] - 1 / 2 * 1 / 36 * WINDOW_WIDTH, pos[1]))
        else:
            self.direction = 'v'
            self.current_image = self.vertical_image
            self.rect = self.current_image.get_frect(midtop=(pos[0], pos[1] - 1 / 2 * 1 / 36 * WINDOW_WIDTH))
        display_surface.blit(self.current_image, self.rect)

    def display(self, display_surface):
        display_surface.blit(self.current_image, self.rect)

    def rotate(self):
        if self.horizontal:
            self.horizontal = False
        else:
            self.horizontal = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Opponent_boat: #meme principe que dans les anciennes versions
    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = 1
        self.direction = direction
        self.shape = 'B'
        self.touch = 0
        self.alive = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Opponent_torpedo:
    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = 2
        self.direction = direction
        self.shape = 'T'
        self.touch = 0
        self.alive = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Opponent_submarine:
    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = 3
        self.direction = direction
        self.shape = 'S'
        self.touch = 0
        self.alive = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Opponent_cruiser:
    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = 4
        self.direction = direction
        self.shape = 'C'
        self.touch = 0
        self.alive = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Opponent_aircraft:
    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = 5
        self.direction = direction
        self.shape = 'A'
        self.touch = 0
        self.alive = True

    def get_damage(self):
        self.touch += 1
        if (self.size - self.touch == 0):
            self.alive = False


class Case(pygame.sprite.Sprite): #class de sprite(option offert par pygame permettant de considerer une class comme un sprite, cela fascilite la manipulation des instance de cette class), cette class gere l'aspect graphique et physique des cases du joueur
    def __init__(self, pos, player_grid, groups): # la fct qui initialse les proproetees de la class et prend en parametre: pos qui correspond a la position dans la grille où l'on veut cette case, player_grid qui sera la grille du joueur et qui permettra de regarder l'etat de la grille afin de pouvoir s'adapter a celle ci et groups correspond au groupes de sprites dans lesquelles on veut mettre notre instance(permet de regrouper des instance de classe entre elle et donc de pouvoir par la suite y acceder plus facilement)
        super().__init__(groups)
        self.pos = pos
        self.surf = pygame.Surface((int((1 / 36) * WINDOW_WIDTH), int((1 / 36) * WINDOW_WIDTH)), pygame.SRCALPHA) #apres des recherches on a descidé de couper la largeur de notre fenetre en 36 et chaque case fait 1/36eme par 1/36eme de cette largeur
        self.rect = self.surf.get_frect(topleft=(int(((self.pos[1] + 4) / 36) * WINDOW_WIDTH),
                                                 int((self.pos[0] / 36) * WINDOW_WIDTH + (
                                                         WINDOW_HEIGHT - ((10 / 36) * WINDOW_WIDTH)) / 2))) #on place les cases en fonction de notre descision precedente et pour la hauteur on commence a: la hauteur - la taille d'un coté de notre grille(qui est carre) ce qui nous donne l'espace restant en heuteur si on fait une grille respectant les conditions abordees au dessu et on divise cette espace restant par 2 afin d'avoir la moitier de cette espace au debut(donc du haut de la fenetre jusque aux cases les plus haute de la grille) puis l'espace restant sera forcement l'autre moitié qui sera a la fin(donc entre les cases les plus basse et le bas de notre fenetre
        self.is_green = False #initialisation qui permet de revenir au cas de base si rien ne se passe
        self.is_clicked = False
        self.player_grid = player_grid

    def curser_collision(self, mouse_pos): #permet de regarder si la position de la souri est sur notre case, dans ce cas self.is_green = True ce qui permet dans display() de colorier la case en vert pour quel le joueur comprene bien qu'il est sur cette case
        if self.rect.collidepoint(mouse_pos):
            self.is_green = True
        else:
            self.is_green = False

    def click_collision(self, click_pos): #meme principe que curser collision mais dans le cas ou le joueur a clicker sur la case
        if self.rect.collidepoint(click_pos):
            self.is_clicked = True
        else:
            self.is_clicked = False

    def display(self): #modifie le rendu visuelle en fonction de ce qui ce passe sur les cases
        if self.is_green:
            self.surf.fill((100, 200, 100))
        elif self.player_grid[self.pos[0]][self.pos[1]] == 0: #si la case correspond a 0 dans la grille du joueur alors on colorie en bleu pour montrer au joueur que ce n'est pas une case deja 'tire'
            self.surf.fill((40, 130, 210))
        elif self.player_grid[self.pos[0]][self.pos[1]] == 1: #de meme mais si c'est une case 'rate'
            self.surf.fill((173, 216, 230))
        elif self.player_grid[self.pos[0]][self.pos[1]] == 2: # 'touche'
            self.surf.fill((255, 99, 71))
        elif self.player_grid[self.pos[0]][self.pos[1]] == 3: # 'coule'
            self.surf.fill((105, 105, 105))
        else:
            self.surf.fill((100, 200, 100)) # cela correspond au cas ou l'on a un bateau non 'tire' par l'ennemie dessu(on colorie alors en vert)

    def update(self, display_surface, font, mouse_pos, click_pos): # fct globale de Case permet d'afficher les lignes entre les cases aisi que les lettre et chiffre des coordonnee et execute tt les fct precedente en utilisent en parametre les parametre nessecaire a ces fct(c'est donc la seul fct appelé dans le code pour cette class)
        self.curser_collision(mouse_pos=mouse_pos)
        self.click_collision(click_pos=click_pos)
        self.display()
        display_surface.blit(self.surf, self.rect)
        pygame.draw.line(display_surface, (220, 220, 220, 128), self.rect.topleft, self.rect.topright, 5)
        pygame.draw.line(display_surface, (220, 220, 220, 128), self.rect.topleft, self.rect.bottomleft, 5)
        pygame.draw.line(display_surface, (220, 220, 220, 128), self.rect.bottomleft, self.rect.bottomright, 5)
        pygame.draw.line(display_surface, (220, 220, 220, 128), self.rect.bottomright, self.rect.topright, 5)
        if self.pos[0] == 0: #si la case est tt en haut donc sur la premiere ligne alors il faut qu'il y est un chiffre au dessu de celle ci, pour definir ce chiffre on regarde dans quelle colonne est cette case et on ajoute 1(on est comme tjr entre 0 et 9 la où on affiche des chiffres entre 1 et 10
            index_surf = font.render(str(self.pos[1] + 1), True, (50, 50, 50)) #utilise la police de caractere font qui est donne en parametre de cette fct pour cree une surface ou ecrire le chiifre correspondant a: str(self.pos[1] + 1)
            index_surf = pygame.transform.scale(index_surf, (1 / 36 * WINDOW_WIDTH - 10, 1 / 36 * WINDOW_WIDTH)) #on redimentionne cette surface
            index_rect = index_surf.get_frect(midbottom=(self.rect.midtop[0], self.rect.midtop[1] - 5)) #on lui attrubue une surface 'physique'
            display_surface.blit(index_surf, index_rect) #on afffiche a l'ecran
        if self.pos[1] == 0: #meme principe mais pour les case tt a gauche ou il faut une lettre(on regarde si la case et en premier collone et ensuite sa ligne pour determiner la lettre a mettre
            index_surf = font.render(chr(ord('A') + self.pos[0]), True, (50, 50, 50))
            index_surf = pygame.transform.scale(index_surf, (1 / 36 * WINDOW_WIDTH - 10, 1 / 36 * WINDOW_WIDTH))
            index_rect = index_surf.get_frect(midright=(self.rect.midleft[0] - 15, self.rect.midleft[1] + 5))
            display_surface.blit(index_surf, index_rect)


class Opponent_case(pygame.sprite.Sprite): # meme principe que Case mais pour les cases adverse(le placement sur l'ecran change et on affichera les lettre des coordonnees non pas a geuche mais a droite de la grille)
    def __init__(self, pos, player_grid, groups): # et dans display si la case correspond a un bateau non 'tiré' on colorie de la meme facon que si cetait une case non 'tire' afin que le joueur ne voit pas les bateaux adverses
        super().__init__(groups)
        self.pos = pos
        self.surf = pygame.Surface((int((1 / 36) * WINDOW_WIDTH), int((1 / 36) * WINDOW_WIDTH)), pygame.SRCALPHA) #pygame.SRCALPHA permet juste de cree une surface de base qui est transparente et sur laquelle on pourra dessiner ou colorier par la suite
        self.rect = self.surf.get_frect(topleft=(int(((self.pos[1] + 4 + 18) / 36) * WINDOW_WIDTH),
                                                 int((self.pos[0] / 36) * WINDOW_WIDTH + (
                                                         WINDOW_HEIGHT - ((10 / 36) * WINDOW_WIDTH)) / 2)))
        self.is_green = False
        self.is_clicked = False
        self.player_grid = player_grid

    def curser_collision(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_green = True
        else:
            self.is_green = False

    def click_collision(self, click_pos):
        if self.rect.collidepoint(click_pos):
            self.is_clicked = True
        else:
            self.is_clicked = False

    def display(self):
        if self.player_grid[self.pos[0]][self.pos[1]] == 0:
            if self.is_green:
                self.surf.fill((100, 200, 100))
            else:
                self.surf.fill((40, 130, 210))
        elif self.player_grid[self.pos[0]][self.pos[1]] == 1:
            self.surf.fill((173, 216, 230))
        elif self.player_grid[self.pos[0]][self.pos[1]] == 2:
            self.surf.fill((255, 99, 71))
        elif self.player_grid[self.pos[0]][self.pos[1]] == 3:
            self.surf.fill((105, 105, 105))
        else:
            if self.is_green:
                self.surf.fill((100, 200, 100))
            else:
                self.surf.fill((40, 130, 210))

    def update(self, display_surface, font, mouse_pos, click_pos):
        self.curser_collision(mouse_pos=mouse_pos)
        self.click_collision(click_pos=click_pos)
        self.display()
        display_surface.blit(self.surf, self.rect)
        pygame.draw.line(display_surface, (220, 220, 220, 128), self.rect.topleft, self.rect.topright, 5)
        pygame.draw.line(display_surface, (220, 220, 220, 128), self.rect.topleft, self.rect.bottomleft, 5)
        pygame.draw.line(display_surface, (220, 220, 220, 128), self.rect.bottomleft, self.rect.bottomright, 5)
        pygame.draw.line(display_surface, (220, 220, 220, 128), self.rect.bottomright, self.rect.topright, 5)
        if self.pos[0] == 0:
            index_surf = font.render(str(self.pos[1] + 1), True, (50, 50, 50))
            index_surf = pygame.transform.scale(index_surf, (1 / 36 * WINDOW_WIDTH - 10, 1 / 36 * WINDOW_WIDTH))
            index_rect = index_surf.get_frect(midbottom=(self.rect.midtop[0], self.rect.midtop[1] - 5))
            display_surface.blit(index_surf, index_rect)
        if self.pos[1] == 9:
            index_surf = font.render(chr(ord('A') + self.pos[0]), True, (50, 50, 50))
            index_surf = pygame.transform.scale(index_surf, (1 / 36 * WINDOW_WIDTH - 10, 1 / 36 * WINDOW_WIDTH))
            index_rect = index_surf.get_frect(midleft=(self.rect.midright[0] + 15, self.rect.midright[1] + 5))
            display_surface.blit(index_surf, index_rect)


class Game:
    def __init__(self): # permet d'initialiser tt les parametre nessecaire a notre class
        self.running = True
        self.game_state = 0
        self.player1 = Player1(self.create_grid()) #on cree une instance de Player1 avec comme argument une grille rempli de 0 cree par la fct create_grid
        self.player2_ia = Player2_IA(self.create_grid())
        self.mouse_pos = (0, 0) #on initie les position de souri(et dans un endroit ou il ya rien c'est a dire tt en haut a gauche de l'ecran)
        self.click_pos = (0, 0)
        self.declick_pos = (0, 0)
        self.last_rotate_time = 0  # permet d'avoir un cas initial pour ce temps la(si on va voir sont utilisation dans run on comprend que lorsque l'on regarde ce temps la pour la premiere fois il est plus simple de cree un cas a part (if self.last_rotate_time ==0:) et ensuite on changera cette prise de temps par le vrai temps a savoir la dernier fois que l'on a rotate un bateau
        self.rotate_cooldown = 250  # c'est le temps necessaire avant de pouvoir a nouveau rotate notre bateau(correspond a 250 millisecondes)
        self.menu_music = pygame.mixer.Sound(join('musique', 'menu_music.mp3')) #importation d'un music
        self.game_music = pygame.mixer.Sound(join('musique', 'game_music.mp3'))
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #creation d'un fenetre a la taille: WINDOW_WIDTH, WINDOW_HEIGHT
        self.all_sprite = pygame.sprite.Group() #creation d'un groupe de sprites, utilisé par la suite pour stocker tt les sprite correspondant a des cases donc les instances de Case et de Opponent_Case
        self.cases_sprite = pygame.sprite.Group() # pareille mais que pour les instance de Case
        self.opponent_cases_sprite = pygame.sprite.Group()# que pour les Opponent_case, pour information un groupe de sprite permer de regrouper differentes instance de class qui sont considere comme sprite, cela permet de mieu manipuller les class sprite et donc de mieu y acceder
        self.font = pygame.font.Font(join('image', 'Oxanium-Bold.ttf'), 40) #importation d'une police d'ecriture pour les coordonner de nos cases
        self.game_background = pygame.transform.scale(pygame.image.load(join('image', 'game_background.jpg')).convert(),
                                                      (WINDOW_WIDTH, WINDOW_HEIGHT)) #importation de l'image de fond pour quand on joue(le convert() permet un meilleur rendu)
        self.menu_background = pygame.transform.scale(pygame.image.load(join('image', 'menu_background.png')).convert(),
                                                      (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.end_background = pygame.transform.scale(pygame.image.load(join('image', 'end_background.png')).convert(),
                                                      (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.quit_button = pygame.transform.scale(pygame.image.load(join('image', 'quit_button.png')).convert_alpha(), # le convert_alpha() a la meme utiliter que le convert() mais pour des image que lon superpose c'est a dire tt les image ajouter sur le background(en terme technique convert_alpha() prend en compte les pixelle transparent d'une image(par exemple nos bouton ne sont pas rond en realite ce sont des image carre mais avec des pixel transparant autour)
                                              (5 / 36 * WINDOW_WIDTH, 5 / 36 * WINDOW_WIDTH)) #!!!!! sert peut etre aussi a manupuler les mask !!!!
        self.quit_button_rect = self.quit_button.get_frect(midtop=(WINDOW_WIDTH / 2, 0))
        self.button1 = pygame.transform.scale(pygame.image.load(join('image', 'button1.png')).convert_alpha(),
                                              (5 / 36 * WINDOW_WIDTH, 5 / 36 * WINDOW_WIDTH))
        self.button1_rect = self.button1.get_frect(center=(1 * WINDOW_WIDTH / 6, 4 / 5 * WINDOW_HEIGHT)) # .get_frect() permet de cree une 'hitbox' pour notre bouton et de le placer a une position presise
        self.button2 = pygame.transform.scale(pygame.image.load(join('image', 'button2.png')).convert_alpha(),
                                              (6 / 36 * WINDOW_WIDTH, 6 / 36 * WINDOW_WIDTH))
        self.button2_rect = self.button2.get_frect(center=(3 * WINDOW_WIDTH / 6, 4 / 5 * WINDOW_HEIGHT))
        self.button3 = pygame.transform.scale(pygame.image.load(join('image', 'button3.png')).convert_alpha(),
                                              (5 / 36 * WINDOW_WIDTH, 5 / 36 * WINDOW_WIDTH))
        self.button3_rect = self.button3.get_frect(center=(5 * WINDOW_WIDTH / 6, 4 / 5 * WINDOW_HEIGHT))
        self.title = pygame.transform.scale(pygame.image.load(join('image', 'title.png')).convert_alpha(),
                                              (11 / 36 * WINDOW_WIDTH, 13 / 36 * WINDOW_HEIGHT))
        self.title_rect = self.title.get_frect(center=(WINDOW_WIDTH / 2, 1 / 5 * WINDOW_HEIGHT))
        self.icon = pygame.image.load(join('image', 'menu_background.png')).convert() #icone de notre fenetre
        self.win_message = self.font.render("VOUS AVEZ GAGNÉ", True, (44, 44, 44))
        self.win_message_rect = self.win_message.get_frect(center= (WINDOW_WIDTH / 2, 3 * WINDOW_HEIGHT / 8))
        self.loose_message = self.font.render("VOUS AVEZ PERDU", True, (44, 44, 44))
        self.loose_message_rect = self.loose_message.get_frect(center=(WINDOW_WIDTH / 2, 3 * WINDOW_HEIGHT / 8))

    def create_grid(self): #cree une grille a la taille de GRID_SIZE rempli de 0
        grid = []
        for i in range(GRID_SIZE):
            grid.append([0] * GRID_SIZE)
        return grid

    def create_player_case(self, grid): # cree tt les instance de Case avec leur coordonner dans la grille du joueur
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                Case([i, j], grid, (self.cases_sprite, self.all_sprite))

    def create_opponent_case(self, grid): # de meme pour l'adversaire
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                Opponent_case([i, j], grid, (self.opponent_cases_sprite, self.all_sprite))

    def run(self): #boucle du jeu
        pygame.display.set_caption('Bataille Navale') #titre de la fenetre
        pygame.display.set_icon(self.icon) #mise en place de l'incone de notre fenetre
        ok1 = False
        while self.running:
            self.menu_music.play(loops= -1) #on joue la music en boucle a l'infinie(loops = k veut dire que l'on joue k fois la musique avec k entier >0, et si l'on veut jouer en boucle a l'infini on met k= -1)
            while self.game_state == 0: #boucle du menu
                for event in pygame.event.get(): #event loop permettent de detecter si le joueur ferme la fenetre et si le joueur click quelque part
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.game_state = -1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.click_pos = event.pos
                if self.button1_rect.collidepoint(self.click_pos): #on regarde si le joueur a clicker sur le button1, si c'est le cas on reinitialise click pos et on change le game state ce qui nouss fera sortire de la boucle du menu pour aller dans celle de la v1
                    self.game_state = 1
                    self.click_pos = (0, 0)
                if self.button2_rect.collidepoint(self.click_pos): #pareil pour v2
                    self.game_state = 2
                    self.click_pos = (0, 0)
                if self.button3_rect.collidepoint(self.click_pos): #pareil mais pour v3
                    self.game_state = 3
                    self.click_pos = (0, 0)
                self.display_surface.blit(self.menu_background, (0, 0)) #on affiche tt ce qui est nessecaire et on fait bien attention a l'ordre(le dernier afficher est poser sur l'ecran peut importe l'image deriere donc si je met le backgroud en dernier je ne verrai que celui ci et rien d'autre)
                self.display_surface.blit(self.button1, self.button1_rect)
                self.display_surface.blit(self.button2, self.button2_rect)
                self.display_surface.blit(self.button3, self.button3_rect)
                self.display_surface.blit(self.title, self.title_rect)
                pygame.display.update() # on actualise l'image de notre fenetre afin de voir tt les modification

            self.menu_music.stop() #on arrete la musique du menu car on est sorti de la booucle du menu et on joue la musique du jeu
            self.game_music.play(loops= -1)

            while self.game_state == 1:
                self.display_surface.blit(self.game_background, (0, 0))
                if self.cases_sprite:
                    # (post-initialisation), le jeu commence vraiment
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            self.game_state = -1
                        elif event.type == pygame.MOUSEMOTION:
                            self.mouse_pos = event.pos
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.click_pos = event.pos
                    for case in self.opponent_cases_sprite:
                        case.update(self.display_surface, self.font, self.mouse_pos, self.click_pos)
                        if case.is_clicked:
                            if self.player1.can_shoot:
                                self.player1.shoot(case.pos)
                            else:
                                self.player1.can_shoot = True
                    for case in self.cases_sprite:
                        case.update(self.display_surface, self.font, self.mouse_pos, self.click_pos)
                    if self.player1.have_win():
                        self.game_state = 4
                    pygame.display.update()

                else:
                    # initialisation du jeu (placement des bateau etc...) !!!
                    self.create_player_case(self.player1.grid)
                    self.create_opponent_case(self.player2_ia.grid)
                    for i in range(SHIPS_NBR):
                        self.player2_ia.create_ships(i)
                    player1_opponent_grid_original = self.create_grid()
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            player1_opponent_grid_original[i][j] = self.player2_ia.grid[i][j]  # on a copier la grille original de l'ia de cette facon, ainsi aucune modification sur 'self.player2_ia.grid' n'apportera de changement sur 'player1_opponent_grid_original'
                    self.player1.set_opponent_settings(self.player2_ia.grid, player1_opponent_grid_original,
                                                       self.player2_ia.boat, self.player2_ia.torpedo,
                                                       self.player2_ia.submarine, self.player2_ia.cruiser,
                                                       self.player2_ia.aircraft)

            while self.game_state == 2: #EXACTEMENT MEME PRINCIPE QUE LA BOUCLE DE LA V3 EXPLIQUER PLUS BAS EN DETAIL(la seul ligne changé est: self.player2_ia.shoot('simple'), le mode utiliser dans la v3 est 'hard'
                self.display_surface.blit(self.game_background, (0, 0))
                if self.cases_sprite:
                    # (post-initialisation), le jeu commence vraiment
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            self.game_state = -1
                        elif event.type == pygame.MOUSEMOTION:
                            self.mouse_pos = event.pos
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.click_pos = event.pos
                    for case in self.opponent_cases_sprite:
                        case.update(self.display_surface, self.font, self.mouse_pos, self.click_pos)
                        if case.is_clicked:
                            if self.player1.can_shoot:
                                self.player1.shoot(case.pos)
                            else:
                                self.player2_ia.can_shoot = True
                                if self.player2_ia.shoot_cooldown():
                                    self.player2_ia.shoot('simple')
                                if self.player2_ia.can_shoot == False:
                                    self.click_pos = (0,
                                                      0)  # permet de ne pas prendre en compte les clicks que le joueur a fait pendent que l'ia tirait, ce qui fait que c'est seulement une fois quelle a terminer que les click de joueur sont pris en compte(le probleme etait que si l'on cliquait pendant que l'ia jouait, une fois qu'elle avait terminer ca nous faisait directement tirer sur la case qu'on avait cliquer(c du detail)
                                    self.player1.can_shoot = True
                    for case in self.cases_sprite:
                        case.update(self.display_surface, self.font, self.mouse_pos, self.click_pos)
                    for ship in self.player1.ships_sprite:  # comme dans la fase d'initialisation plus bas dans le code on fini tjr par afficher tt nos bateau(apres avoir afficher les cases sinon ce serait les case qui serai devant les bateau et on ne verrai donc pas les bateaux)
                        ship.display(self.display_surface)
                    if self.player1.have_win():
                        self.game_state = 4
                    elif self.player2_ia.have_win():
                        self.game_state = 5
                    pygame.display.update()

                else:
                    # initialisation du jeu (placement des bateau etc...) !!!
                    if ok1:
                        self.create_player_case(self.player1.grid)
                        self.create_opponent_case(self.player2_ia.grid)
                        while ok1:
                            self.display_surface.blit(self.game_background, (0, 0))
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    self.running = False
                                    self.game_state = -1
                                    ok1 = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    self.click_pos = event.pos
                                elif event.type == pygame.MOUSEMOTION:
                                    self.mouse_pos = event.pos
                                elif event.type == pygame.MOUSEBUTTONUP:
                                    self.declick_pos = event.pos
                            for ship in self.player1.ships_sprite:
                                ship.click_collision(self.click_pos)
                                if (ship.is_clicked and ship.is_placed == False):
                                    if pygame.mouse.get_pressed()[0]:  # regarde si l'on est tjr entrain d'appuiller
                                        ship.update_pos(self.mouse_pos, self.display_surface)
                                        if pygame.key.get_pressed()[
                                            pygame.K_r]:  # on regarde si le joueur appui sur r et donc souhaite rotate sont bateau
                                            if self.last_rotate_time == 0:  # on cree un timing affin de pouvoir rotate que tout les 'self.rotate_cooldown' millisecondes, cela permet surtout d'eviter le probleme de trop rotate(en effet si on appui qu'une seul fois sur la touche r le code etant rapide il peut detecter plusieur fois que c'est appuiller et donc rotate plusieur fois au lieu de une
                                                ship.rotate()
                                                self.last_rotate_time = pygame.time.get_ticks()
                                            elif pygame.time.get_ticks() - self.last_rotate_time >= self.rotate_cooldown:
                                                ship.rotate()
                                                self.last_rotate_time = pygame.time.get_ticks()
                                        for case in self.cases_sprite:
                                            case.update(self.display_surface, self.font, self.mouse_pos, (0, 0))
                                    else:
                                        for case in self.cases_sprite:
                                            case.update(self.display_surface, self.font, self.mouse_pos,
                                                        self.declick_pos)
                                            if case.is_clicked:
                                                ship.place_ship(case.pos[1], case.pos[0])
                                                self.player1.create_ships(ship.size - 1, case.pos)
                                                self.declick_pos = (0, 0)
                                                ok2 = True
                                            else:
                                                ok2 = False
                                        if (ok2 == False and ship.is_placed == False):
                                            ship.replace()
                                else:
                                    for case in self.cases_sprite:
                                        case.update(self.display_surface, self.font, self.mouse_pos, self.declick_pos)
                            for case in self.opponent_cases_sprite:
                                case.update(self.display_surface, self.font, self.mouse_pos, self.declick_pos)
                            ships_placed = 0
                            for ship in self.player1.ships_sprite:
                                if ship.is_placed:
                                    ships_placed += 1
                                ship.display(self.display_surface)
                            if ships_placed == 5:
                                player2_ia_opponent_grid_original = self.create_grid()
                                for i in range(GRID_SIZE):
                                    for j in range(GRID_SIZE):
                                        player2_ia_opponent_grid_original[i][j] = self.player1.grid[i][j]
                                self.player2_ia.set_opponent_settings(self.player1.grid,
                                                                      player2_ia_opponent_grid_original,
                                                                      self.player1.boat, self.player1.torpedo,
                                                                      self.player1.submarine, self.player1.cruiser,
                                                                      self.player1.aircraft)
                                ok1 = False
                            pygame.display.update()
                    else:
                        for i in range(SHIPS_NBR):
                            self.player2_ia.create_ships(i)
                        player1_opponent_grid_original = self.create_grid()
                        for i in range(GRID_SIZE):
                            for j in range(GRID_SIZE):
                                player1_opponent_grid_original[i][j] = self.player2_ia.grid[i][
                                    j]  # on a copier la grille original de l'ia de cette facon, ainsi aucune modification sur 'self.player2_ia.grid' n'apportera de changement sur 'player1_opponent_grid_original'
                        self.player1.set_opponent_settings(self.player2_ia.grid, player1_opponent_grid_original,
                                                           self.player2_ia.boat, self.player2_ia.torpedo,
                                                           self.player2_ia.submarine, self.player2_ia.cruiser,
                                                           self.player2_ia.aircraft)
                        ok1 = True

            while self.game_state == 3: #correspond a la boucle du jeu pour jouer a la l'equivalent de la V3 ATTENTION NE PAS FORCEMENT LIRE LE CODE DE HAUT EN BAS, PLUTOT LE LIRE DANS LORDRE DE DEROULEMENT DU JEU(jai donner les etapes pour faciliter la lecture)
                self.display_surface.blit(self.game_background, (0, 0))
                # 3eme ETAPE:
                if self.cases_sprite:
                    # (post-initialisation), le jeu commence vraiment
                    for event in pygame.event.get(): #event loop permettant de detecter le fait de fermer la fenetre et donc de quitter le jeux, de detecter les mouvement de la souris et de lui associer une position ainsi que de detecter si on click sur un bouton de la souri et aussi lui associer une positions
                        if event.type == pygame.QUIT:
                            self.running = False
                            self.game_state = -1
                        elif event.type == pygame.MOUSEMOTION:
                            self.mouse_pos = event.pos
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.click_pos = event.pos
                    for case in self.opponent_cases_sprite: #cette boucle for permet d'afficher et d'actualiser les case adverse
                        case.update(self.display_surface, self.font, self.mouse_pos, self.click_pos)
                        if case.is_clicked: #on regarde si une case a ete clické(donc si le joueur a 'tiré' sur celle ci)
                            if self.player1.can_shoot: #si le joueur peut tirer on applique sa fct shoot
                                self.player1.shoot(case.pos)
                            else: #sinon on donne le droit a l'adversere de tirer car si on est ici c'est que le joueur a rater et c'est donc au tour de l'adversaire de tirer
                                self.player2_ia.can_shoot = True
                                if self.player2_ia.shoot_cooldown(): #on regarde si l'ia peut a nouveau tirer par rapport au temps passer depuis sont dernier tire(permet de ne pas avoir une ia qui donne l'impression de tirer plusieur case d'un coup
                                    self.player2_ia.shoot('hard') #on est dans la v3 donc on utilise l'ia avancer d'ou le 'hard' en parametre qui permet a la fct shoot de Player2_IA de d'abord choisir les potential_target avant les can_shoot(est deja explique en detail dans la fct en question)
                                if self.player2_ia.can_shoot == False:#veut dire que l'ia a rater, c'est donc au joueur de tirer
                                    self.click_pos = (0, 0)  # permet de ne pas prendre en compte les clicks que le joueur a fait pendent que l'ia tirait, ce qui fait que c'est seulement une fois quelle a terminer que les click du joueur sont pris en compte(le probleme etait que si l'on cliquait pendant que l'ia jouait, une fois qu'elle avait terminer ca nous faisait directement tirer sur la case qu'on avait clique
                                    self.player1.can_shoot = True
                    for case in self.cases_sprite: #permet d'afficher et d'actualiser les case du joueur
                        case.update(self.display_surface, self.font, self.mouse_pos, self.click_pos)
                    for ship in self.player1.ships_sprite:  # comme dans la phase d'initialisation plus bas dans le code on fini tjr par afficher tt nos bateau(apres avoir afficher les cases sinon ce serait les case qui serai devant les bateau et on ne verrai donc pas les bateaux)
                        ship.display(self.display_surface)
                    if self.player1.have_win(): # on ragarde si quelqu'un a gagner, si c'est le cas on change de boucle de jeu
                        self.game_state = 4
                    elif self.player2_ia.have_win():
                        self.game_state = 5
                    pygame.display.update() # permet d'actualiser l'image de la fenetre avec tt les modification nessecaire a chaque fin de boucle

                else:
                    # initialisation du jeu (placement des bateau etc...) !!!
                    # 2eme ETAPE:
                    if ok1: #on va rentrer dans la boucle de placement des bateaux du joueur
                        self.create_player_case(self.player1.grid) #creation des instance de class sprite des cases de nos grilles(cree les case physique et visuelle)
                        self.create_opponent_case(self.player2_ia.grid)
                        while ok1:
                            self.display_surface.blit(self.game_background, (0, 0)) #comme tjr on commence par afficher le fond
                            for event in pygame.event.get(): #event loop permettant de detecter le fait de fermer la fenetre et donc de quitter le jeux, de detecter les mouvement de la souris et de lui associer une position ainsi que de detecter si on click ou declick un bouton de la souri et aussi leur associer des positions
                                if event.type == pygame.QUIT:
                                    self.running = False
                                    self.game_state = -1
                                    ok1 = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    self.click_pos = event.pos
                                elif event.type == pygame.MOUSEMOTION:
                                    self.mouse_pos = event.pos
                                elif event.type == pygame.MOUSEBUTTONUP:
                                    self.declick_pos = event.pos
                            for ship in self.player1.ships_sprite: #dans cette boucle for on regarde tt les bateau du joueur qui sont considerer comme des class de sprite a part entier et on regarde si il sont en collision avec un click de souri
                                ship.click_collision(self.click_pos)
                                if (ship.is_clicked and ship.is_placed == False): #ceci correspond au cas ou le joueur a clicker sur un bateau qui n'est pas consideré comme placer
                                    if pygame.mouse.get_pressed()[0]:  # regarde si l'on est tjr entrain d'appuiller
                                        ship.update_pos(self.mouse_pos, self.display_surface) #on fait suivre le bateau a la souri
                                        if pygame.key.get_pressed()[pygame.K_r]:  # on regarde si le joueur appui sur r et donc souhaite rotate sont bateau
                                            if self.last_rotate_time == 0:  # on cree un timing affin de pouvoir rotate que tout les 'self.rotate_cooldown' millisecondes, cela permet surtout d'eviter le probleme de trop rotate(en effet si on appui qu'une seul fois sur la touche r le code etant rapide il peut detecter plusieur fois que c'est appuiller et donc rotate plusieur fois au lieu de une
                                                ship.rotate()  #cela corerspond au cas initiale, donc la premier fois de la partie que le joueur rotate un bateau
                                                self.last_rotate_time = pygame.time.get_ticks()
                                            elif pygame.time.get_ticks() - self.last_rotate_time >= self.rotate_cooldown: # comme dit precedamment on regarde si on peut rotate a nouveau
                                                ship.rotate()
                                                self.last_rotate_time = pygame.time.get_ticks() #self.last_rotate_time correspond au temps du jeu pendant lequelle on a effectué notre dernire rotation de bateau et si on appelle directement pygame.time.get_ticks(), cela nous donne le temps actuelle ainsi la difference des deux nous donne le temps passé depuis notre derniere rotation de bateau
                                        for case in self.cases_sprite:
                                            case.update(self.display_surface, self.font, self.mouse_pos, (0, 0)) #pemet d'afficher les case du joueur dans le cas ou le joueur continue d'appuiller sur la souri
                                    else: #cela veut dire forcement que l'on a lacher un bateau qulque part car si on est ici c'est qu'un bateau a ete selectionné et que le joueur a lacher le boutton de la souri
                                        for case in self.cases_sprite:
                                            case.update(self.display_surface, self.font, self.mouse_pos,
                                                        self.declick_pos) # pemet d'afficher les case du joueur dans le cas ou je joueur a lacher le bouton de la souri
                                            if case.is_clicked: #on regarde donc si le joueur a lacher le bateau sur une case, si c'est le cas on essaye de placer ce bateau
                                                ship.place_ship(case.pos[1], case.pos[0])
                                                self.player1.create_ships(ship.size - 1, case.pos) # si il y a une erreur de positionnoment la fct create_ships s'occupe automatiquement de replacer le bateau en bas de l'ecran en utilisant directement la fct replace() associe a ce bateau
                                                self.declick_pos = (0, 0)
                                                ok2 = True
                                            else:
                                                ok2 = False
                                        if (ok2 == False and ship.is_placed == False): #dans ce cas cela veut dire que le joueur na pas lacher le bateau sur une case, un le replace donc avec la fct replace() propre a ce bateau
                                            ship.replace()
                                else: #cas ou le joueur n'a pas selectionner de bateau non placé
                                    for case in self.cases_sprite: #permet d'afficher les case du joueur dans ce cas la
                                        case.update(self.display_surface, self.font, self.mouse_pos, self.declick_pos)
                            for case in self.opponent_cases_sprite: #permet d'afficher les case adverse dans tt les cas puisque on est a la fin de la boucle ou le scripte est obliger de passer
                                case.update(self.display_surface, self.font, self.mouse_pos, self.declick_pos)
                            ships_placed = 0 #initialisation
                            for ship in self.player1.ships_sprite: #on compte le nombre de bateau placés
                                if ship.is_placed:
                                    ships_placed += 1
                                ship.display(self.display_surface) #on affiche les bateau(en dernier car on veut les voir devant les cases et non derriere
                            if ships_placed == 5: #cas ou tt les bateau on ete placer
                                player2_ia_opponent_grid_original = self.create_grid() #on va cree une 'capture' de la grille advers qui ne changera pas dans le temps(sert dans les fct shoot lorsque que l'on coule un bateau)
                                for i in range(GRID_SIZE):
                                    for j in range(GRID_SIZE):
                                        player2_ia_opponent_grid_original[i][j] = self.player1.grid[i][j]
                                self.player2_ia.set_opponent_settings(self.player1.grid, player2_ia_opponent_grid_original, self.player1.boat, self.player1.torpedo, self.player1.submarine, self.player1.cruiser, self.player1.aircraft)
                                ok1 = False #le joueur 2 a maintenent tt les donnees nessecaire pour jouer on met donc ok1 en False et comme on a cree des cases la condition if self.cases_sprite: du debut de la boucle s'activera et on pacera dans la phase de 'tire' de la partie
                            pygame.display.update() # permet d'actualiser l'image de la fenetre avec tt les modification nessecaire a chaque fin de boucle
                    # 1er ETAPE:
                    else: #on cree et place tt les bateau de l'ia(c'est la premier chose faite dans la boucle while self.game_state == 3)
                        for i in range(SHIPS_NBR):
                            self.player2_ia.create_ships(i)
                        player1_opponent_grid_original = self.create_grid()
                        for i in range(GRID_SIZE):
                            for j in range(GRID_SIZE):
                                player1_opponent_grid_original[i][j] = self.player2_ia.grid[i][j]  # on a copier la grille original de l'ia de cette facon, ainsi aucune modification sur 'self.player2_ia.grid' n'apportera de changement sur 'player1_opponent_grid_original'
                        self.player1.set_opponent_settings(self.player2_ia.grid, player1_opponent_grid_original, self.player2_ia.boat, self.player2_ia.torpedo, self.player2_ia.submarine, self.player2_ia.cruiser, self.player2_ia.aircraft)
                        ok1 = True #on a donc pue remplire tt les donner adverse nessessaire pour notre joueur et on met ok1 = True afin de passer a l'etape suivante de notre partie(a savoir le placement de nos propre bateau)

            while self.game_state == 4: #menu de victoir pour le joueur
                for event in pygame.event.get(): #event loop permettant de quitter le jeu ou de revenir au menu principale
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.game_state = -1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.click_pos = event.pos
                if self.quit_button_rect.collidepoint(self.click_pos):
                    self.game_state = 0
                self.display_surface.blit(self.end_background, (0, 0))
                self.display_surface.blit(self.win_message, self.win_message_rect)
                self.display_surface.blit(self.quit_button, self.quit_button_rect)
                pygame.display.update()

            while self.game_state == 5: #menu de defaite pour le joueur(meme principe que celui pour la victoire)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.game_state = -1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.click_pos = event.pos
                if self.quit_button_rect.collidepoint(self.click_pos):
                    self.game_state = 0
                self.display_surface.blit(self.end_background, (0, 0))
                self.display_surface.blit(self.loose_message, self.loose_message_rect)
                self.display_surface.blit(self.quit_button, self.quit_button_rect)
                pygame.display.update()

            for case in self.all_sprite:  # on suprime tt les sprites du group self.all_sprite donc en gros on supprime tt les instance de Case qui on etait cree au cours de la parti precedente
                case.kill()
            for ship in self.player1.ships_sprite:  # de meme mais pour les bateaux du joueur, le but deriere tt ca est de pouvoir relancer d'autre parties(et donc il faut "oublier" tt ce qui c'est passer dans les parties precedente)
                ship.kill()
            self.player1.__init__(
                self.create_grid())  # permet de reinitialiser l'instance self.player1 afin de pouvoir relancer d'autre parti en repartant de 0 a chaque fois
            self.player2_ia.__init__(
                self.create_grid())  # permet de reinitialiser l'instance self.player2_ia afin de pouvoir relancer d'autre parti en repartant de 0 a chaque fois
            self.click_pos = (0, 0)  # on reinitialise tt les position de souri par precotion afin de ne pas detecter les anciens clicks dans les nouvelles parties
            self.mouse_pos = (0, 0)
            self.declick_pos = (0, 0)
            self.last_rotate_time = 0  # tjr dans la logique de tt reinitialiser
            self.game_music.stop() #on stop la music car on sait qu'une fois arriver la, soit on a quitter le jeu soit on va au menu principal

pygame.init() #initialisation de pygame afin de pouvoir l'utiliser
game = Game() #creation d'une instance de Game
game.run() #appelle de la fct run de notre instance game
pygame.quit() #si on est ici cela veut dire que run et terminer et donc que le joueur a quitter le jeu donc on met fin a pygame