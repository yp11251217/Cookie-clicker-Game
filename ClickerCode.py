import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mini Minecraft", layout="wide")

st.title("⛏️ Mini Minecraft (Streamlit + HTML)")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      background: #1e1e1e;
      font-family: Arial;
    }
    #toolbar {
      padding: 10px;
      background: #333;
      color: white;
    }
    canvas {
      display: block;
      margin: 0 auto;
      background: #87CEEB;
      cursor: pointer;
    }
    button {
      margin-right: 10px;
      padding: 8px;
      cursor: pointer;
    }
  </style>
</head>

<body>

<div id="toolbar">
  <button onclick="setBlock('green')">Grass</button>
  <button onclick="setBlock('saddlebrown')">Dirt</button>
  <button onclick="setBlock('gray')">Stone</button>
  <button onclick="setBlock('skyblue')">Erase</button>
</div>

<canvas id="game" width="600" height="600"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const gridSize = 30;
const rows = canvas.height / gridSize;
const cols = canvas.width / gridSize;

let selectedBlock = "green";

// world grid
let grid = Array.from({ length: rows }, () =>
  Array.from({ length: cols }, () => null)
);

function setBlock(color) {
  selectedBlock = color;
}

function drawGrid() {
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      if (grid[y][x]) {
        ctx.fillStyle = grid[y][x];
        ctx.fillRect(x * gridSize, y * gridSize, gridSize, gridSize);
      } else {
        ctx.fillStyle = "#87CEEB";
        ctx.fillRect(x * gridSize, y * gridSize, gridSize, gridSize);
      }

      ctx.strokeStyle = "rgba(0,0,0,0.1)";
      ctx.strokeRect(x * gridSize, y * gridSize, gridSize, gridSize);
    }
  }
}

canvas.addEventListener("click", (e) => {
  const rect = canvas.getBoundingClientRect();
  const x = Math.floor((e.clientX - rect.left) / gridSize);
  const y = Math.floor((e.clientY - rect.top) / gridSize);

  if (selectedBlock === "skyblue") {
    grid[y][x] = null; // erase
  } else {
    grid[y][x] = selectedBlock;
  }

  drawGrid();
});

drawGrid();
</script>

</body>
</html>
"""

components.html(html_code, height=700)
