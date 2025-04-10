document.addEventListener("DOMContentLoaded", function () {
    // =========================================
    // Registro de Usuario (registro.html)
    // =========================================
    const registroForm = document.querySelector("#form-registro");
    if (registroForm) {
        registroForm.addEventListener("submit", async function(e) {
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
    }

    // =========================================
    // Carrusel (inicio.html)
    // =========================================
    const carousel = document.querySelector('.carousel');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');

    if (carousel && nextBtn && prevBtn) {
        const items = Array.from(carousel.children);
        const totalItems = items.length;
        const itemWidth = 190;
        let index = 0;

        function moveCarousel(direction) {
            console.log("Moviendo carrusel hacia:", direction);
            if (direction === 'next') {
                index = (index + 1) % totalItems;
            } else {
                index = (index - 1 + totalItems) % totalItems;
            }

            carousel.style.transition = "transform 0.5s ease-in-out";
            carousel.style.transform = `translateX(-${index * itemWidth}px)`;
        }

        nextBtn.addEventListener('click', () => moveCarousel('next'));
        prevBtn.addEventListener('click', () => moveCarousel('prev'));
    }

    // =========================================
    // Agrega aquí más bloques condicionales si lo necesitas
    // Ejemplo:
    // const formIngreso = document.querySelector("#form-ingreso");
    // if (formIngreso) { ... }
});
