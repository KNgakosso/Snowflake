window.addEventListener("beforeunload", () => {
    console.log("PAGE RELOAD");
});

// app.js
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth - 250;
canvas.height = window.innerHeight;

let mesh = null;
let displayMode = "frozen";
const selectedCells = new Set();
const API = "http://localhost:8000";

let currentMin = 0;
let currentMax = 1;

// ==========================
// FETCH ET SIMULATION
// ==========================
async function fetchMesh() {
    console.log("fecthMesh", displayMode)
    const res = await fetch(`${API}/mesh`);
    mesh = await res.json();
    drawMesh();
}

async function runSimulation() {
    await fetch(`${API}/simulation`, { method: "PUT" });
    await fetchMesh();
}


async function updateParams() {
    const size = parseInt(document.getElementById("size").value);
    const iterations = parseInt(document.getElementById("iterations").value);

    await fetch(`${API}/simulation_params`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            size: size,
            iterations: iterations,
            color: [255, 255, 255]
        })
    });

    await fetchMesh();
}

// ################################################
// BORNES DYNAMIQUES
// ################################################
function computeMinMax() {
    if(displayMode === "frozen") return;

    const values = mesh.cells.map(cell => {
        if(displayMode === "temperature") return cell.temperature;
        if(displayMode === "vapor") return cell.vapor;
        if(displayMode === "ice_potential") return cell.ice_potential;
    });

    currentMin = Math.min(...values);
    currentMax = Math.max(...values);

    if(currentMin === currentMax) {
        currentMax = currentMin + 1e-9;
    }
}

// ################################################
// COLOR
// ################################################
function getColorFromValue(mode, value) {

    if(mode === "frozen") {
        return value ? "white" : "black";
    }

    const v = (value - currentMin) / (currentMax - currentMin);
    const clamped = Math.min(Math.max(v, 0), 1);

    if(mode === "temperature") {
        // bleu → rouge
        const r = 255 * clamped;
        const b = 255 * (1 - clamped);
        return `rgb(${r},0,${b})`;
    }

    if(mode === "vapor") {
        // noir → bleu
        const b = 255 * clamped;
        return `rgb(0,0,${b})`;
    }

    if(mode === "ice_potential") {
        // vert → jaune
        const r = 255 * clamped;
        const g = 255;
        return `rgb(${r},${g},0)`;
    }

    return "#222";
}

// ################################################
// COLORBAR
// ################################################
function drawColorBar() {

    const bar = document.getElementById("colorBar");
    const ctxBar = bar.getContext("2d");

    ctxBar.clearRect(0, 0, bar.width, bar.height);

    if(displayMode === "frozen") {

        ctxBar.fillStyle = "black";
        ctxBar.fillRect(0, 0, bar.width, bar.height/2);

        ctxBar.fillStyle = "white";
        ctxBar.fillRect(0, bar.height/2, bar.width, bar.height/2);

        document.getElementById("colorMin").innerText = "False";
        document.getElementById("colorMax").innerText = "True";

        return;
    }

    const gradient = ctxBar.createLinearGradient(0, 0, 0, bar.height);

    for(let i = 0; i <= 100; i++) {
        const value = currentMin + (currentMax - currentMin) * (i/100);
        gradient.addColorStop(
            1 - i/100,
            getColorFromValue(displayMode, value)
        );
    }

    ctxBar.fillStyle = gradient;
    ctxBar.fillRect(0, 0, bar.width, bar.height);

    document.getElementById("colorMin").innerText = currentMin.toFixed(3);
    document.getElementById("colorMax").innerText = currentMax.toFixed(3);
}

// ==========================
// DESSIN HEXAGONES
// ==========================
function drawHex(x, y, side_length, color, selected=false) {
    const angle = Math.PI / 3;
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
        ctx.lineTo(
            x + side_length * Math.cos(angle * i + Math.PI / 6),
            y + side_length * Math.sin(angle * i + Math.PI / 6)
        );
    }
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    
    ctx.strokeStyle = selected ? "yellow" : "#000";
    ctx.lineWidth = selected ? 2 : 1;
    ctx.stroke();
}

