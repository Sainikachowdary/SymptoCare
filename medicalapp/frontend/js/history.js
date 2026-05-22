const historyData = JSON.parse(localStorage.getItem("history")) || [];

const container = document.getElementById("historyContainer");

if (historyData.length === 0) {
  container.innerHTML = `

<div class="card">

<h2>No history found</h2>

</div>

`;
} else {
  historyData.reverse().forEach((item) => {
    container.innerHTML += `

<div class="card">

<h2>
Disease:
${item.disease}
</h2>

<p>
Symptoms:
${item.symptoms}
</p>

<p>
Confidence:
${item.confidence}%
</p>

<p>
Date:
${item.date}
</p>

</div>

`;
  });
}
