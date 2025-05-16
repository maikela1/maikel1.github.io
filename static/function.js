$(document).ready(function() {
    $('#login-btn').on('click', function() {
        const email = $('#email').val();
        const password = $('#password').val();
        const role = $('#role').val(); // Capturamos el rol, aunque tu backend actual no lo esté utilizando

        const userData = {
            correo: email,
            clave: password,
            rol: role // Enviamos el rol en los datos
        };

        $.ajax({
            method: 'POST',
            url: '/agregar_cliente', // Asegúrate de que esta sea la URL correcta de tu API de inicio de sesión
            dataType: 'json', // Esperamos una respuesta JSON del servidor
            contentType: 'application/json', // Indicamos que enviamos datos en formato JSON
            data: JSON.stringify(userData), // Convertimos el objeto JavaScript a JSON
            success: function(data) {
                // Manejar la respuesta exitosa del servidor
                console.log('Respuesta del servidor:', data);
                if (data.mensaje === 'Cliente guardado exitosamente') {
                    // Redirigir al usuario o mostrar un mensaje de éxito
                    window.location.href = '/dashboard'; // Ejemplo de redirección
                } else if (data.error) {
                    // Mostrar mensaje de error
                    const errorMessage = data.error;
                    $('#auth-view').append(`<div class="text-red-500 mt-2">${errorMessage}</div>`);
                    // O podrías mostrar el error en un elemento específico del DOM
                } else {
                    // Manejar otros tipos de respuestas
                    $('#auth-view').append('<div class="text-yellow-500 mt-2">Respuesta inesperada del servidor.</div>');
                }
            },
            error: function(error) {
                // Manejar errores de la petición
                console.error('Error al enviar los datos:', error);
                $('#auth-view').append('<div class="text-red-500 mt-2">No se pudo conectar con el servidor.</div>');
                // O podrías mostrar un mensaje de error más específico
            }
        });
    });
});