function isValid(grid, row, col, num) {
    // Vérification de la ligne
    if (grid[row].includes(num)) {
        return false;
    }
    // Vérification de la colonne
    for (let i = 0; i < 9; i++) {
        if (grid[i][col] === num) {
            return false;
        }
    }
    // Vérification du carré 3x3
    let boxStartRow = Math.floor(row / 3) * 3;
    let boxStartCol = Math.floor(col / 3) * 3;
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            if (grid[boxStartRow + i][boxStartCol + j] === num) {
                return false;
            }
        }
    }
    return true;
}

function findEmptyCell(grid) {
    for (let i = 0; i < 81; i++) {
        let x = Math.floor(Perm[i] / 9);
        let y = Perm[i] % 9;
        if (grid[x][y] === null) {
            return [x, y];
        }
    }
    return null;
}

function findEmptyCellStraight(grid) {
    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            if (grid[row][col] === null) {
                return [row, col];
            }
        }
    }
    return null;
}

function solveSudoku(grid) {
    let emptyCell = findEmptyCell(grid);
    if (!emptyCell) {
        return true;
    }
    let [row, col] = emptyCell;
    for (let num = 1; num <= 9; num++) {
        if (isValid(grid, row, col, num)) {
            grid[row][col] = num;
            if (solveSudoku(grid)) {
                return true;
            }
            grid[row][col] = null;
        }
    }
    return false;
}

function printSudoku(grid) {
    for (let i = 0; i < 9; i++) {
        console.log(grid[i].map(num => (num === null ? "." : num)).join(" "));
        if (i === 2 || i === 5) console.log(""); 
    }
}

function str2grid(str) {
    str = str.replace(/\s|\n/g, "");
    if (str.length !== 81) {
        return null;
    }
    let grid = Array.from({ length: 9 }, () => Array(9).fill(null));
    for (let i = 0; i < 81; i++) {
        let num = parseInt(str[i], 10);
        if (!isNaN(num) && num !== 0) {
            grid[Math.floor(i / 9)][i % 9] = num;
        }
    }
    return grid;
}

function go(sudokuGrid) {
    console.log("Grille Sudoku initiale :");
    printSudoku(sudokuGrid);
    if (solveSudoku(sudokuGrid)) {
        console.log("\nSolution trouvée :");
        printSudoku(sudokuGrid);
    } else {
        console.log("\nPas de solution trouvée.");
    }
}

function shuffleArray(array,n=-1) {
    if (n==-1)
        n = array.length;// donc fera le nombre de pas prevu par l'algo
    let cpt = 0;
    for (let i = array.length - 1; i > 0; i--) {
        if (cpt==n)
            break
        cpt += 1
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Échange des éléments
    }
}

// EN AVANT SIMONE
let Perm = Array.from({ length: 81 }, (_, i) => i);

let sudokuGrid = [
    [5, 3, null, null, 7, null, null, null, null],
    [6, null, null, 1, 9, 5, null, null, null],
    [null, 9, 8, null, null, null, null, 6, null],
    [8, null, null, null, 6, null, null, null, 3],
    [4, null, null, 8, null, 3, null, null, 1],
    [7, null, null, null, 2, null, null, null, 6],
    [null, 6, null, null, null, null, 2, 8, null],
    [null, null, null, 4, 1, 9, null, null, 5],
    [null, null, null, null, 8, null, null, 7, 9]
];

let zeroGrid = [
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null]
];

let unGrid = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null]
];

shuffleArray(Perm,5)

console.log(Perm)
go(unGrid);
