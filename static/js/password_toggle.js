// ==========================================================
// MOSTRAR / ESCONDER SENHA
// ==========================================================

function togglePassword(idField, idButton) {
    const field = document.getElementById(idField);
    const button = document.getElementById(idButton);

    if (field.type === "password") {
        field.type = "text";
        button.innerText = "Ocultar";
    } else {
        field.type = "password";
        button.innerText = "Mostrar";
    }
}
