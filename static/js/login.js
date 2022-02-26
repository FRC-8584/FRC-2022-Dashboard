function logincheck() {
    var data = {
        "account": document.querySelector(".account").value,
        "password": document.querySelector(".password").value
    };
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader("Request-type", "login");
    xhr.send(JSON.stringify(data));
    xhr.onload = function () {
            if (JSON.parse(xhr.responseText).successed){
                document.querySelector(".login-fail").style.display = "none"
                document.location.href="/";
            }
            else{
                document.querySelector(".login-fail").style.display = ""
            }
        };
}
