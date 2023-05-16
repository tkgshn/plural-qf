function connectionOrientedClusterMatch(groups, contributions) {
    var agents = Array.from({length: contributions.length}, (_, i) => i);

    var memberships = agents.map(i => groups.filter(g => g.includes(i)).length);

    var friendMatrix = agents.map(i => agents.map(j => groups.filter(g => g.includes(i) && g.includes(j)).length));

    var fundingAmount = contributions.reduce((a, b) => a + b, 0);

    function K(i, h) {
        if (h.some(j => friendMatrix[i][j] > 0)) {
            return Math.sqrt(contributions[i]);
        }
        return contributions[i];
    }

    for (var p = 0; p < groups.length; p++) {
        for (var q = p+1; q < groups.length; q++) {
            fundingAmount += 2 * Math.sqrt(groups[p].reduce((total, i) => total + K(i, groups[q]) / memberships[i], 0)) * Math.sqrt(groups[q].reduce((total, j) => total + K(j, groups[p]) / memberships[j], 0));
        }
    }

    return fundingAmount;
}

function calculate() {
    var contributions = [];
    for (var i = 0; i < 7; i++) {
        var slider = document.getElementById("agent" + i);
        contributions[i] = Number(slider.value);
    }

    var groups = [[0],[1,2],[2,3,4,5],[5,6]];
    var result = connectionOrientedClusterMatch(groups, contributions);

    document.getElementById("result").innerHTML = "Result: $" + result.toFixed(2);
}

var sliders = document.getElementsByClassName("slider");
for (var i = 0; i < sliders.length; i++) {
    sliders[i].oninput = function() {
        document.getElementById("value" + this.id.slice(-1)).innerHTML = this.value;
    }
}
