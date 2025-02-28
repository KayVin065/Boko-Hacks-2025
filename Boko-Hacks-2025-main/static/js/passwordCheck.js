

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
    let alert = "";

    if(password.length < minLength || !hasUpperCase || !hasLowerCase || !hasSym || !hasNum) {
        alert = "Password does not meet requirements.";
    } else {
        this.submit();
    }

    if(password !== resubPassword) {
        alert += "Passwords do not match.";
    }

    document.getElementById("alertOutput") = alert;

}