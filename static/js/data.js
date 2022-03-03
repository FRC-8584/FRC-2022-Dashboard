function get_data() {
    var data = {
        "team": document.getElementsByName("recorder-team")[0].value,
        "screen": document.getElementsByName("recorder-screen")[0].value
    };
    document.getElementById("form").reset();
    document.getElementsByName("recorder-team")[0].value = data.team;
    document.getElementsByName("recorder-screen")[0].value = data.screen
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
            "win",
            "Score",
            "RP_Score"
        ]
        let element;
        for (let i = 0; i < NAME_LIS.length; i++) {
            if (data[NAME_LIS[i]] != undefined) {
                element = document.getElementsByName(NAME_LIS[i])[0]
                if (element.tagName == "P") {
                    element.textContent = data[NAME_LIS[i]]
                }
                else if (element.type == "checkbox") {
                    element.checked = data[NAME_LIS[i]]
                }
                else {
                    element.value = data[NAME_LIS[i]]
                }
            }
        }
    }
}