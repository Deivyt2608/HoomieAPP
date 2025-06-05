const pasos = document.querySelectorAll(".paso");
const btnSiguiente = document.getElementById("btnSiguiente");
const btnAnterior = document.getElementById("btnAnterior");
const formulario = document.getElementById("formularioInmueble");
const inputFotos = document.getElementById("fotos");
const previewFotos = document.getElementById("previewFotos");
let pasoActual = 0;
let mapa, marcador;
let archivosCargados = [];


const secciones = [
  { titulo: "Tipo de inmueble", descripcion: "Selecciona si es apartamento o casa" },
  { titulo: "Ubicación", descripcion: "Indica ciudad, barrio y dirección" },
  { titulo: "Costos", descripcion: "Arriendo mensual y administración" },
  { titulo: "Características físicas", descripcion: "Área, habitaciones, baños, parqueaderos y estrato" },
  { titulo: "Preferencias y normas", descripcion: "Mascotas, fumar, fiestas y género" },
  { titulo: "Fotos", descripcion: "Sube al menos 2 imágenes del lugar" }
];

function mostrarPaso(index) {
  pasos.forEach((paso, i) => paso.classList.toggle("oculto", i !== index));
  btnAnterior.classList.toggle("oculto", index === 0);
  btnSiguiente.textContent = index === pasos.length - 1 ? "Publicar" : "Siguiente";

  document.getElementById("circuloNumero").textContent = `${index + 1}/${secciones.length}`;
  document.getElementById("tituloPaso").textContent = secciones[index].titulo;
  document.getElementById("descripcionPaso").textContent = secciones[index].descripcion;

  const circunferencia = 2 * Math.PI * 18;
  const offset = circunferencia * (1 - (index + 1) / secciones.length);
  document.getElementById("circuloProgreso").style.strokeDashoffset = offset;

  if (index === 1) {
    setTimeout(() => {
      if (!mapa) inicializarMapa();
      mapa.invalidateSize();
    }, 300);
  }
}

btnAnterior.addEventListener("click", () => {
  if (pasoActual > 0) {
    pasoActual--;
    mostrarPaso(pasoActual);
  }
});

btnSiguiente.addEventListener("click", () => {
    const camposActuales = pasos[pasoActual].querySelectorAll("input, select");
    for (let campo of camposActuales) {
      if (!campo.checkValidity()) {
        campo.reportValidity();
        return;
      }
    }
  
    // Validación paso 2
    if (pasoActual === 1) {
      const ciudad = document.getElementById("ciudad").value.trim();
      const barrio = document.getElementById("barrio").value.trim();
      const direccion = document.querySelector('input[name="direccion"]').value.trim();
  
      if (!ciudad || !barrio || !direccion) {
        alert("Por favor completa ciudad, barrio y dirección antes de continuar.");
        return;
      }
  
      const lat = parseFloat(document.getElementById("latitud").value);
      const lng = parseFloat(document.getElementById("longitud").value);
      const ciudadDetectada = ubicacionEsValida(lat, lng);
      if (!ciudadDetectada) {
        document.getElementById("modalUbicacion").classList.remove("oculto");
        return;
      }
    }
  
    // Validación paso final
    if (pasoActual === pasos.length - 1) {
      if (!inputFotos || inputFotos.files.length < 2) {
        alert("Debes subir al menos 2 fotos.");
        return;
      }
  
      // Desformatear valores monetarios
      const arriendo = document.getElementById("valor_arriendo");
      const administracion = document.getElementById("valor_administracion");
  
      arriendo.value = arriendo.value.replace(/[^0-9]/g, "");
      administracion.value = administracion.disabled ? "0" : administracion.value.replace(/[^0-9]/g, "");
  
      formulario.submit();
    } else {
      pasoActual++;
      mostrarPaso(pasoActual);
    }
  });
  

formulario.addEventListener("submit", () => {

    const arriendo = document.getElementById("valor_arriendo");
    const administracion = document.getElementById("valor_administracion");

    arriendo.value = arriendo.value.replace(/[^0-9]/g, "");
    administracion.value = administracion.disabled ? "0" : administracion.value.replace(/[^0-9]/g, "");

  });
  

