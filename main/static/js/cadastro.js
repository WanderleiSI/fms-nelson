const usernameField=document.querySelector('#usernameField');
const feedBackError = document.querySelector(".feedback_error");
const emailField=document.querySelector('#emailField');
const emailError = document.querySelector(".email_error");
const exibeSenha = document.querySelector(".exibeSenha"); 
const passwordField = document.querySelector("#passwordField");
//const submitButton = document.querySelector('.submit-btn');

usernameField.addEventListener("keyup", (e) => {
    const usernameValue = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedBackError.style.display = "none";

    //console.log('usernameValue', usernameValue);
    if(usernameValue.length > 0){
        // chamar a API
        fetch("/auth/validacao", {
            //especificação do que vai ser enviado pelo post. O stringfy tranforma o objeto javascript em JSON para que possa ser enviado
            body: JSON.stringify({ username: usernameValue }), //chave e valor
            method: "POST",
        //fetch retorna uma promessa, então vai retornar outra promessa, mapear o json e retornar os dados
        })
        .then((res) => res.json())
        .then((data) => {
        console.log("data", data)
        if (data.error){
            usernameField.classList.add("is-invalid");
            //Exibe alerta de erro no formulário
            feedBackError.style.display = "block";
            feedBackError.innerHTML = `<p>${data.error}</p>`;
            //submitButton.setAttribute('disabled', 'disabled');
            //submitButton.disabled = true;
        } //else {
            //submitButton.removeAttribute('disabled');
        //}
        });
    }
});

emailField.addEventListener("keyup", (e) => {
    const emailValue = e.target.value;
    emailField.classList.remove("is-invalid");
    emailError.style.display = "none";

    if(emailValue.length > 0){
        fetch("/auth/valida_email", {
            body: JSON.stringify({ email: emailValue }), //chave e valor
            method: "POST",
        })  
        .then((res) => res.json())
        .then((data) => {
        console.log("data", data)
        if (data.error_email){
            //submitButton.setAttribute('disabled', 'disabled');
            //submitButton.disabled = true;
            emailField.classList.add("is-invalid");
            emailError.style.display = "block";
            emailError.innerHTML = `<p>${data.error_email}</p>`;
        } //else {
           // submitButton.removeAttribute('disabled');
        //}
        });
    }
});

const handleInput = (e) => {
    if(exibeSenha.textContent === 'Mostrar senha'){
        exibeSenha.textContent = "Esconder";

        passwordField.setAttribute("type", "text");
    } else {
        exibeSenha.textContent = "Mostrar senha";
        passwordField.setAttribute("type", "password");
    }
}


exibeSenha.addEventListener('click',handleInput);
