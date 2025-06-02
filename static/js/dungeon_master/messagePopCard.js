function mostrarPopup(nombre, vida, mana, armadura) {
    document.getElementById('popup-nombre').textContent = nombre;
    document.getElementById('popup-vida').textContent = vida;
    document.getElementById('popup-mana').textContent = mana;
    document.getElementById('popup-armadura').textContent = armadura;
    document.getElementById('popup').style.display = 'flex';
}

function cerrarPopup() {
    document.getElementById('popup').style.display = 'none';
}