function inicializarMapa() {
  mapa = L.map('mapa').setView([4.65, -74.1], 11);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(mapa);

  mapa.on('click', async function (e) {
    const { lat, lng } = e.latlng;
    document.getElementById('latitud').value = lat;
    document.getElementById('longitud').value = lng;

    if (marcador) {
      marcador.setLatLng(e.latlng);
    } else {
      marcador = L.marker(e.latlng).addTo(mapa);
    }

    try {
      const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`);
      const data = await res.json();
      if (data && data.address) {
        const a = data.address;
        const via = a.road || a.pedestrian || a.footway || a.path || a.highway || "";
        const numero = a.house_number || "";
        const barrio = a.neighbourhood || a.suburb || a.village || a.hamlet || a.quarter || "";
        const localidad = a.city || a.town || a.county || a.state_district || a.state || "";
        const pais = a.country || "";

        const direccionFormateada = [via, numero].filter(Boolean).join(" ") +
                                    (barrio ? ` - ${barrio}` : "") +
                                    (localidad ? `, ${localidad}` : "") +
                                    (pais ? ` (${pais})` : "");

        const campoDireccion = document.querySelector('input[name="direccion"]');
        if (campoDireccion) campoDireccion.value = direccionFormateada;
      }
    } catch (error) {
      console.error("Error al buscar dirección inversa:", error);
    }
  });
}

document.getElementById("usarUbicacion")?.addEventListener("click", () => {
  if (!navigator.geolocation) {
    alert("Tu navegador no permite obtener tu ubicación.");
    return;
  }

  navigator.geolocation.getCurrentPosition(async (position) => {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;

    document.getElementById("latitud").value = lat;
    document.getElementById("longitud").value = lng;

    mapa.setView([lat, lng], 16);

    if (marcador) {
      marcador.setLatLng([lat, lng]);
    } else {
      marcador = L.marker([lat, lng]).addTo(mapa);
    }

    try {
      const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`);
      const data = await res.json();
      if (data && data.address) {
        const campoDireccion = document.querySelector('input[name="direccion"]');
        const a = data.address;
        const via = a.road || a.pedestrian || "";
        const barrio = a.neighbourhood || a.suburb || "";
        const ciudad = a.city || a.town || a.county || "";

        campoDireccion.value = `${via} - ${barrio}, ${ciudad}`.trim();
        document.getElementById("ciudad").value = ciudad;
      }
    } catch (err) {
      console.error("Error al obtener dirección automática:", err);
    }
  }, () => {
    alert("No pudimos acceder a tu ubicación.");
  });
});

function ubicacionEsValida(lat, lng) {
  const dentroDe = (lat, lng, box) => (
    lat >= box.minLat && lat <= box.maxLat &&
    lng >= box.minLng && lng <= box.maxLng
  );
  const ciudades = {
    "Bogotá": { minLat: 4.48, maxLat: 4.83, minLng: -74.25, maxLng: -73.99 },
    "Medellín": { minLat: 6.14, maxLat: 6.34, minLng: -75.66, maxLng: -75.52 },
    "Cartagena": { minLat: 10.35, maxLat: 10.50, minLng: -75.60, maxLng: -75.45 }
  };
  for (const ciudad in ciudades) {
    if (dentroDe(lat, lng, ciudades[ciudad])) {
      return ciudad;
    }
  }
  return null;
}

const campoDireccion = document.getElementById("direccion");

