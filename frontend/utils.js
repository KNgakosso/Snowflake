export function computeCellCenter(id, canvas_center_x, canvas_center_y, radiusMesh) {
    const [r, i] = id;
    let center_x, center_y;
    if (r === 0) {
            center_x = canvas_center_x;
            center_y = canvas_center_y;
        } else {
            const alpha_0 = - Math.PI/3 * (Math.floor(i/r)-1);
            const x_0 = canvas_center_x + r * radiusMesh * Math.cos(alpha_0);
            const y_0 = canvas_center_y + r * radiusMesh * Math.sin(alpha_0);
            
            const alpha_1 = - Math.PI/3 * Math.floor(i/r); 
            const x_1 = canvas_center_x + r * radiusMesh * Math.cos(alpha_1);
            const y_1 = canvas_center_y + r * radiusMesh * Math.sin(alpha_1); 
            const t = (i % r) / r;
            
            center_x = (1 - t)  * x_0 + t * x_1;
            center_y = (1 - t)  * y_0 + t * y_1;
        }
    return [center_x, center_y];
}

export function temperatureToColor(temp, tempMin, tempMax) {
  let t = normalize(temp, tempMin, tempMax);
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

export function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

export function normalize(temp, min, max) {
  return (temp - min) / (max - min);
}

export function lerp(a, b, t) {
  return a + (b - a) * t;
}