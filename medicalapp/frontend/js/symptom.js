let symptoms = [];

const allSymptoms = [
  "abdominal_pain",
  "acidity",
  "acute_liver_failure",
  "altered_sensorium",
  "anxiety",
  "back_pain",
  "belly_pain",
  "blackheads",
  "bladder_discomfort",
  "blistering_rash",
  "blood_in_sputum",
  "bloody_stool",
  "blurred_and_distorted_vision",
  "breathlessness",
  "brittle_nails",
  "bruising",
  "burning_micturition",
  "chest_pain",
  "chills",
  "cold_hands_and_feets",
  "coma",
  "congestion",
  "constipation",
  "continuous_feel_of_urine",
  "continuous_sneezing",
  "cough",
  "cramps",
  "dark_urine",
  "dehydration",
  "depression",
  "diarrhoea",
  "dizziness",
  "drying_and_tingling_lips",
  "enlarged_thyroid",
  "excessive_hunger",
  "extra_marital_contacts",
  "family_history",
  "fatigue",
  "fever",
  "fluid_overload",
  "foul_smell_of_urine",
  "headache",
  "high_fever",
  "hip_joint_pain",
  "indigestion",
  "irregular_sugar_level",
  "irritability",
  "itching",
  "joint_pain",
  "knee_pain",
  "lack_of_concentration",
  "lethargy",
  "loss_of_appetite",
  "loss_of_balance",
  "malaise",
  "mild_fever",
  "mood_swings",
  "movement_stiffness",
  "muscle_pain",
  "muscle_wasting",
  "muscle_weakness",
  "nausea",
  "neck_pain",
  "nodal_skin_eruptions",
  "obesity",
  "pain_behind_the_eyes",
  "pain_during_bowel_movements",
  "pain_in_anal_region",
  "painful_walking",
  "palpitations",
  "passage_of_gases",
  "patches_in_throat",
  "phlegm",
  "polyuria",
  "pus_filled_pimples",
  "red_sore_around_nose",
  "red_spots_over_body",
  "restlessness",
  "runny_nose",
  "rusty_sputum",
  "shivering",
  "silver_like_dusting",
  "skin_peeling",
  "skin_rash",
  "slurred_speech",
  "small_dents_in_nails",
  "spinning_movements",
  "spotting_urination",
  "stiff_neck",
  "stomach_pain",
  "sweating",
  "swelled_lymph_nodes",
  "swelling_joints",
  "throat_irritation",
  "toxic_look_typhos",
  "ulcers_on_tongue",
  "vomiting",
  "weakness_in_limbs",
  "weakness_of_one_body_side",
  "weight_gain",
  "weight_loss",
  "yellow_crust_ooze",
  "yellow_urine",
  "yellowing_of_eyes",
  "yellowish_skin",
];

window.onload = function () {
  const list = document.getElementById("symptomSuggestions");

  allSymptoms.forEach((symptom) => {
    const option = document.createElement("option");

    option.value = symptom;

    list.appendChild(option);
  });
};

function addSymptom() {
  const input = document.getElementById("symptomInput");

  const value = input.value.trim();

  if (value === "") {
    alert("Select symptom");

    return;
  }

  if (symptoms.includes(value)) {
    alert("Already added");

    return;
  }

  symptoms.push(value);

  renderSymptoms();

  input.value = "";
}

function renderSymptoms() {
  const div = document.getElementById("symptomList");

  div.innerHTML = "";

  symptoms.forEach((symptom, index) => {
    div.innerHTML += `

<span class="chip">

${symptom}

<button
onclick=
"removeSymptom(${index})"
>

×

</button>

</span>

`;
  });
}

function removeSymptom(index) {
  symptoms.splice(index, 1);

  renderSymptoms();
}

async function checkDisease() {
  if (symptoms.length === 0) {
    alert("Select symptoms first");

    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/ml/predict", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        symptoms: symptoms,
      }),
    });

    const data = await response.json();

    console.log(data);

    /* SAVE HISTORY */

    let history = JSON.parse(localStorage.getItem("history")) || [];

    history.push({
      disease: data.disease,

      symptoms: symptoms.join(", "),

      confidence: data.confidence,

      date: new Date().toLocaleString(),
    });

    localStorage.setItem(
      "history",

      JSON.stringify(history),
    );

    /* PRECAUTIONS */

    let precautionsHTML = "";

    if (data.precautions) {
      data.precautions.forEach((item) => {
        precautionsHTML += `

<div class="precaution-item">

✓ ${item}

</div>

`;
      });
    }

    document.getElementById("result").innerHTML = `

<div class="result-card">

<h2>

Disease:
${data.disease}

</h2>

<p>

Confidence:
${data.confidence}%

</p>

<h3>

📋 Precautions & Recommendations

</h3>

${precautionsHTML}

<div style="
margin-top:20px;
padding:15px;
background:#ffe8e8;
border-left:5px solid red;
border-radius:10px;
">

⚠ Medical Disclaimer:
Always consult a healthcare professional

</div>

</div>

`;
  } catch (error) {
    console.log(error);

    alert("Prediction Failed");
  }
}
