const erro_msg = "Por favor, verifique se as senhas e emails estão iguais!"

var testeCondicional = () => {
    if (confirmaSenha.value == senha.value && confirmaEmail.value == email.value) {
        sBtn.disabled = false;
        return true
    } else {
        sBtn.disabled = true;
        document.getElementById('erro-msg-span').innerHTML = erro_msg
        return false
    }
}

// Variável representando o input de senha
var senha = document.getElementById('senha');
senha.addEventListener('input', async () => testeCondicional());

// Variável representando o input de confirmar senha
var confirmaSenha = document.getElementById('confirma-senha');
confirmaSenha.addEventListener('input', async () => testeCondicional());

// Agora a gente pega o botão de submit
var sBtn = document.getElementById('sbtn');

// ============== Parte de email ==============    
var email = document.getElementById('email');
email.addEventListener('input', async () => testeCondicional());

var confirmaEmail = document.getElementById('confirma-email');
confirmaEmail.addEventListener('input', async () => testeCondicional());