import { getMesh } from "./api.js";
import { computeCellCenter, normalize, clamp, lerp } from "./utils.js";
import {
  addIdToSelection,
  clearSelection,
  deleteIdFromSelection,
  isInSelection,
} from "./storage.js";

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const frozen_map = {
  frozen_color: [255, 255, 255], //blanc
  non_frozen_color: [0, 0, 0], //noir
};

const thermal_map = {
  min: -200,
  max: 50,
  palette: [
    { stop: 0.0, color: [0, 0, 255] }, // bleu
    { stop: 0.25, color: [0, 255, 255] }, // cyan
    { stop: 0.5, color: [0, 255, 0] }, // vert
    { stop: 0.75, color: [255, 255, 0] }, // jaune
    { stop: 1.0, color: [255, 0, 0] }, // rouge
  ],
};

const vapor_map = {
  min: 0,
  max: 100,
  palette: [
    { stop: 0.0, color: [200, 200, 255] }, // bleu pâle
    { stop: 0.5, color: [150, 255, 255] }, // cyan
    { stop: 1.0, color: [255, 255, 200] }, // jaune clair
  ],
};

const ice_potential_map = {
  min: 0,
  max: 100,
  palette: [
    { stop: 0.0, color: [0, 0, 128] }, // bleu foncé
    { stop: 0.5, color: [0, 128, 255] }, // bleu clair
    { stop: 1.0, color: [255, 255, 255] }, // blanc glace
  ],
};

export async function initCanvas() {
  canvas.width = window.innerWidth - 250;
  canvas.height = window.innerHeight;
  const mesh = await getMesh();
  drawMesh(mesh);
  canvas.addEventListener("click", handleClick);
  window.addEventListener("resize", () => {
    resizeCanvas();
    drawMesh(mesh);
  });
}

function resizeCanvas() {
  const ratio = window.devicePixelRatio || 1;
  const width = window.innerWidth - 250;
  const height = window.innerHeight;

  canvas.width = width * ratio;
  canvas.height = height * ratio;

  canvas.style.width = width + "px";
  canvas.style.height = height + "px";

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(ratio, ratio);
}

export function drawCell(
  cell,
  center_x,
  center_y,
  side_length,
  selected = false,
) {
  const angle = Math.PI / 3;
  ctx.beginPath();
  for (let i = 0; i < 6; i++) {
    ctx.lineTo(
      center_x + side_length * Math.cos(angle * i + Math.PI / 6),
      center_y + side_length * Math.sin(angle * i + Math.PI / 6),
    );
  }
  ctx.closePath();
  ctx.fillStyle = getCellColor(cell);
  ctx.fill();

  ctx.strokeStyle = selected ? "yellow" : "#000";
  ctx.lineWidth = selected ? 3 : 1;
  ctx.stroke();
}

export function drawMesh(mesh) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawColorBar();
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;

  const minDim = Math.min(width, height);
  const canvas_center_x = width / 2;
  const canvas_center_y = height / 2;

  const radiusMesh = (0.45 * minDim) / (mesh.size + 1 / Math.sqrt(3));
  const side_length = radiusMesh / Math.sqrt(3);

  mesh.cells.forEach((cell) => {
    let center_x, center_y;
    [center_x, center_y] = computeCellCenter(
      cell.id,
      canvas_center_x,
      canvas_center_y,
      radiusMesh,
    );
    const selected = isInSelection(cell.id);
    drawCell(cell, center_x, center_y, side_length, selected);
  });
}

export function drawColorBar() {
  const displayMode = document.getElementById("displayMode").value;
  let displayMap;
  const legendWidth = 20;
  const legendHeight = 150;
  const padding = 50;

  const x = canvas.clientWidth - legendWidth - padding;
  const y = canvas.clientHeight - legendHeight - padding;

  if (displayMode === "frozen") {
    drawLegendFrozen();
    return;
  }
  if (displayMode === "temperature") displayMap = thermal_map;
  if (displayMode === "vapor") displayMap = vapor_map;
  if (displayMode === "icePotential") displayMap = ice_potential_map;

  const gradient = ctx.createLinearGradient(0, y + legendHeight, 0, y);
  for (let i = 0; i < displayMap.palette.length; i++) {
    gradient.addColorStop(
      displayMap.palette[i].stop,
      alterColor(displayMap.palette[i].color),
    );
  }
  ctx.fillStyle = gradient;
  ctx.fillRect(x, y, legendWidth, legendHeight);

  ctx.strokeStyle = "white";
  // ctx.strokeRect(x, y, legendWidth, legendHeight);

  // 4️⃣ Labels
  ctx.fillStyle = "white";
  ctx.font = "12px Arial";
  ctx.textAlign = "left";

  ctx.fillText(displayMap.max, x + legendWidth + 5, y + 10);
  ctx.fillText(displayMap.min, x + legendWidth + 5, y + legendHeight);
}

