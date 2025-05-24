// Elenco delle immagini (puoi espanderlo con tutte le tue URL da GitHub)
const wallpapers = [
  "https://github.com/il-tuo-username/wallpapers/blob/main/wallpaper1.jpg?raw=true ",
  "https://github.com/il-tuo-username/wallpapers/blob/main/wallpaper2.jpg?raw=true ",
  "https://github.com/il-tuo-username/wallpapers/blob/main/wallpaper3.jpg?raw=true ",
  "https://github.com/il-tuo-username/wallpapers/blob/main/wallpaper4.jpg?raw=true ",
  // Aggiungi altre immagini
];

// Funzione per generare la griglia
function generateWallpapers() {
  const grid = document.getElementById("wallpaper-grid");

  wallpapers.forEach(url => {
    const col = document.createElement("div");
    col.className = "col-md-4 mb-4";

    const card = document.createElement("div");
    card.className = "card wallpaper-card shadow-sm";

    const img = document.createElement("img");
    img.src = url;
    img.alt = "Wallpaper";
    img.loading = "lazy";

    const cardBody = document.createElement("div");
    cardBody.className = "card-body text-center";

    const downloadBtn = document.createElement("a");
    downloadBtn.href = url;
    downloadBtn.download = "";
    downloadBtn.className = "btn btn-primary btn-sm";
    downloadBtn.textContent = "Scarica";

    cardBody.appendChild(downloadBtn);
    card.appendChild(img);
    card.appendChild(cardBody);
    col.appendChild(card);
    grid.appendChild(col);
  });
}

window.onload = generateWallpapers;
