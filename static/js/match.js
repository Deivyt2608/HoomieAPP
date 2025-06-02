let pasoActual = 0;
let respuestas = {}; // aquí guardamos las respuestas

const preguntas = [
    { 
        tipo: "explicacion",
        texto: "¡Bienvenido al Match! 💛💙", 
        descripcion: "Este formulario te ayudará a encontrar el roomie perfecto 🏡✨. Usamos tus respuestas para calcular la compatibilidad usando un algoritmo especial 🤓🔍. ¡Responde con sinceridad para tener los mejores resultados! 🚀", 
        imagen: "/static/imagenes/match1.jpg"
    },
    { tipo: "escala", texto: "El aseo del hogar", descripcion: "¿Qué tan importante es para ti que los espacios compartidos estén limpios? 🧽", imagen: "/static/imagenes/aseo.png" },
    { tipo: "escala", texto: "El ruido del hogar", descripcion: "¿Qué tan tolerante eres al ruido en casa (música, invitados, fiestas)? 🔊", imagen: "/static/imagenes/ruido.png" },
    { tipo: "escala", texto: "Las visitas", descripcion: "¿Qué tan cómodo te sientes recibiendo visitas en casa? 👥", imagen: "/static/imagenes/visitas.png" },
    { tipo: "escala", texto: "El aseo personal", descripcion: "¿Qué tan importante es para ti que tu roomie tenga buenos hábitos de higiene personal? 🛁", imagen: "/static/imagenes/personal.png" },
    { tipo: "escala", texto: "División de tareas del hogar", descripcion: "¿Qué tan importante es que las tareas se repartan equitativamente? 🧹", imagen: "/static/imagenes/tareas.png" },
    { tipo: "escala", texto: "Salidas de fiesta", descripcion: "¿Qué tan importante es para ti salir de fiesta o socializar fuera? 🎉", imagen: "/static/imagenes/fiesta.png" },
    { tipo: "binario", texto: "¿Fumas?", descripcion: "¿Fumas con regularidad en casa o fuera? 🚬", imagen: "/static/imagenes/fumas.png" },
    { tipo: "binario", texto: "¿Consumes alcohol regularmente?", descripcion: "¿Consumes bebidas alcohólicas de manera regular? 🍷", imagen: "/static/imagenes/alcohol.png" },
    { tipo: "binario", texto: "¿Trabajas?", descripcion: "¿Actualmente te encuentras trabajando? 🪪", imagen: "/static/imagenes/trabajas.png" },
    { tipo: "binario", texto: "¿Estudias?", descripcion: "¿Actualmente estudias, ya sea presencial o virtual? 📚", imagen: "/static/imagenes/estudias.png" },
    { tipo: "binario", texto: "¿Trabajas en casa?", descripcion: "¿Realizas trabajo remoto o desde casa habitualmente? 💻", imagen: "/static/imagenes/home-office.png" },
    { tipo: "binario", texto: "¿Tienes mascotas?", descripcion: "¿Convives con mascotas (perros, gatos, etc.) en tu vivienda? 🐾", imagen: "/static/imagenes/mascotas.png" }
    
];

// Referencias a elementos HTML
const modal = document.getElementById("modalMatch");
const cancelarBtn = document.getElementById("cancelarBtn");
const anteriorBtn = document.getElementById("anteriorBtn");
const siguienteBtn = document.getElementById("siguienteBtn");
const textoPregunta = document.getElementById("textoPregunta");
const descripcionPregunta = document.getElementById("descripcionPregunta");
const imagenPregunta = document.getElementById("imagenPregunta");
const respuestaPregunta = document.getElementById("respuestaPregunta");
const barraProgreso = document.getElementById("barraProgreso");

// Mostrar modal al cargar
modal.style.display = "flex";

// Botón Cancelar → solo en primer paso
cancelarBtn.onclick = () => {
    window.history.back();
};

anteriorBtn.onclick = () => {
    if (pasoActual > 0) {
        pasoActual--;
        actualizarPaso();
    }
};

