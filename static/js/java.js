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