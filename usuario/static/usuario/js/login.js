function togglePasswordVisibility() {
    var passwordField = document.getElementById("id_password");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

document.addEventListener("DOMContentLoaded", function() {
});