function estMinuscule(c) {
    return c >= 'a' && c <= 'z';
}
function valeurNum(c){
    return c.charCodeAt(0) - 65;
}
function valeurAlpha(c){
    return String.fromCharCode(c + 65);
}