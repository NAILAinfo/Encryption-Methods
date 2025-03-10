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