function drawLegendFrozen() {
  // Coordonnées et taille

  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const squareSize = 20;
  const padding_x = width / 10;
  const padding_y = height / 10;
  const x = width - padding_x;
  const y = height - padding_y;

  // Couleurs
  const colorMin = alterColor(frozen_map.frozen_color);
  const colorMax = alterColor(frozen_map.non_frozen_color);

  // 1️⃣ Carré couleur min
  ctx.fillStyle = colorMin;
  ctx.fillRect(x, y, squareSize, squareSize);

  // 2️⃣ Carré couleur max
  ctx.fillStyle = colorMax;
  ctx.fillRect(x, y + 2 * squareSize, squareSize, squareSize);
  // 3️⃣ Labels
  ctx.fillStyle = "white";
  ctx.font = "12px Arial";
  ctx.textAlign = "left";

  ctx.fillText("Gelé", x + squareSize + 5, y + squareSize / 2);
  ctx.fillText("Non gelé", x + squareSize + 5, y + 2.5 * squareSize);
}

function getCellColor(cell) {
  const displayMode = document.getElementById("displayMode").value;
  let displayMap;
  let value;
  if (displayMode === "frozen") {
    return cell.frozen
      ? alterColor(frozen_map.frozen_color)
      : alterColor(frozen_map.non_frozen_color);
  }
  if (displayMode === "temperature") {
    displayMap = thermal_map;
    value = cell.temperature;
  }
  if (displayMode === "vapor") {
    displayMap = vapor_map;
    value = cell.vapor;
  }
  if (displayMode === "icePotential") {
    displayMap = ice_potential_map;
    value = cell.ice_potential;
  }

  const color = valueToColor(
    value,
    displayMap.min,
    displayMap.max,
    displayMap.palette,
  );
  return color;
}

function valueToColor(value, minValue, maxValue, palette) {
  let t = normalize(value, minValue, maxValue);
  t = clamp(t, 0, 1);

  for (let i = 0; i < palette.length - 1; i++) {
    let left = palette[i];
    let right = palette[i + 1];
    if (t >= left.stop && t <= right.stop) {
      let localT = (t - left.stop) / (right.stop - left.stop);
      let r = Math.round(lerp(left.color[0], right.color[0], localT));
      let g = Math.round(lerp(left.color[1], right.color[1], localT));
      let b = Math.round(lerp(left.color[2], right.color[2], localT));
      return `rgb(${r},${g},${b})`;
    }
  }
}

export async function handleClick(e) {
  const mesh = await getMesh();
  const rect = canvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  const width = canvas.clientWidth;
  const height = canvas.clientHeight;

  const minDim = Math.min(width, height);
  const radiusMesh = (0.45 * minDim) / (mesh.size + 1 / Math.sqrt(3));
  const side_length = radiusMesh / Math.sqrt(3);
  const center_canvas_x = width / 2;
  const center_canvas_y = height / 2;

  mesh.cells.forEach((cell) => {
    let center_x, center_y;
    [center_x, center_y] = computeCellCenter(
      cell.id,
      center_canvas_x,
      center_canvas_y,
      radiusMesh,
    );

    const dx = mouseX - center_x;
    const dy = mouseY - center_y;

    // Test dans le cercle inscrit (approximation suffisante)
    if (Math.sqrt(dx * dx + dy * dy) < side_length) {
      if (e.shiftKey) {
        // multi-selection
        if (isInSelection(cell.id)) {
          deleteIdFromSelection(cell.id);
        } else {
          addIdToSelection(cell.id);
        }
      } else {
        // sélection simple
        if (isInSelection(cell.id)) {
          deleteIdFromSelection(cell.id);
        } else {
          addIdToSelection(cell.id);
        }
      }
      drawMesh(mesh);
    }
  });
}
function alterColor(color) {
  return `rgb(${color[0]},${color[1]},${color[2]})`;
}
