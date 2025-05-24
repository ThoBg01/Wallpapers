// Lista dei wallpaper con categorie
const wallpapers = [
  { url: "https://github.com/il-tuo-username/wallpapers/blob/main/natura1.jpg?raw=true ", category: "natura" },
  { url: "https://github.com/il-tuo-username/wallpapers/blob/main/anime1.jpg?raw=true ", category: "anime" },
  { url: "https://github.com/il-tuo-username/wallpapers/blob/main/citta1.jpg?raw=true ", category: "città" },
  { url: "https://github.com/il-tuo-username/wallpapers/blob/main/natura2.jpg?raw=true ", category: "natura" },
  { url: "https://github.com/il-tuo-username/wallpapers/blob/main/anime2.jpg?raw=true ", category: "anime" },
  { url: "https://github.com/il-tuo-username/wallpapers/blob/main/citta2.jpg?raw=true ", category: "città" },
];

let currentCategory = "tutti";

function generateWallpapers() {
  const grid = document.getElementById("wallpaper-grid");
  grid.innerHTML = "";

  wallpapers.forEach(wallpaper => {
    if (currentCategory === "tutti" || wallpaper.category === currentCategory) {
      const col = document.createElement("div");
      col.className = "col-md-2 col-sm-4 mb-4 wallpaper-card";

      const card = document.createElement("div");
      card.className = "card shadow-sm";

      const img = document.createElement("img");
      img.src = wallpaper.url;
      img.alt = "Wallpaper";
      img.loading = "lazy";

      const cardBody = document.createElement("div");
      cardBody.className = "card-body text-center";

      const downloadBtn = document.createElement("a");
      downloadBtn.href = wallpaper.url;
      downloadBtn.download = "";
      downloadBtn.className = "download-btn btn btn-primary";
      downloadBtn.textContent = "Scarica";

      cardBody.appendChild(downloadBtn);
      card.appendChild(img);
      card.appendChild(cardBody);
      col.appendChild(card);
      grid.appendChild(col);
    }
  });
}

function filterCategory(category) {
  currentCategory = category;
  generateWallpapers();
}

window.onload = generateWallpapers;
