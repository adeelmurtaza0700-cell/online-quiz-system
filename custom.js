document.addEventListener('contextmenu', event => event.preventDefault());
document.addEventListener('copy', event => event.preventDefault());
document.addEventListener('keydown', event => {
    if(event.key==="F12" || (event.ctrlKey && event.shiftKey && event.key==="I")){
        event.preventDefault();
    }
});
window.onblur = function(){alert("Do not switch tabs!");};
