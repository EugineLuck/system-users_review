document.getElementById("toggleSidebar").addEventListener("click", function() {
    var sidebar = document.getElementById("sidebar");
    var navbar = document.querySelector(".navbar");
    var mainContent = document.querySelector(".flex-grow-1");

    sidebar.classList.toggle("collapsed");

    // Adjust navbar when sidebar is toggled
    if (sidebar.classList.contains("collapsed")) {
        navbar.style.marginLeft = "80px";  
        navbar.style.paddingLeft = "80px"; 
        mainContent.style.marginLeft = "80px"; 
    } else {
        navbar.style.marginLeft = "200px"; 
        navbar.style.paddingLeft = "200px"; 
        mainContent.style.marginLeft = "200px"; 
    }
});
