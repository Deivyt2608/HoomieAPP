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
    // Anuncio flotante
    // =========================================
    const anuncio = document.getElementById("anuncio");
    if (anuncio) {
        setTimeout(() => {
            anuncio.classList.add("mostrar");
        }, 800);
    }

    window.cerrarAnuncio = function () {
        if (anuncio) {
            anuncio.classList.remove("mostrar");
        }
    }

    // =========================================
    // Modal Formulario
    // =========================================
    const modal = document.getElementById("formModal");
    const openModalBtn = document.getElementById("openModalBtn");
    const closeModalBtn = document.querySelector(".close");
    const steps = document.querySelectorAll(".form-step");
    const nextBtns = document.querySelectorAll(".next");
    const backBtns = document.querySelectorAll(".back");
    const progress = document.getElementById("progress");

    let currentStep = 0;

    function showStep(step) {
        steps.forEach((s, i) => {
            s.classList.toggle("active", i === step);
        });
        if (progress) {
            progress.style.width = ((step + 1) / steps.length) * 100 + "%";
        }
    }

    if (openModalBtn && modal) {
        openModalBtn.onclick = () => {
            modal.style.display = "flex";
            document.body.classList.add("modal-open");
            showStep(currentStep);
        };
    }

    if (closeModalBtn && modal) {
        closeModalBtn.onclick = () => {
            const modalContent = document.querySelector(".modal-content");
          
            modalContent.style.animation = "slideDown 0.4s ease";
          
            setTimeout(() => {
              modal.style.display = "none";
              modalContent.style.animation = "slideUp 0.4s ease";
              document.body.classList.remove("modal-open"); // Reiniciar animación por si se vuelve a abrir
            }, 400);
          };
          
    }

    const cancelBtn = document.querySelector(".cancel");

        cancelBtn.onclick = () => {
        const modalContent = document.querySelector(".modal-content");
        
        modalContent.style.animation = "slideDown 0.4s ease"; // Nueva animación

        setTimeout(() => {
            document.getElementById("formModal").style.display = "none";
            window.location.href = "publicar"; // Redirige suavemente
            document.body.classList.remove("modal-open");
        }, 400); // Espera que termine la animación 
        };


        window.onclick = (e) => {
            if (e.target === modal) {
              const modalContent = document.querySelector(".modal-content");
          
              // Animación de "pop" cuando hacen clic fuera del modal
              modalContent.animate([
                { transform: 'scale(1)', offset: 0 },
                { transform: 'scale(1.03)', offset: 0.5 },
                { transform: 'scale(1)', offset: 1 }
              ], {
                duration: 200,
                easing: 'ease-in-out'
              });
            }
          };
          

    nextBtns.forEach((btn, i) => {
        const inputs = steps[i].querySelectorAll("input[required], textarea[required]");
      
        function validateInputs() {
          const allFilled = Array.from(inputs).every(input => input.value.trim() !== "");
          btn.disabled = !allFilled;
        }
      
        inputs.forEach(input => {
          input.addEventListener("input", validateInputs);
        });
      
        btn.onclick = () => {
          const allFilled = Array.from(inputs).every(input => input.value.trim() !== "");
          if (allFilled) {
            currentStep++;
            showStep(currentStep);
          }
        };
      });
      
    backBtns.forEach((btn) => {
        btn.onclick = () => {
            currentStep--;
            showStep(currentStep);
        };
    });

});
