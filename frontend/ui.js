import { getMesh, getInitializationParams, getPhysicalParams, getSimulationParams } from "./api.js";
import { updateInitializationParamsClick, updateSimulationParamsClick, runSimulationClick, randomizeClick, setFrozenClick, setIcePotentialClick, setTemperatureClick, setVaporClick, unsetFrozenClick, changeDisplayMode, updatePhysicalParamsClick } from "./event.js";

export function initInterface() {
    const updtInitParamsBtn = document.getElementById("updateInitParams");
    const updtPhysParamsBtn = document.getElementById("updatePhysParams");
    const updtSimulParamsBtn = document.getElementById("updateSimulParams");
    const runBtn = document.getElementById("runBtn");
    const randBtn = document.getElementById("randBtn");
    const tempBtn = document.getElementById("applyTemp");
    const iceBtn = document.getElementById("applyIce");
    const vaporBtn = document.getElementById("applyVapor");
    const freezeTrueBtn = document.getElementById("setFrozen");
    const freezeFalseBtn = document.getElementById("unsetFrozen");
    const displayModeSelect = document.getElementById("displayMode");

    updtInitParamsBtn.addEventListener("click", updateInitializationParamsClick);
    updtPhysParamsBtn.addEventListener("click", updatePhysicalParamsClick);
    updtSimulParamsBtn.addEventListener("click", updateSimulationParamsClick);
    runBtn.addEventListener("click", runSimulationClick);
    randBtn.addEventListener("click", randomizeClick);
    tempBtn.addEventListener("click", setTemperatureClick);
    iceBtn.addEventListener("click", setIcePotentialClick);
    vaporBtn.addEventListener("click", setVaporClick);
    freezeTrueBtn.addEventListener("click", setFrozenClick);
    freezeFalseBtn.addEventListener("click", unsetFrozenClick);
    displayModeSelect.addEventListener("change", changeDisplayMode);
}

export async function initDefaultVaules() {
    const initializationParams = await getInitializationParams();
    const simulationParams = await getSimulationParams();
    const physicalParams = await getPhysicalParams();

    document.getElementById("size").value = initializationParams.size;
    document.getElementById("iterations").value = simulationParams.iterations;
    document.getElementById("alphaTemp").value = physicalParams.alpha_temperature;
    document.getElementById("alphaVapor").value = physicalParams.alpha_vapor;
    document.getElementById("betaVapor").value = physicalParams.beta_vapor;
    document.getElementById("alphaCond").value = physicalParams.alpha_condensation;
    document.getElementById("vapSat").value = physicalParams.vapor_saturation;
    document.getElementById("iceThresh").value = physicalParams.ice_threshold;
    document.getElementById("tempThresh").value = physicalParams.temperature_threshold;
    document.getElementById("nFrozenNeigh").value = physicalParams.n_frozen_neighbors_threshold;
}