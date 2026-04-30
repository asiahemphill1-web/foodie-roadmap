const deleteForms = document.querySelectorAll("[data-confirm-delete]");

deleteForms.forEach((form) => {
    form.addEventListener("submit", (event) => {
        const shouldDelete = confirm("Are you sure you want to delete this item?");

        if (!shouldDelete) {
            event.preventDefault();
        }
    });
});
