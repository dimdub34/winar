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

    //Draw new pair of circles
    ctx.beginPath();
    ctx.arc(distance1, horizontal, radius, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(distance2, horizontal, radius, 0, 2 * Math.PI);
    ctx.stroke();

    //Keep the label in the center of the circle, to not have more overlap
    let headers = multiplier[Math.min(Value - 1, 3)];

    //Write labels into
    ctx.font = "25px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = 'middle';
    ctx.fillText("You", center - ((radius * headers) / 2), horizontal);
    ctx.fillText("Others", center + ((radius * headers) / 2), horizontal);

    //Record variable value
    //Include the variable recording HERE. The currently selected value in the slider is saved in the variable "Value"
    document.querySelector('input[name=ios_value]').value = Value;
}