document.addEventListener("DOMContentLoaded", () => {
  const FAVORITES_KEY = "favorites";
  const favorites = new Map(JSON.parse(localStorage.getItem(FAVORITES_KEY)) || []);

  document.querySelectorAll(".fav_button").forEach(button => {
    const url = button.dataset.url;
    const image = button.dataset.image;
    const title = button.dataset.title;
    if (favorites.has(url)) {
        button.classList.add("active");
        button.innerHTML = "In your favorites";
    }

    button.addEventListener("click", (event) => {
        event.stopPropagation(); // prevents click from propagating to parent elements
        event.preventDefault();  // prevents the <a> link from triggering when click the "Add to favorites" button
        if (favorites.has(url)) {
            favorites.delete(url);
            button.classList.remove("active");
            button.innerHTML = "★ Add to favorites";
        } else {
            favorites.set(url, {url, image, title});
            button.classList.add("active");
            button.innerHTML = "In your favorites";
        }
        localStorage.setItem(FAVORITES_KEY, JSON.stringify([...favorites]));
    });
  });
});