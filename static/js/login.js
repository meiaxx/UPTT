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