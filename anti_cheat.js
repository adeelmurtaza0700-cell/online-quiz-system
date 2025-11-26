document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
        alert("You switched tabs! This is not allowed.");
    }
});
