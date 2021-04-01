$(document).ready(function() {

  $("#id_email_registration").focusout("input", validateEmail);
  $("#id_email_registration").after("<div id='email-errors' class='text-danger'></div>");

})

function validateEmail() {

  let formData = $("#register-form").serialize();

  $.ajax({

    type: "POST",
    url: "/validate_email",
    data: formData,
    dataType: 'JSON',

    success: function(response) {

      $("#email-errors").text("");

      if (response.errors) {
        errorsAsP = "";
        for (let i = 0; i < response.errors.length; i++) {
          error = response.errors[i];
          console.log(error);
          errorsAsP += "<p><strong>" + error + "</strong></p>";
        }
        $("#email-errors").html(errorsAsP);
      }

    },

    error: function (response) {

      let message = "There is no response from server";
      $("#email-errors").text(message);
      console.log(response)

    }

  });

}
