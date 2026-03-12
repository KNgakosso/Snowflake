import { getMesh, runSimulation, randomize, setFrozenFalse, setFrozenTrue, setIcePotential, setTemperature, setVapor, updateInitializationParams, updatePhysicalParams, updateSimulationParams } from "./api.js";
import { drawColorBar, drawMesh } from "./display.js";
import { getSelection } from "./storage.js";

export async function updateInitializationParamsClick(e) {
    e.preventDefault();
    const size = parseInt(document.getElementById("size").value);

    await updateInitializationParams({ size });
    const mesh = await getMesh();
    drawMesh(mesh);

}export async function updateSimulationParamsClick(e) {
    e.preventDefault();
    const iterations = parseInt(document.getElementById("iterations").value);

    updateSimulationParams({ iterations });
}

export async function updatePhysicalParamsClick(e) {
    e.preventDefault();
    const alphaTemp = parseFloat(document.getElementById("alphaTemp").value);
    const alphaVapor = parseFloat(document.getElementById("alphaVapor").value);
    const betaVapor = parseFloat(document.getElementById("betaVapor").value);
    const alphaCond = parseFloat(document.getElementById("alphaCond").value);
    const vapSat = parseFloat(document.getElementById("vapSat").value);
    const iceThresh = parseFloat(document.getElementById("iceThresh").value);
    const tempThresh = parseFloat(document.getElementById("tempThresh").value);
    const nFrozenNeigh = parseInt(document.getElementById("nFrozenNeigh").value);

    updatePhysicalParams({
        alpha_temperature : alphaTemp,
        alpha_vapor : alphaVapor,
        beta_vapor : betaVapor,
        alpha_condensation : alphaCond,
        vapor_saturation : vapSat,
        ice_threshold : iceThresh, 
        temperature_threshold : tempThresh,
        n_frozen_neighbors_threshold : nFrozenNeigh
        }
    )
}

export async function runSimulationClick(e) {
    const loading = document.getElementById("loading");

    e.preventDefault();
    // afficher le loading
    loading.style.display = "block";
    runBtn.disabled = true;
    const loopIterations = parseInt(document.getElementById("loop").value);
    // laisser le navigateur afficher le loader
    await new Promise(resolve => setTimeout(resolve, 50));

    for (let i = 0; i < loopIterations; i++) {
        await runSimulation();
        const mesh = await getMesh();
        drawMesh(mesh);
    }
    // cacher le loading
    loading.style.display = "none";
    runBtn.disabled = false;
}

export async function randomizeClick(e) {
    e.preventDefault();
    await randomize();
    const mesh = await getMesh();
    drawMesh(mesh);
}

export async function setTemperatureClick(e) {
    e.preventDefault();
    const value = document.getElementById('tempValue').value;
    const set_cells_id = getSelection()
    await setTemperature({ value, set_cells_id });
    const mesh = await getMesh();
    drawMesh(mesh);
}

export async function setVaporClick(e) {
    e.preventDefault();
    const value = document.getElementById('vaporValue').value;
    const set_cells_id = getSelection()
    await setVapor({ value, set_cells_id });
    const mesh = await getMesh();
    drawMesh(mesh);
}

export async function setIcePotentialClick(e) {
    e.preventDefault();
    const value = document.getElementById('iceValue').value;
    const set_cells_id = getSelection()
    await setIcePotential({ value, set_cells_id });
    const mesh = await getMesh();
    drawMesh(mesh);
}

export async function setFrozenClick(e) {
    e.preventDefault();
    const value = document.getElementById('setFrozen').value;
    const set_cells_id = getSelection()
    await setFrozenTrue({ value, set_cells_id});
    const mesh = await getMesh();
    drawMesh(mesh);
}

export async function unsetFrozenClick(e) {
    e.preventDefault();
    const value = document.getElementById('unsetFrozen').value;
    const set_cells_id = getSelection()
    await setFrozenFalse({value, set_cells_id});
    const mesh = await getMesh();
    drawMesh(mesh);
}

export async function changeDisplayMode(e) {
    e.preventDefault();
    const mesh = await getMesh();
    drawMesh(mesh);
}