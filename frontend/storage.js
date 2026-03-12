const selectedCells = new Set();

export function getSelection() {
    if(selectedCells.size === 0) return null;
    return Array.from(selectedCells).map(k => k.split(",").map(Number));
}

export function addIdToSelection(id) {
    const key = `${id[0]},${id[1]}`;
    selectedCells.add(key);
}

export function deleteIdFromSelection(id) {
    const key = `${id[0]},${id[1]}`;
    selectedCells.delete(key);
}

export function isInSelection(id) {
    const key = `${id[0]},${id[1]}`;
    return selectedCells.has(key);
}

export function clearSelection() {
    selectedCells.clear();
}