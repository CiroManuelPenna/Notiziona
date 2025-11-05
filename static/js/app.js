document.addEventListener("DOMContentLoaded", () => {
  const FAVORITES_KEY = "favorites";
  const favorites = new Set(JSON.parse(localStorage.getItem(FAVORITES_KEY)) || []);

  document.querySelectorAll(".fav_button").forEach(button => {
    const url = button.dataset.url;
    if (favorites.has(url)) {
        button.classList.add("active");
        button.innerHTML = "In your favourites"
    }

    button.addEventListener("click", (event) => {
        event.stopPropagation(); // prevents click from propagating to parent elements
        event.preventDefault();  // prevents the <a> link from triggering when click the "Add to Favorites" button
        if (favorites.has(url)) {
            favorites.delete(url);
            button.classList.remove("active");
            button.innerHTML = "★ Add to Favorites";
        } else {
            favorites.add(url);
            button.classList.add("active");
            button.innerHTML = "In your favourites"
        }
        localStorage.setItem(FAVORITES_KEY, JSON.stringify([...favorites]));
    });
  });
});