campoDireccion?.addEventListener("change", async () => {
  const direccion = campoDireccion.value.trim();
  if (direccion.length < 5) return;

  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(direccion)}&countrycodes=co&limit=1`);
    const data = await res.json();

    if (data.length > 0) {
      const lat = parseFloat(data[0].lat);
      const lng = parseFloat(data[0].lon);

      // Actualizar mapa y marcador
      document.getElementById("latitud").value = lat;
      document.getElementById("longitud").value = lng;

      mapa.setView([lat, lng], 16);

      if (marcador) {
        marcador.setLatLng([lat, lng]);
      } else {
        marcador = L.marker([lat, lng]).addTo(mapa);
      }
    } else {
      alert("No se encontró la dirección ingresada.");
    }
  } catch (err) {
    console.error("Error al buscar coordenadas por dirección:", err);
    alert("Error al localizar la dirección.");
  }
});


mostrarPaso(pasoActual);

const barriosPorCiudad = {
    "Bogotá": {
      "Chapinero": [4.6486, -74.0576],
      "Usaquén": [4.7126, -74.0300],
      "Teusaquillo": [4.6394, -74.0798],
      "Kennedy": [4.6267, -74.1656],
      "Suba": [4.7480, -74.0975],
      "Santa Fe": [4.6064, -74.0714],
      "Fontibón": [4.6799, -74.1428],
      "Engativá": [4.7056, -74.1143],
      "Bosa": [4.6292, -74.1867],
      "Tunjuelito": [4.5728, -74.1306]
    },
    "Medellín": {
      "El Poblado": [6.2088, -75.5650],
      "Laureles": [6.2442, -75.6017],
      "Belén": [6.2294, -75.5906],
      "Robledo": [6.2791, -75.5894],
      "Buenos Aires": [6.2422, -75.5540],
      "Aranjuez": [6.2784, -75.5603],
      "Manrique": [6.2753, -75.5544],
      "Castilla": [6.2913, -75.5799],
      "San Javier": [6.2664, -75.6034],
      "La América": [6.2531, -75.5890]
    },
    "Cartagena": {
      "Centro Histórico": [10.4222, -75.5472],
      "Bocagrande": [10.3985, -75.5519],
      "Manga": [10.4091, -75.5376],
      "Getsemaní": [10.4237, -75.5475],
      "La Boquilla": [10.4531, -75.5022],
      "Pie de la Popa": [10.4124, -75.5338],
      "El Cabrero": [10.4321, -75.5427],
      "Castillogrande": [10.3909, -75.5541],
      "Torices": [10.4277, -75.5359],
      "Santa Rita": [10.4286, -75.5252]
    }
  };
  
  const selectCiudad = document.getElementById("ciudad");
  const selectBarrio = document.getElementById("barrio");
  
  selectCiudad?.addEventListener("change", () => {
    const ciudad = selectCiudad.value;
    selectBarrio.innerHTML = '<option value="">Selecciona un barrio</option>';
  
    if (barriosPorCiudad[ciudad]) {
      for (const barrio in barriosPorCiudad[ciudad]) {
        const option = document.createElement("option");
        option.value = barrio;
        option.textContent = barrio;
        selectBarrio.appendChild(option);
      }
    }
  });
  
  selectBarrio?.addEventListener("change", () => {
    const ciudad = selectCiudad.value;
    const barrio = selectBarrio.value;
  
    if (barriosPorCiudad[ciudad] && barriosPorCiudad[ciudad][barrio]) {
      const [lat, lng] = barriosPorCiudad[ciudad][barrio];
      mapa.setView([lat, lng], 15);
      document.getElementById("latitud").value = lat;
      document.getElementById("longitud").value = lng;
  
      if (marcador) {
        marcador.setLatLng([lat, lng]);
      } else {
        marcador = L.marker([lat, lng]).addTo(mapa);
      }
  
      // También puedes actualizar la dirección automáticamente
      const campoDireccion = document.querySelector('input[name="direccion"]');
      if (campoDireccion) campoDireccion.value = `${barrio}, ${ciudad}`;
    }
  });

  document.getElementById("cerrarModalUbicacion")?.addEventListener("click", () => {
    document.getElementById("modalUbicacion").classList.add("oculto");
  });
  
  function formatearMonedaSinSimbolo(input) {
    const valor = input.value.replace(/\D/g, ""); // solo números
    if (!valor) {
      input.value = "";
      return;
    }
  
    const conPuntos = valor.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    input.value = conPuntos;
  }
  
  
  // Detectar inputs de dinero
  ["valor_arriendo", "valor_administracion"].forEach(id => {
    const campo = document.getElementById(id);
    campo?.addEventListener("input", () => formatearMonedaSinSimbolo(campo));
  });
  

  function desformatearMoneda(valorFormateado) {
    return valorFormateado.replace(/[^0-9]/g, "");
  }
  
const adminSwitch = document.getElementById("admin_switch");
const campoAdministracion = document.getElementById("valor_administracion");

adminSwitch?.addEventListener("change", () => {
  const activo = adminSwitch.checked;
  const grupoAdmin = campoAdministracion.closest(".input-moneda");
    if (activo) {
    grupoAdmin.style.display = "block";
    campoAdministracion.disabled = false;
    campoAdministracion.value = "";
    } else {
    grupoAdmin.style.display = "none";
    campoAdministracion.disabled = true;
    campoAdministracion.value = "0";
    }

});

document.querySelectorAll(".stepper").forEach(stepper => {
    const input = stepper.querySelector("input");
    const btnMenos = stepper.querySelector(".menos");
    const btnMas = stepper.querySelector(".mas");
  
    function actualizarBotones() {
      const valor = parseInt(input.value) || 0;
      const min = parseInt(input.min || 0);
      const max = parseInt(input.max || Infinity);
  
      btnMenos.disabled = valor <= min;
      btnMas.disabled = valor >= max;
    }
  
    btnMenos.addEventListener("click", () => {
      let valor = parseInt(input.value) || 0;
      const min = parseInt(input.min || 0);
      if (valor > min) {
        input.value = valor - 1;
        actualizarBotones();
      }
    });
  
    btnMas.addEventListener("click", () => {
      let valor = parseInt(input.value) || 0;
      const max = parseInt(input.max || Infinity);
      if (valor < max) {
        input.value = valor + 1;
        actualizarBotones();
      }
    });
  
    // Actualiza cuando cambia manualmente el valor
    input.addEventListener("input", actualizarBotones);
  
    actualizarBotones(); // inicial
  });
  
  const dropzone = document.getElementById("dropzone");
  
  // 🧹 Limpiar preview y setear input
  function manejarArchivos(files) {
    const dataTransfer = new DataTransfer();
    previewFotos.innerHTML = "";
  
    files = [...files].filter(file => file.type.startsWith("image/"));
    files.forEach(file => {
      dataTransfer.items.add(file);
      const reader = new FileReader();
      reader.onload = e => {
        const img = document.createElement("img");
        img.src = e.target.result;
        previewFotos.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
  
    inputFotos.files = dataTransfer.files;
  }
  
  // 👉 Click sobre dropzone abre input
  dropzone.addEventListener("click", () => inputFotos.click());
  
  // 🪂 Drag & Drop sin duplicaciones
  dropzone.addEventListener("dragover", e => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });
  
  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });
  
  dropzone.addEventListener("drop", e => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    manejarArchivos(e.dataTransfer.files);
  })
  
  // 📂 Selección manual desde input
  inputFotos.addEventListener("change", () => {
    const files = inputFotos.files;
  
    if (files.length > 10) {
      alert("Solo puedes subir hasta 10 fotos.");
      inputFotos.value = "";
      return;
    }
  
    if (files.length < 2) {
      alert("Debes subir al menos 2 fotos.");
      return;
    }
  
    manejarArchivos(files);
  });
  
  
  function mostrarPrevisualizacion(files) {
    previewFotos.innerHTML = "";
  
    const dataTransfer = new DataTransfer();
  
    Array.from(files).forEach((file, index) => {
      if (!file.type.startsWith("image/")) return;
  
      const reader = new FileReader();
  
      reader.onload = (e) => {
        const contenedor = document.createElement("div");
        contenedor.classList.add("foto-preview");
  
        const img = document.createElement("img");
        img.src = e.target.result;
  
        const btnEliminar = document.createElement("button");
        btnEliminar.textContent = "❌";
        btnEliminar.classList.add("eliminar-foto");
        btnEliminar.type = "button";
  
        btnEliminar.addEventListener("click", () => {
          // ⚠️ Crear nuevo FileList SIN esta imagen
          const nuevoDT = new DataTransfer();
          Array.from(inputFotos.files).forEach((f) => {
            if (f.name !== file.name || f.size !== file.size) {
              nuevoDT.items.add(f);
            }
          });
  
          // ✅ Actualizar input
          inputFotos.files = nuevoDT.files;
  
          // ✅ Volver a mostrar
          mostrarPrevisualizacion(inputFotos.files);
        });
  
        contenedor.appendChild(img);
        contenedor.appendChild(btnEliminar);
        previewFotos.appendChild(contenedor);
      };
  
      reader.readAsDataURL(file);
      dataTransfer.items.add(file);
    });
  
    // ✅ Actualizar input al renderizar
    inputFotos.files = dataTransfer.files;
  }
