 // Obtener los elementos del campo de contraseña y el botón de alternar
 var campoContraseña = document.getElementById("contrasena");
 var botonAlternar = document.getElementById("ver-ocultar-contraseña");
 var iconoOjo = document.getElementById("icono-ojo");

 // Agregar un evento de clic al botón
 botonAlternar.addEventListener("click", function () {
     if (campoContraseña.type === "password") {
         // Mostrar la contraseña
         campoContraseña.type = "text";
         iconoOjo.classList.remove("fa-eye");
         iconoOjo.classList.add("fa-eye-slash");
     } else {
         // Ocultar la contraseña
         campoContraseña.type = "password";
         iconoOjo.classList.remove("fa-eye-slash");
         iconoOjo.classList.add("fa-eye");
     }
 });


     // Agregamos un evento para validar el campo de usuario al escribir
     document.getElementById("usuario").addEventListener("input", function () {
         // Obtenemos el valor actual del campo de usuario
         let usuario = this.value;
 
         // Removemos caracteres que no son números
         usuario = usuario.replace(/[^0-9]/g, "");
 
         // Limitamos a 8 caracteres
         usuario = usuario.slice(0, 8);
 
         // Asignamos el valor de vuelta al campo
         this.value = usuario;
     });


      // Agregamos un evento para validar el campo de usuario al escribir
     document.getElementById("telefono").addEventListener("input", function () {
     // Obtenemos el valor actual del campo de usuario
     let usuario = this.value;

     // Removemos caracteres que no son números
     usuario = usuario.replace(/[^0-9]/g, "");

     // Limitamos a 8 caracteres
     usuario = usuario.slice(0, 11);

     // Asignamos el valor de vuelta al campo
     this.value = usuario;
 });


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


     $(document).ready(function() {
       // Ocultar los campos de usuario y contraseña al cargar la página
       $('#usuario').hide();
       $('#contrasena').hide();
     
       // Mostrar u ocultar los campos de usuario y contraseña según la opción seleccionada
       $('#cargo').change(function() {
         var seleccion = $(this).val();
         if (seleccion === 'Administrador Sistema') {
           $('#usuario').show(); 
           $('#contrasena').show();
         } else {
           $('#usuario').hide();
           $('#contrasena').hide();
         }
       });
     });