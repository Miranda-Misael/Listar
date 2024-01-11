document.addEventListener("DOMContentLoaded", function () {
  // Obtén el token CSRF desde el atributo de datos
  var csrfToken = document.querySelector("[data-csrf-token]").getAttribute("data-csrf-token");

  // Define la URL de la vista 'mod_presente' en Django
  var modificarPresenteURL = document.querySelector("[data-modificar-url]").getAttribute("data-modificar-url");

  function modificarPresente(idAsistencia) {
    // Reemplaza el marcador '0' en la URL con el ID de asistencia
    modificarPresenteURL = modificarPresenteURL.replace("0", idAsistencia);

    // Realiza la solicitud AJAX utilizando el URL actualizado y el token CSRF
    $.ajax({
      url: modificarPresenteURL,
      method: "POST", // Ajusta el método según tu vista de Django
      data: {
        csrfmiddlewaretoken: csrfToken, // Utiliza el token CSRF obtenido
      },
      success: function (data) {
        // La solicitud fue exitosa, actualiza la tabla de asistencias si es necesario
        // Puedes usar jQuery o JavaScript puro para hacerlo
      },
      error: function (error) {
        // Maneja errores si es necesario
        console.error("Error en la solicitud AJAX:", error);
      },
    });
  }
});
