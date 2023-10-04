    // Función para redirigir a la página de logout después de dos minutos de inactividad
    function logoutAfterTwoMinutes() {
        setTimeout(function () {
          window.location.href = '/logout';  // Ruta de la página de logout en tu aplicación
        }, 2 * 60 * 1000);  // 2 minutos en milisegundos
      }
  
      // Llamar a la función cuando la página se cargue o cuando haya una interacción del usuario
      document.addEventListener('DOMContentLoaded', logoutAfterTwoMinutes);
      document.addEventListener('mousemove', logoutAfterTwoMinutes);
      document.addEventListener('keypress', logoutAfterTwoMinutes);