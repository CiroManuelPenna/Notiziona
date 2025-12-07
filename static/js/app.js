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

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".fav_term_button").forEach(btn => {
        const term = btn.dataset.term;
        const type = btn.dataset.type;

        if (btn.classList.contains("active")) {
          btn.innerHTML = type === "category"
            ? "Category in your favorites"
            : "Keyword in your favorites";
        }

        btn.addEventListener("click", async (ev) => {
            ev.preventDefault();
            ev.stopPropagation();

            const isActive = btn.classList.contains("active");

            if (isActive) {
                const res = await fetch("/api/favterm/remove", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ term })
                });

                if (res.ok) {
                    btn.classList.remove("active");
                    btn.innerHTML = type === "category"
                    ? "★ Add this category to favorites"
                    : "★ Add this keyword to favorites";
                }

            } else {
                const res = await fetch("/api/favterm/add", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ term, type })
                });

                if (res.ok) {
                    btn.classList.add("active");
                    btn.innerHTML = type === "category"
                    ? "Category in your favorites"
                    : "Keyword in your favorites";
                }
            }
        });
    });
});
