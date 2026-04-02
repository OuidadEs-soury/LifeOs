const card = document.querySelector(".chart-card")

const productivity = parseInt(card.dataset.productivity)

const ctx = document.getElementById("chart")

new Chart(ctx, {

type: "doughnut",

data: {

labels: ["Completed", "Remaining"],

datasets: [{

data: [productivity, 100 - productivity],

backgroundColor: [

"#00f5ff",

"#1f2937"

],

borderWidth: 0

}]

},

options: {

responsive: true,

cutout: "70%",

animation: {

animateScale: true,

animateRotate: true

},

plugins: {

legend: {

labels: {

color: "#ffffff"

}

}

}

}

})