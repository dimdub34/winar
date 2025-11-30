//Specify circle values relative to canvas size (here: 400x180)

const canvas = document.getElementById("IOSscreen");
const center = 200;
const horizontal = 90;
const radius = 70;

//Distances between centers in task, where 2.15 means 2.15*radius. Thus, circles are fully separated
const multiplier = [2.15, 1.89, 1.64, 1.45, 1.27, 0.91, 0.73, 0.58, 0.44, 0.33, 0.22]

//function change is executed every time the slider is moved (see html)
function change() {
    const c = document.getElementById("IOSscreen");
    const ctx = c.getContext("2d");

    //initiate value that is not defined to have screen initially empty
    let Value = -1;

    //Get value selected in slider
    let Input = document.querySelector("#Input");
    Value = Input.value;

    let distance1 = center - ((radius * multiplier[Value - 1]) / 2);
    let distance2 = center + ((radius * multiplier[Value - 1]) / 2);

    //Update canvas

    //Empty current canvas
    ctx.clearRect(0, 0, c.width, c.height);
    ctx.lineWidth = 3;

    //Draw new pair of circles
    ctx.beginPath();
    ctx.arc(distance1, horizontal, radius, 0, 2 * Math.PI);
    // Remplissage bleu avec 50% d'opacité
    ctx.fillStyle = "rgba(59, 130, 246, 0.5)";
    ctx.fill();
    // Bordure bleue solide
    ctx.strokeStyle = "rgba(29, 78, 216, 1)";
    ctx.stroke();

    // cercle de droite
    ctx.beginPath();
    ctx.arc(distance2, horizontal, radius, 0, 2 * Math.PI);
    // Remplissage orange avec 50% d'opacité
    ctx.fillStyle = "rgba(245, 158, 11, 0.5)";
    ctx.fill();
    // Bordure orange solide
    ctx.strokeStyle = "rgba(180, 83, 9, 1)";
    ctx.stroke();

    //Keep the label in the center of the circle, to not have more overlap
    let headers = multiplier[Math.min(Value - 1, 3)];

    //Write labels into
    let you = "You";
    let others = "Others";
    if (js_vars.fr) {
        you = "Vous";
        others = "Autres";
    }
    ctx.font = "bold 24px 'Helvetica Neue', Helvetica, Arial, sans-serif";
    ctx.fillStyle = "#1f2937"; // Gris très foncé (presque noir) pour le texte
    // Ombre portée blanche sous le texte pour garantir la lisibilité si superposition
    ctx.shadowColor = "white";
    ctx.shadowBlur = 4;

    ctx.textAlign = "center";
    ctx.textBaseline = 'middle';
    ctx.fillText(you, center - ((radius * headers) / 2), horizontal);
    ctx.fillText(others, center + ((radius * headers) / 2), horizontal);

    // Reset shadow pour les prochains dessins (important !)
    ctx.shadowColor = "transparent";
    ctx.shadowBlur = 0;
    //Record variable value
    //Include the variable recording HERE. The currently selected value in the slider is saved in the variable "Value"
    document.querySelector('input[name=ios_value]').value = Value;

    // --- MODIFICATION : Remplissage dynamique du slider ---
    // Calcul du pourcentage (Min = 1, Max = 11, donc plage de 10)
    const min = 1;
    const max = 11;
    // (Value - min) / (max - min) * 100
    const percent = ((Value - min) / (max - min)) * 100;

    // Mise à jour du dégradé : Bleu jusqu'au curseur, Gris ensuite
    Input.style.background = `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${percent}%, #e5e7eb ${percent}%, #e5e7eb 100%)`;
}