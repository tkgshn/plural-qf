
var button1 = document.getElementById("button1");
button1.innerHTML = "Agent 1: $" + agentContributions.agent1;

var button2 = document.getElementById("button2");
button2.innerHTML = "Agent 2: $" + agentContributions.agent2;

// Update the button text when agent contributions change
function updateButton() {
  button2.innerHTML = "Agent 2: $" + agentContributions.agent2;
}


function calculate() {
  var contributions = [];
  for (var i = 0; i < 7; i++) {
    var slider = document.getElementById("agent" + i);
    contributions[i] = Number(slider.value);
  }

  // The Plural QF calculation goes here.
  // You will need to convert the Python code to JavaScript.
  var result = pluralQF(contributions);

  // Display the result.
  document.getElementById("result").innerHTML = "Project B: $" + result.projectB.toFixed(2) + ", Project C: $" + result.projectC.toFixed(2);
}

function pluralQF(contributions) {
  // Convert the Python code to JavaScript and implement the calculation here.
  // This is a placeholder for the actual calculation.
  return {projectB: 0, projectC: 0};
}

// Update the current slider value (each time you drag the slider handle)
var sliders = document.getElementsByClassName("slider");
for (var i = 0; i < sliders.length; i++) {
  sliders[i].oninput = function() {
    document.getElementById("value" + this.id.slice(-1)).innerHTML = this.value;
  }
}

