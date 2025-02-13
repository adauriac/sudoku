"""
Solution du sudoku version chatGPT ie recursif
trouve une solution si il y en a une, et detecte s'il n'y en a pas.
Quand il y a plusieurs solutions le chois de la solution trouvee vient de
find_empty_cell et de l'ordre qu'il utilise pour trouver la premiere cell vide 

Il y a : 
    find_empty_cell qui est la fonction effectivement appellée
    find_empty_cell_ORIG(grid) qui marche bien 
    my_find_empty_cell(grid) qui utilise la liste global Perm pour chercher le prochain nombre a trouver
    on branche l'une ou l'autre avec find_empty_cell = find_empty_cell_ORIG ou find_empty_cell = my_find_empty_cell 
    de plus dans my_find_empty_cell si il n'y a pas de Perm deja definie utilise l'identité

    PROBLÈME RETESTE UNE CONFIGURATION DÉJÀ ESSAYÉE SI ON UTILISE UNE PERMUTATION NON TRIVIALE ????????

"""
def is_valid(grid, row, col, num):
    """Vérifie si `num` peut être placé à la position (row, col) sans violer les règles du Sudoku."""
    # Vérification de la ligne
    if num in grid[row]:
        return False   
    # Vérification de la colonne
    if num in (grid[i][col] for i in range(9)):
        return False    
    # Vérification du carré 3x3
    box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[box_start_row + i][box_start_col + j] == num:
                return False
    return True
# FIN is_valid

def my_find_empty_cell(grid):
    """
    Retourne la première cellule vide (None) sous forme de tuple (row, col), ou None si la grille est complète.
    l'ordre d'inspection est dicté par la permutation Perm de [0..80] variable gloale
    """
    global Perm
    if not "Perm" in globals():
        print("creating Perm")
        Perm = list(range(81))
    for i in range(81):
        x = Perm[i]//9
        y = Perm[i]%9
        if grid[x][y] is None: return(x,y)
    return None
# FIN my_find_empty_cell(grid)

def find_empty_cell_ORIG(grid):
    """Retourne la première cellule vide (None) sous forme de tuple (row, col), ou None si la grille est complète."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] is None:  # Une case vide est représentée par None
                return (row, col)
    return None
# FIN find_empty_cell_ORIG(grid)

def solve_sudoku(grid):
    """Résout le Sudoku en remplissant `grid` avec une approche récursive de backtracking."""
    str=""
    for i in range(9):
        for j in range(9):
            str+= "." if grid[i][j]is None else "%d"%grid[i][j]
    print(f"{str=}")
    empty_cell = find_empty_cell(grid)
    if not empty_cell:  # Si plus aucune case vide, la grille est résolue
        return True
    row, col = empty_cell
    for num in range(1, 10):  # Essai des chiffres de 1 à 9
        if is_valid(grid, row, col, num):
            grid[row][col] = num  # Place un chiffre valide            
            if solve_sudoku(grid):  # Récursion
                return True           
            grid[row][col] = None  # Annule le choix (backtrack)    
    return False  # Aucun chiffre n'a fonctionné, retour en arrière
# FIN solve_sudoku(grid)

def print_sudoku(grid):
    for i in range(9):
        for j in range(9):
            print("." if grid[i][j]==None else grid[i][j],end=" " if j==2 or j==5 else "")
        print("\n" if i==2 or i==5 else "")
# FIN myPrint(grid)

def str2grid(strinGrid):
    """ peut contenir 0,1,..,9,blanc, retour ligne rtourne None ou la liste de liste d'entiers"""
    strinGrid=strinGrid.replace(" ","").replace("\n","")
    if len(strinGrid) != 81:
       return None
    res = [[None for i in range(9)] for j in range(9)]
    for i,c in enumerate(strinGrid):
        try :
            if c!='0':
                res[i//9][i%9] = int(c) 
        except :
            return None
    return res
# FIN str2grid

def go(sudoku_grid):# Affichage de la grille avant résolution
    print("Grille Sudoku initiale :")
    print_sudoku(sudoku_grid)
    # Résolution du Sudoku
    if solve_sudoku(sudoku_grid):
        print("\nSolution trouvée :")
        print_sudoku(sudoku_grid)
    else:   
        print("\nPas de solution trouvée.")
# FIN go(grid)

# Exemple de grille Sudoku à résoudre (0 ou None représentent des cases vides)
sudoku_grid = [
    [5, 3, None, None, 7, None, None, None, None],
    [6, None, None, 1, 9, 5, None, None, None],
    [None, 9, 8, None, None, None, None, 6, None],
    [8, None, None, None, 6, None, None, None, 3],
    [4, None, None, 8, None, 3, None, None, 1],
    [7, None, None, None, 2, None, None, None, 6],
    [None, 6, None, None, None, None, 2, 8, None],
    [None, None, None, 4, 1, 9, None, None, 5],
    [None, None, None, None, 8, None, None, 7, 9]
]
zero_grid = [[None for i in range(9)] for j in range(9)]
example1 = str2grid("030007240640020509700009000000053608900201007405970000000700005506030021098100034")
example2 = str2grid("950300401000500002040080007009000050006408200070000300700060020800007000605004093")
example3 = str2grid("300024007000030600970651002600090080250000079080070005500743018008010000700560004")
example4 = str2grid("508004000600070009000030060015700000920080041000001970060010000700020008000900302")
example5 = str2grid("900417005003086000000900040270000403430000098601000057050001000000790500700528006")
exsimple = str2grid("958372461367541982241689537489723156136458279572196348713965824894237615625804093")
exsimple = str2grid("008372461367541982241689537489723156136458279572196348713965824894237615625804093")

Perm = list(range(81))
import random
# random.shuffle(Perm)
Perm.reverse()
find_empty_cell = my_find_empty_cell
go(zero_grid)
# go(exsimple)