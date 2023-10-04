  // Función para calcular la edad a partir de la fecha de nacimiento
  function calcularEdad() {
    var fechaNacimiento = document.getElementById("fecha-nacimiento").value;
    var fechaNacimientoDate = new Date(fechaNacimiento);
    var hoy = new Date();
    var edad = hoy.getFullYear() - fechaNacimientoDate.getFullYear();
    var mes = hoy.getMonth() - fechaNacimientoDate.getMonth();

    if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNacimientoDate.getDate())) {
        edad--;
    }

    // Mostrar la edad en un campo de texto
    document.getElementById("edad").value = edad;
}

// Llamar a la función para calcular la edad cuando se cambie la fecha de nacimiento
document.getElementById("fecha-nacimiento").addEventListener("change", calcularEdad);


// Obtener el elemento de la fecha
var dateElement = document.querySelector('.date');
var currentDate = new Date();
// Formatear la fecha en "día/mes/año"
var formattedDate = currentDate.getDate() + '/' + (currentDate.getMonth() + 1) + '/' + currentDate.getFullYear();
// Actualizar el contenido del elemento de la fecha
dateElement.textContent = formattedDate;

  // Función para mostrar una alerta cuando queden 15 segundos antes de cerrar la sesión
  function mostrarAlertaDeCierre() {
    Swal.fire({
        title: "¡Cierre de sesión inminente!",
        text: "Por motivos de seguridad, su sesión se cerrará en 15 segundos.",
        icon: "warning",
        timer: 15000, // Tiempo en milisegundos (15 segundos)
        timerProgressBar: true,
        showConfirmButton: false
    });
}

// Función para redirigir a la página de logout después de dos minutos de inactividad
function logoutAfterTwoMinutes() {
    setTimeout(function () {
        mostrarAlertaDeCierre(); // Mostrar la alerta de cierre
    }, 105 * 1000); // 1 minuto y 45 segundos en milisegundos
    setTimeout(function () {
        window.location.href = '/logout'; // Redirigir a la página de logout
    }, 2 * 60 * 1000); // 2 minutos en milisegundos
}

// Llamar a la función cuando la página se cargue o cuando haya una interacción del usuario
document.addEventListener('DOMContentLoaded', logoutAfterTwoMinutes);
document.addEventListener('mousemove', logoutAfterTwoMinutes);
document.addEventListener('keypress', logoutAfterTwoMinutes);