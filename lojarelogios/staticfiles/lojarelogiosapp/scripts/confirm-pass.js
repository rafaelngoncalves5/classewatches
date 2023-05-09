const erro_msg = "Por favor, verifique se as senhas estão iguais!"
var testeCondicional = () => {
    if (confirmaSenha.value == senha.value) {
        //sBtn.disabled = false;
        return true;
    } else {
        //sBtn.disabled = true;
        return false;
    }
}

// Agora a gente pega o botão de submit
var sBtn = document.getElementById('sbtn');

// Variável representando o input de senha
var senha = document.getElementById('senha');
senha.addEventListener('input', async () => testeCondicional());

// Variável representando o input de confirmar senha
var confirmaSenha = document.getElementById('confirma-senha');
confirmaSenha.addEventListener('input', async () => testeCondicional());

function checkDouble() {
    if (testeCondicional()) {
        document.getElementById('switch-pass-2-form').submit()
    } else {
        document.getElementById('erro-msg-span').innerHTML = erro_msg
    }
}

// ============== Parte de senha ==============    
//www.linkedin.com/pulse/create-strong-password-validation-regex-javascript-mitanshu-kumar/
function checkRegex() {
    const isContainsSymbol =
        /^(?=.*[~`!@#$%^&*()--+={}\[\]|\\:;"'<>,.?/_₹])/;

    if (!isContainsSymbol.test(senha.value)) {
        let erro_msg_regex = "Sua senha precisa de pelo menos um caracter especial!"
        document.getElementById('erro-msg-span').innerHTML = erro_msg_regex
    } else if (senha.value.length <= 8) {
        let erro_msg_regex = "Sua senha precisa de pelo menos 8 caracteres"
        document.getElementById('erro-msg-span').innerHTML = erro_msg_regex
    }
    else {
        checkDouble()
        return true;
    }
}

sBtn.addEventListener('click', () => checkRegex())