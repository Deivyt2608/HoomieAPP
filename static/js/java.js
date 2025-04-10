document.querySelector("form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    try {
        const response = await fetch("/registro", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            alert("¡Usuario registrado con éxito!");
            window.location.href = "/inicio";
        } else {
            const data = await response.json();
            alert(data.detail || "Error al registrar.");
        }
    } catch (error) {
        alert("Error en el servidor. Intenta más tarde.");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector('.carousel');
    const items = Array.from(carousel.children);
    const totalItems = items.length;
    const visibleItems = 3;
    const itemWidth = 190; // Ancho de cada tarjeta (180px + margen)
    let index = 0;

    function moveCarousel(direction) {
        if (direction === 'next') {
            index = (index + 1) % totalItems; // Ciclo sin necesidad de clones
        } else {
            index = (index - 1 + totalItems) % totalItems;
        }

        carousel.style.transition = "transform 0.5s ease-in-out";
        carousel.style.transform = `translateX(-${index * itemWidth}px)`;
    }

    document.getElementById('prevBtn').addEventListener('click', () => moveCarousel('prev'));
    document.getElementById('nextBtn').addEventListener('click', () => moveCarousel('next'));
});

