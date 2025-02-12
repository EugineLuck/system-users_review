document.addEventListener("DOMContentLoaded", function () {
    const headers = document.querySelectorAll("th");
    
    headers.forEach((th) => {
        const resizer = th.querySelector(".resizer");
        if (resizer) {
            resizer.addEventListener("mousedown", initResize);
        }
    });
    
    function initResize(event) {
        const th = event.target.parentElement;
        const startX = event.clientX;
        const startWidth = th.offsetWidth;
        
        document.addEventListener("mousemove", resizeColumn);
        document.addEventListener("mouseup", stopResize);
        
        function resizeColumn(event) {
            const newWidth = startWidth + (event.clientX - startX);
            th.style.width = `${newWidth}px`;
        }
        
        function stopResize() {
            document.removeEventListener("mousemove", resizeColumn);
            document.removeEventListener("mouseup", stopResize);
        }
    }
});