document.addEventListener("DOMContentLoaded", () => {

  document.querySelectorAll(".fav_button").forEach(button => {
    const url = button.dataset.url;
    const title = button.dataset.title;
    const image = button.dataset.image;

    if (button.classList.contains("active")) {
      button.innerHTML = "In your favorites";
    }

    button.addEventListener("click", async (event) => {
      event.preventDefault();
      event.stopPropagation();

      const isActive = button.classList.contains("active");

      if (isActive) {
        const res = await fetch("/api/favorite/remove", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({ url })
        });

        if (res.ok) {
          button.classList.remove("active");
          button.innerHTML = "★ Add to favorites";
        }
      } else {
        const res = await fetch("/api/favorite/add", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({ url, title, image })
        });

        if (res.ok) {
          button.classList.add("active");
          button.innerHTML = "In your favorites";
        }
      }
    });
  });
});
