const erro_msg = "Por favor, verifique se os emails estão iguais!"

var testeCondicional = () => {
    if (confirmaEmail.value == email.value) {
        //sBtn.disabled = false;
        return true;
    } else {
        //sBtn.disabled = true;
        return false;
    }
}

// Agora a gente pega o botão de submit
var sBtn = document.getElementById('sbtn');

// ============== Parte de email ==============    
var email = document.getElementById('email');
email.addEventListener('input', async () => testeCondicional());

var confirmaEmail = document.getElementById('confirma-email');
confirmaEmail.addEventListener('input', async () => testeCondicional());

function checkDouble(event) {
    if (testeCondicional()) {
        document.getElementById('switch-pass-form').submit()
    } else {
        document.getElementById('erro-msg-span').innerHTML = erro_msg
    }
}
sBtn.addEventListener('click', () => checkDouble())