const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const sendBtn = document.getElementById("sendBtn");
const resultsDiv = document.getElementById("results");
const rawTextPre = document.getElementById("rawText");

let selectedFile = null;

fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  resultsDiv.innerHTML = "";
  rawTextPre.textContent = "";
  if (!file) {
    preview.innerHTML = "";
    sendBtn.disabled = true;
    selectedFile = null;
    return;
  }
  selectedFile = file;
  preview.innerHTML = `<img src="${URL.createObjectURL(file)}" alt="Preview" />`;
  sendBtn.disabled = false;
});

sendBtn.addEventListener("click", async () => {
  if (!selectedFile) return;
  sendBtn.disabled = true;
  sendBtn.textContent = "Analyzing...";

  const form = new FormData();
  form.append("image", selectedFile);

  try {
    const resp = await fetch("/api/ocr", { method: "POST", body: form });
    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.error || "Server error");
    }
    const json = await resp.json();
    renderResults(json);
  } catch (err) {
    resultsDiv.innerHTML = `<div class="vital-card"><strong>Error:</strong> ${err.message}</div>`;
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = "Analyze";
  }
});

function renderResults(json) {
  resultsDiv.innerHTML = "";
  rawTextPre.textContent = json.raw_text || "";

  const vitals = json.vitals || {};
  if (Object.keys(vitals).length === 0) {
    resultsDiv.innerHTML = `<div class="vital-card"><p>No vitals detected. Try a clearer image or crop to the table area.</p></div>`;
    return;
  }

  // For each vital, create a card + chart
  Object.entries(vitals).forEach(([name, data], idx) => {
    const card = document.createElement("div");
    card.className = "vital-card";

    const title = document.createElement("div");
    title.className = "vital-title";
    title.innerHTML = `<h3 style="margin:0;">${name}</h3>
                       <div>${data.value}</div>`;

    const text = document.createElement("p");
    text.innerHTML = `<strong>Normal range:</strong> ${data.lower} - ${data.upper}`;

    const analysis = document.createElement("p");
    let analysisText = "";
    if (data.value < data.lower) {
      analysisText = `⚠️ ${name} is below the normal range (${data.lower}-${data.upper})`;
    } else if (data.value > data.upper) {
      analysisText = `⚠️ ${name} is above the normal range (${data.lower}-${data.upper})`;
    } else {
      analysisText = `✅ ${name} is within the normal range (${data.lower}-${data.upper})`;
    }
    analysis.innerHTML = analysisText;

    const canvas = document.createElement("canvas");
    canvas.id = `chart-${idx}`;
    canvas.width = 600;
    canvas.height = 200;

    card.appendChild(title);
    card.appendChild(text);
    card.appendChild(analysis);
    card.appendChild(canvas);
    resultsDiv.appendChild(card);

    // Chart: show lower, value, upper as a small line/bar plot
    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Lower", "Observed", "Upper"],
        datasets: [{
          label: name,
          data: [data.lower, data.value, data.upper],
          // no explicit colors - Chart.js default palette will be used
        }]
      },
      options: {
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: false }
        }
      }
    });
  });
}
