const formTemplates = {
    'create-character': `
        <div id="create-character">
        <h2>Crear Personaje</h2>
        <hr>
        <form id="form-character">
            <label for="name">Nombre del personaje:</label>
            <input type="text" name="name" placeholder="Character Name" required>
            <br><br>

            <label for="race-select">Raza:</label>
            <select name="race_id" id="race-select" required>
            <!-- Opciones de razas aquí, ejemplo: -->
            <!-- <option value="1">Elf</option> -->
            </select>

            <label for="class-select">Clase:</label>
            <select name="class_id" id="class-select" required>
            <!-- Opciones de clases aquí, ejemplo: -->
            <!-- <option value="1">Warrior</option> -->
            </select>

            <br><br>
            <label for="class-select">Nivel de ataque:</label>
            <input type="number" name="attack" placeholder="Attack Level" min="0" value="0" required>
            <br><br>
            <label for="class-select">Nivel de defenza:</label>
            <input type="number" name="defense" placeholder="Defense Level" min="0" value="0" required>
            
            <br><br>
            <button type="submit" class="btn-medieval btn-add btn-success">Save</button>
        </form>
    `,


    'create-mission': `
      <h2>Crear misión</h2>
      <form id="form-mission">
        <input type="text" name="name" placeholder="Nombre de la misión" required>
        <input type="number" name="location_id" placeholder="ID de ubicación" required>
        <input type="number" name="reward" placeholder="Recompensa">
        <button type="submit" class="btn-medieval btn-add">Guardar</button>
      </form>
    `
};
const races = [
  { id: 1, name: "Elf", description: "Agile and intelligent" },
  { id: 2, name: "Dwarf", description: "Sturdy and strong" },
];

const classes = [
  { id: 1, name: "Warrior", description: "Close combat fighter" },
  { id: 2, name: "Mage", description: "Master of magic" },
];

function fillSelectAndTable() {
  const raceSelect = document.getElementById('race-select');
  const racesTableBody = document.querySelector('#races-table tbody');

  races.forEach(race => {
    // Opciones select
    const option = document.createElement('option');
    option.value = race.id;
    option.textContent = race.name;
    raceSelect.appendChild(option);

    // Filas tabla
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${race.id}</td><td>${race.name}</td><td>${race.description}</td>`;
    racesTableBody.appendChild(tr);
  });

  const classSelect = document.getElementById('class-select');
  const classesTableBody = document.querySelector('#classes-table tbody');

  classes.forEach(cls => {
    // Opciones select
    const option = document.createElement('option');
    option.value = cls.id;
    option.textContent = cls.name;
    classSelect.appendChild(option);

    // Filas tabla
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${cls.id}</td><td>${cls.name}</td><td>${cls.description}</td>`;
    classesTableBody.appendChild(tr);
  });
}

//document.addEventListener('DOMContentLoaded', fillSelectAndTable);

document.querySelectorAll('.open-form-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const formKey = btn.getAttribute('data-form');
        const formHtml = formTemplates[formKey];
        if (formHtml) {
            document.getElementById('form-container').innerHTML = formHtml;
            document.getElementById('pop-form').classList.remove('hidden');
        }
    });
});

document.getElementById('close-pop-form').addEventListener('click', () => {
    document.getElementById('pop-form').classList.add('hidden');
});

// Listener genérico para enviar formularios por AJAX
document.addEventListener('submit', async function (e) {
    if (e.target.matches('form')) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch('/api/' + e.target.id, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            alert(result.message || 'Guardado con éxito');
            document.getElementById('pop-form').classList.add('hidden');
        } catch (err) {
            alert('Error al guardar');
            console.error(err);
        }
    }
});