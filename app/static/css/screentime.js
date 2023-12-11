let startTime = 0;
let focusedTime= 0;
let timerInterval;

window.addEventListener("focus", function () {
    if (!startTime) {
        startTime = Date.now();
        timerInterval = setInterval(updateFocusedTime, 1000);
    }
});

window.addEventListener("blur", function() {
    if (startTime) {
        clearInterval(timerInterval);
        const currentTime = Date.now();
        focusedTime += (currentTime - startTime) / 1000;
        startTime = 0;
    }
});

function updateFocusedTime() {
    const currentTime = Date.now();
    focusedTime += (currentTime - startTime) / 1000;
    startTime = currentTime;
}