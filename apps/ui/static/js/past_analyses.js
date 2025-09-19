document.addEventListener("DOMContentLoaded", function () {
  const perPage = 3;
  const cards = Array.from(document.querySelectorAll(".analysis-card"));
  const pagination = document.getElementById("pagination-controls");

  function showPage(page) {
    const start = (page - 1) * perPage;
    const end = start + perPage;

    cards.forEach((card, index) => {
      card.classList.toggle("hidden", index < start || index >= end);
    });

    pagination.innerHTML = "";
    const totalPages = Math.ceil(cards.length / perPage);

    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement("button");
      btn.textContent = i;
      btn.className =
        "px-3 py-1 border rounded text-sm font-medium " +
        (i === page
          ? "bg-green-700 text-white border-green-700"
          : "bg-white text-green-700 border-green-300 hover:bg-green-100");
      btn.addEventListener("click", () => showPage(i));
      pagination.appendChild(btn);
    }
  }

  showPage(1);

  // Modal logic
  document.querySelectorAll(".view-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-id");
      document.getElementById(`modal-${id}`).classList.remove("hidden");
      document.getElementById(`modal-${id}`).classList.add("flex");
    });
  });

  document.querySelectorAll(".close-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-id");
      document.getElementById(`modal-${id}`).classList.add("hidden");
      document.getElementById(`modal-${id}`).classList.remove("flex");
    });
  });
});
