document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".responsive-image");

    images.forEach((img) => {
        const container = img.closest(".info-card");
        if (!container) return;

        const applyAspectClass = () => {
            // Calculate image aspect ratio and assign a class based on it. 
            const aspectRatio = img.naturalWidth / img.naturalHeight;
            container.classList.add(aspectRatio > 0.7 ? "wide-image" : "tall-image");
        };

        if (img.complete) {
            applyAspectClass(); // Image already loaded
        } else {
            img.onload = applyAspectClass; // Wait until loaded
        }
    });
});