function drawMesh() {
    if (!mesh) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const minDim = Math.min(canvas.width, canvas.height);
    const radiusHex = (0.45 * minDim) / (mesh.size + 1 / Math.sqrt(3));
    const side_length = radiusHex / Math.sqrt(3);

    const center_x = canvas.width / 2;
    const center_y = canvas.height / 2;

    computeMinMax();

    mesh.cells.forEach(cell => {
        let x, y;
        const [r, i] = cell.id;

        if (r === 0) {
            x = center_x;
            y = center_y;
        } else {
            const alpha_0 = Math.PI/3 * Math.floor(i/r);
            const x_0 = center_x + r * radiusHex * Math.cos(alpha_0);
            const y_0 = center_y + r * radiusHex * Math.sin(alpha_0);
            
            const alpha_1 = Math.PI/3 * (Math.floor(i/r)+1); 
            const x_1 = center_x + r * radiusHex * Math.cos(alpha_1);
            const y_1 = center_y + r * radiusHex * Math.sin(alpha_1); 
            const t = (i % r) / r;
            
            x = t * x_0 + (1 - t) * x_1;
            y = t * y_0 + (1 - t) * y_1;
        }

        let value;
        if(displayMode === "frozen") value = cell.frozen;
        if(displayMode === "temperature") value = cell.temperature;
        if(displayMode === "vapor") value = cell.vapor;
        if(displayMode === "ice_potential") value = cell.ice_potential;

        const color = getColorFromValue(displayMode, value);
        const selected = selectedCells.has(`${r},${i}`);
        drawHex(x, y, side_length, color, selected);
    });

    drawColorBar();
}

// ==========================
// GESTION SELECTION CELLS
// ==========================
canvas.addEventListener("click", handleClick);

function handleClick(e) {
    if(!mesh) return;

    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const minDim = Math.min(canvas.width, canvas.height);
    const radiusHex = (0.45 * minDim) / (mesh.size + 1 / Math.sqrt(3));
    const side_length = radiusHex / Math.sqrt(3);
    const center_x = canvas.width / 2;
    const center_y = canvas.height / 2;

    mesh.cells.forEach(cell => {

        let x, y;
        const [r,i] = cell.id;

        if(r === 0) {
            x = center_x;
            y = center_y;
        } else {
            const alpha_0 = Math.PI/3 * Math.floor(i/r);
            const x_0 = center_x + r * radiusHex * Math.cos(alpha_0);
            const y_0 = center_y + r * radiusHex * Math.sin(alpha_0);

            const alpha_1 = Math.PI/3 * (Math.floor(i/r)+1);
            const x_1 = center_x + r * radiusHex * Math.cos(alpha_1);
            const y_1 = center_y + r * radiusHex * Math.sin(alpha_1);

            const t = (i % r)/r;

            x = t*x_0 + (1-t)*x_1;
            y = t*y_0 + (1-t)*y_1;
        }

        const dx = mouseX - x;
        const dy = mouseY - y;

        // Test dans le cercle inscrit (approximation suffisante)
        if(Math.sqrt(dx*dx + dy*dy) < side_length) {

            const key = `${r},${i}`;

            if(e.shiftKey) {
                // multi-selection
                if(selectedCells.has(key)) {
                    selectedCells.delete(key);
                } else {
                    selectedCells.add(key);
                }
            } else {
                // sélection simple
                selectedCells.clear();
                selectedCells.add(key);
            }

            drawMesh();
        }
    });
}

// ==========================
// PATCH ATTRIBUTS
// ==========================
function getSelectionPayload() {
    if(selectedCells.size === 0) return null;
    return Array.from(selectedCells).map(k => k.split(",").map(Number));
}

async function setCellAttr(attr, value) {
    let url = "";
    let payload = null;

    switch(attr) {
        case "temperature":
            url = "/temperature";
            payload = { value: value, set_cells_id: getSelectionPayload() };
            break;
        case "vapor":
            url = "/vapor";
            payload = { value: value, set_cells_id: getSelectionPayload() };
            break;
        case "ice_potential":
            url = "/ice_potential";
            payload = { value: value, set_cells_id: getSelectionPayload() };
            break;
        case "frozen":
            url = value ? "/frozen/true" : "/frozen/false";
            payload = { set_cells_id: getSelectionPayload() || [] };
            break;
        default:
            return;
    }

    await fetch(`${API}${url}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    await fetchMesh();
}

// ==========================
// EVENTS
// ==========================
document.getElementById("runBtn").onclick = runSimulation;
document.getElementById("updateParams").onclick = updateParams;

document.getElementById("displayMode").onchange = (e) => {
    displayMode = e.target.value;
    drawMesh();
};

document.getElementById("applyTemp").addEventListener("click", (e) => {
    e.preventDefault();
    setCellAttr('temperature', parseFloat(document.getElementById('tempValue').value))
        .catch(err => console.error(err));
});

document.getElementById("applyVapor").addEventListener("click", (e) => {
    e.preventDefault();
    setCellAttr('vapor', parseFloat(document.getElementById('vaporValue').value))
        .catch(err => console.error(err));
});

document.getElementById("applyIce").addEventListener("click", (e) => {
    e.preventDefault();
    setCellAttr('ice_potential', parseFloat(document.getElementById('iceValue').value))
        .catch(err => console.error(err));
});

document.getElementById("setFrozen").addEventListener("click", (e) => {
    e.preventDefault();
    setCellAttr('frozen', true).catch(err => console.error(err));
});

document.getElementById("unsetFrozen").addEventListener("click", (e) => {
    e.preventDefault();
    setCellAttr('frozen', false).catch(err => console.error(err));
});

// ==========================
// INIT
// ==========================
fetchMesh();