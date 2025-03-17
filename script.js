export function estMinuscule(c) {
    return c >= 'a' && c <= 'z';
}
export function valeurNum(c){
    return c.charCodeAt(0) - 65;
}
export function valeurAlpha(c){
    return String.fromCharCode(c + 65);
}


export function cesare(msg, decalage) {
    let result = "";
    msg = msg.toUpperCase();

    for (let i = 0; i < msg.length; i++) {
        let char = msg[i];
        if (char >= 'A' && char <= 'Z') {
            let codeChiffre = (valeurNum(char) + decalage) % 26;
            if (codeChiffre < 0) {
                codeChiffre += 26; 
            }
            result += valeurAlpha(codeChiffre);
        } else {
            result += char;
        }
    }
    return result;
}
export function vignere(msg, cle) {
    let result = "";
    msg = msg.toUpperCase().replace(/[^A-Z]/g, ""); 
    cle = cle.toUpperCase().replace(/[^A-Z]/g, ""); 

    if (cle.length === 0) {
        return "Erreur : la clé doit contenir au moins une lettre.";
    }

    for (let i = 0, j = 0; i < msg.length; i++) {
        let n = valeurNum(msg[i]);
        let k = valeurNum(cle[j % cle.length]);
        let newCharCode = (n + k) % 26;
        result += valeurAlpha(newCharCode);
        j++; 
    }
    return result;
}
export function vignereD(msg, cle) {
    let result = "";
    msg = msg.toUpperCase().replace(/[^A-Z]/g, ""); 
    cle = cle.toUpperCase().replace(/[^A-Z]/g, ""); 

    if (cle.length === 0) {
        return "Erreur : la clé doit contenir au moins une lettre.";
    }

    for (let i = 0, j = 0; i < msg.length; i++) {
        let n = valeurNum(msg[i]);
        let k = valeurNum(cle[j % cle.length]);
        let newCharCode = (n - k+ 26) % 26;
        result += valeurAlpha(newCharCode);
        j++; 
    }
    return result;
}
//****************************************************************** */
export function hill(text, matrixString) {
    let matrix = parseMatrix(matrixString);
    if (!matrix) return "Erreur : Matrice invalide !";

    let textVector = textToVector(text, matrix.length);
    let encryptedVector = multiplyMatrixVector(matrix, textVector);

    return vectorToText(encryptedVector);
}

export function hillD(text, matrixString) {
    let matrix = parseMatrix(matrixString);
    if (!matrix) return "Erreur : Matrice invalide !";

    let inverseMatrix = invertMatrix(matrix);
    if (!inverseMatrix) return "Erreur : Matrice non inversible !";

    let textVector = textToVector(text, matrix.length);
    let decryptedVector = multiplyMatrixVector(inverseMatrix, textVector);

    return vectorToText(decryptedVector);
}

// Fonction pour transformer la matrice en tableau
function parseMatrix(matrixString) {
    try {
        return matrixString.split(";").map(row => row.split(",").map(Number));
    } catch {
        return null;
    }
}

// Convertir texte en vecteur numérique
function textToVector(text, size) {
    let vector = text.toUpperCase().split("").map(char => char.charCodeAt(0) - 65);
    while (vector.length % size !== 0) {
        vector.push(23); // Remplissage avec 'X'
    }
    return chunkArray(vector, size);
}

// Transformer un vecteur en texte
function vectorToText(vector) {
    return vector.flat().map(num => String.fromCharCode((num % 26) + 65)).join("");
}

// Multiplication matrice-vecteur
function multiplyMatrixVector(matrix, vector) {
    return vector.map(v =>
        matrix.map(row =>
            row.reduce((sum, val, i) => sum + val * v[i], 0) % 26
        )
    );
}

// Inversion de matrice modulo 26
function invertMatrix(matrix) {
    let det = determinant(matrix);
    let detInv = modInverse(det, 26);
    if (detInv === null) return null;

    let adj = adjugateMatrix(matrix);
    return adj.map(row => row.map(val => (val * detInv) % 26));
}

// Calcul du déterminant d'une matrice 2x2
function determinant(matrix) {
    if (matrix.length !== 2 || matrix[0].length !== 2) return null;
    return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26;
}

// Adjugate (cofacteurs pour 2x2)
function adjugateMatrix(matrix) {
    return [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]];
}

// Inverse modulaire
function modInverse(a, m) {
    a = ((a % m) + m) % m;
    for (let x = 1; x < m; x++) {
        if ((a * x) % m === 1) return x;
    }
    return null;
}

// Diviser un tableau en sous-tableaux de taille donnée
function chunkArray(arr, size) {
    let result = [];
    for (let i = 0; i < arr.length; i += size) {
        result.push(arr.slice(i, i + size));
    }
    return result;
}

export function affineEncrypt(text, a, b) {
    if (gcd(a, 26) !== 1) return "Erreur : 'a' doit être copremier avec 26 !";
    
    return text.toUpperCase().split("").map(char => {
        if (char < "A" || char > "Z") return char;
        let x = char.charCodeAt(0) - 65;
        return String.fromCharCode(((a * x + b) % 26) + 65);
    }).join("");
}

export function affineDecrypt(text, a, b) {
    let aInv = modInverse(a, 26);
    if (aInv === null) return "Erreur : 'a' n'a pas d'inverse mod 26 !";

    return text.toUpperCase().split("").map(char => {
        if (char < "A" || char > "Z") return char;
        let y = char.charCodeAt(0) - 65;
        return String.fromCharCode(((aInv * (y - b + 26)) % 26) + 65);
    }).join("");
}

function gcd(a, b) {
    return b === 0 ? a : gcd(b, a % b);
}

function modInverse(a, m) {
    a = ((a % m) + m) % m;
    for (let x = 1; x < m; x++) {
        if ((a * x) % m === 1) return x;
    }
    return null;
}

