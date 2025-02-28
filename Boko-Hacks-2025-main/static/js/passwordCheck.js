document.getElementById("regButton").addEventListener("click", checkPasswordReq);

function checkPasswordReq() {
    event.preventDefault();
    const password = document.getElementById("password").value;
    const resubPassword = document.getElementById("password2").value;
    const minLength = 16;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasSym = /[~!@#$%^&*()<>,.?]/.test(password);
    const hasNum = /[\d]/.test(password);
    let alertMessage = "";

    if(password.length < minLength || !hasUpperCase || !hasLowerCase || !hasSym || !hasNum) {
        alertMessage = "Password does not meet required conditions.\n";
    }

    if(password !== resubPassword) {
        alertMessage += "Passwords do not match.";
    }

    if(alertMessage) {
        alert(alertMessage);
    } else {
        document.querySelector("form").submit();
    }

}