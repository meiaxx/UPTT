function mostrarHora(tipo) {
    const ahora = new Date();
    let hora = ahora.getHours();
    const minutos = ahora.getMinutes();
    const amPm = hora >= 12 ? 'PM' : 'AM';

    if (hora > 12) {
      hora = hora - 12;
    } else if (hora === 0) {
      hora = 12;
    }

    const horaActual = hora.toString().padStart(2, '0') + ':' + minutos.toString().padStart(2, '0') + ' ' + amPm;

    if (tipo === 'entrada') {
      document.getElementById('hora-entrada').textContent = 'Hora de Entrada: ' + horaActual;
    } else if (tipo === 'salida') {
      document.getElementById('hora-salida').textContent = 'Hora de Salida: ' + horaActual;
    }
  }

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