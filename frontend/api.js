// api.js

const BASE_URL =
  window.location.hostname === "localhost" ? "http://localhost:8000" : "";

// Helper générique pour gérer les requêtes
async function request(url, method = "GET", body = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }
  try {
    const response = await fetch(`${BASE_URL}${url}`, options);
    return await response.json();
  } catch (err) {
    console.log(err);
  }
}

// =====================
// Routes GET
// =====================

export async function readRoot() {
  return await request("/", "GET");
}

export async function getMesh() {
  return await request("/mesh", "GET");
}

export async function getInitializationParams() {
  return await request("/initialization_params", "GET");
}
export async function getSimulationParams() {
  return await request("/simulation_params", "GET");
}

export async function getPhysicalParams() {
  return await request("/physical_params", "GET");
}

// =====================
// Routes PATCH
// =====================

export async function updateInitializationParams(initializationParams) {
  return await request("/initialization_params", "PATCH", initializationParams);
}

export async function updateSimulationParams(simulationParams) {
  return await request("/simulation_params", "PATCH", simulationParams);
}

export async function updatePhysicalParams(physicalParams) {
  return await request("/physical_params", "PATCH", physicalParams);
}

export async function setTemperature(updateSelection) {
  return await request("/temperature", "PATCH", updateSelection);
}

export async function setVapor(updateSelection) {
  return await request("/vapor", "PATCH", updateSelection);
}

export async function setIcePotential(updateSelection) {
  return await request("/ice_potential", "PATCH", updateSelection);
}

export async function setFrozenTrue(selection) {
  return await request("/frozen/true", "PATCH", selection);
}

export async function setFrozenFalse(selection) {
  return await request("/frozen/false", "PATCH", selection);
}

export async function randomize() {
  return await request("/randomize", "PATCH");
}

// =====================
// Route PUT
// =====================

export async function runSimulation() {
  return await request("/simulation", "PUT");
}
