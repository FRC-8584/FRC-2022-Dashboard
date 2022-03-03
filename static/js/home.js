function send_form() {
    if (valid()) {
        let xhr = new XMLHttpRequest();
        let check_box_1 = document.querySelector("#data > div > div:nth-child(1) > div:nth-child(2) > input")
        check_box_1.value = check_box_1.checked
        let check_box_2 = document.querySelector("#data > div > div:nth-child(1) > div:nth-child(18) > input")
        check_box_2.value = check_box_2.checked
        xhr.open("POST", "/", true);
        xhr.setRequestHeader("Request-type", "record");
        xhr.send(new FormData(document.querySelector("#form")));
        alert("傳送成功!")
    }
    else {
        alert("傳送失敗，內容填寫不完全，請重新檢查表單!")
    }
}

function valid() {
    if (document.getElementsByName("recorder-name")[0].value == "") {
        return false
    }
    if (document.getElementsByName("recorder-team")[0].value == "") {
        return false
    }
    return true
}

function get_data() {
    var data = {
        "team": document.getElementsByName("recorder-team")[0].value,
        "screen": document.getElementsByName("recorder-screen")[0].value
    };
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader("Request-type", "get_data");
    xhr.send(JSON.stringify(data));
    xhr.onload = function () {
        data = JSON.parse(xhr.responseText);
        NAME_LIS = [
            "auto-slide",
            "red-card",
            "recorder-name",
            "recorder-team",
            "recorder-screen",
            "auto-height",
            "auto-low",
            "manual-height",
            "manual-low",
            "manual-hang",
            "manual-hang-1",
            "manual-hang-2",
            "foul",
            "tech-foul",
            "yellow-card",
            "good",
            "bad",
            "spec",
            "win"
        ]
        let element;
        for (let i = 0; i < NAME_LIS.length; i++) {
            if (data[NAME_LIS[i]] != undefined) {
                element = document.getElementsByName(NAME_LIS[i])[0]
                if (element.type == "checkbox") {
                    element.checked = data[NAME_LIS[i]]
                }
                else {
                    element.value = data[NAME_LIS[i]]
                }
            }
        }
    }
}