siguienteBtn.onclick = () => {
    const paso = preguntas[pasoActual];

    // Validar respuesta si no es explicativo
    if (paso.tipo !== "explicacion") {
        const valorSeleccionado = respuestaPregunta.value;
        if (!valorSeleccionado) {
            mostrarToast("Por favor selecciona una opción antes de continuar.");
            return;
        }

        // Guardar respuesta
        respuestas[paso.texto] = valorSeleccionado;
    }

    if (pasoActual < preguntas.length - 1) {
        pasoActual++;
        actualizarPaso();
    } else {
        // Último paso: enviar al backend usando FormData
        const formData = new FormData();
        formData.append('aseo_hogar', respuestas['El aseo del hogar']);
        formData.append('ruido_hogar', respuestas['El ruido del hogar']);
        formData.append('visitas', respuestas['Las visitas']);
        formData.append('aseo_personal', respuestas['El aseo personal']);
        formData.append('division_tareas', respuestas['División de tareas del hogar']);
        formData.append('salidas_fiesta', respuestas['Salidas de fiesta']);
        formData.append('fuma', respuestas['¿Fumas?']);
        formData.append('alcohol', respuestas['¿Consumes alcohol regularmente?']);
        formData.append('trabaja_casa', respuestas['¿Trabajas en casa?']);
        formData.append('mascotas', respuestas['¿Tienes mascotas?']);
        formData.append('estudia', respuestas['¿Estudias?']);
        formData.append('trabaja', respuestas['¿Trabajas?']);

        fetch('/guardar-preferencias', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                mostrarToast("Error al guardar preferencias. Intenta nuevamente.");
            }
        })
        .catch(() => {
            mostrarToast("Error al conectar con el servidor.");
        });
    }
};

function actualizarPaso() {
    const paso = preguntas[pasoActual];
    const progreso = ((pasoActual + 1) / preguntas.length) * 100;

    barraProgreso.style.width = progreso + "%";
    textoPregunta.textContent = paso.texto;
    descripcionPregunta.textContent = paso.descripcion || "";
    descripcionPregunta.style.display = "block";
    imagenPregunta.src = paso.imagen;

    if (paso.tipo === "explicacion") {
        respuestaPregunta.style.display = "none";
    } else {
        respuestaPregunta.style.display = "block";

        respuestaPregunta.innerHTML = "";

        const optionDefault = document.createElement("option");
        optionDefault.value = "";
        optionDefault.disabled = true;
        optionDefault.selected = true;
        optionDefault.textContent = "-- Selecciona una opción --";
        respuestaPregunta.appendChild(optionDefault);

        if (paso.tipo === "escala") {
            for (let i = 1; i <= 5; i++) {
                const option = document.createElement("option");
                option.value = i;
                option.textContent = `${i} ${i === 1 ? "(Nada importante)" : i === 5 ? "(Muy importante)" : ""}`;
                respuestaPregunta.appendChild(option);
            }
        } else if (paso.tipo === "binario") {
            ["Sí", "No"].forEach((texto) => {
                const option = document.createElement("option");
                option.value = texto.toLowerCase();
                option.textContent = texto;
                respuestaPregunta.appendChild(option);
            });
        }
    }

    // Cambiar texto del botón en el último paso
    if (pasoActual === preguntas.length - 1) {
        siguienteBtn.textContent = "Enviar";
    } else {
        siguienteBtn.textContent = "Siguiente";
    }

    cancelarBtn.classList.toggle("oculto", pasoActual !== 0);
    anteriorBtn.classList.toggle("oculto", pasoActual === 0);
}

// Inicializar primer paso al cargar
actualizarPaso();

// Función para mostrar toast flotante
function mostrarToast(mensaje) {
    const toast = document.getElementById("toast");
    toast.textContent = mensaje;
    toast.classList.add("mostrar");
    setTimeout(() => {
        toast.classList.remove("mostrar");
    }, 3000);
}