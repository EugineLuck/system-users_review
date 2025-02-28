document.addEventListener("DOMContentLoaded", function () {
    const rolesTabsContainer = document.querySelector("#rolesTabsContainer");
    const pageTitle = document.querySelector("h2.text-center.mb-4");
    const loadingSpinner = document.getElementById("loadingSpinner");

    const categoryNames = {
        headers: "DEFINITION OF HEADERS",
        roles: "SYSTEM ROLE MATRIXES",
        roles_mapping: "USERS ROLE MAPPING",
        maker_checker: "MAKER CHECKER",
        sys_limits: "SYSTEM LIMITS",
        default: "ROLE MATRIXES",
    };

    function showSpinner() {
        if (loadingSpinner) loadingSpinner.style.display = "block";
    }

    function hideSpinner() {
        if (loadingSpinner) loadingSpinner.style.display = "none";
    }

    function updatePageTitle(category) {
        const newTitle = categoryNames[category] || categoryNames.default;
        if (pageTitle) pageTitle.innerText = newTitle;
        
        const noUsersRow = document.querySelector("td[colspan='8']");
        if (noUsersRow) noUsersRow.innerText = `NO ${newTitle} AVAILABLE`;
    }

    function fetchData(url, category = "headers") {
        showSpinner();
        console.log(`Fetching data for category: ${category}, URL: ${url}`);
    
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const newDocument = parser.parseFromString(html, "text/html");
                
                let activeTab = document.getElementById(category);
    
                if (!activeTab) {
                    console.warn(`No active tab found for category: ${category}`);
                    hideSpinner();
                    return;
                }
    
                // Select the correct table body in the fetched document
                const newTableBody = newDocument.querySelector(`#${category} .scrollable-tbody`);
                const currentTableBody = activeTab.querySelector(".scrollable-tbody");
    
                if (newTableBody && currentTableBody) {
                    console.log(`Updating table body for category: ${category}`);
                    currentTableBody.innerHTML = newTableBody.innerHTML;
                } else {
                    console.warn(`No table body found for category: ${category}`);
                    currentTableBody.innerHTML = "<tr><td colspan='8'>No data available</td></tr>";
                }
    
                // Select the correct pagination section in the fetched document
                const newPagination = newDocument.querySelector(`#${category} .pagination`);
                const currentPagination = activeTab.querySelector(".pagination");
    
                if (newPagination && currentPagination) {
                    currentPagination.innerHTML = newPagination.innerHTML;
                }
    
                // Hide all other tab contents and show the active one
                document.querySelectorAll(".tab-content").forEach(section => {
                    section.style.display = "none";
                });
    
                activeTab.style.display = "block";
    
                updatePageTitle(category);
                hideSpinner();
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                hideSpinner();
            });
    }
    

    function handleTabClick(event) {
        event.preventDefault();
        const target = event.target.closest(".nav-link");
        if (!target) return;

        const url = new URL(target.href, window.location.origin);
        const category = url.searchParams.get("category");

        rolesTabsContainer.querySelectorAll(".nav-link").forEach(tab => tab.classList.remove("active"));
        target.classList.add("active");

        fetchData(target.href, category);
    }

    function handlePaginationClick(event) {
        event.preventDefault();
        const activeTab = document.querySelector(".nav-link.active");
        if (!activeTab) return;

        const url = new URL(activeTab.href, window.location.origin);
        const category = url.searchParams.get("category");

        fetchData(event.target.getAttribute("href"), category);
    }

    function initializeTabsAndPagination() {
        if (rolesTabsContainer) {
            rolesTabsContainer.addEventListener("click", handleTabClick);
        }
        document.body.addEventListener("click", function (event) {
            if (event.target.matches(".page-link")) {
                handlePaginationClick(event);
            }
        });
    }

    function init() {
        const urlParams = new URLSearchParams(window.location.search);
        const initialCategory = urlParams.get("category") || "headers";

        const activeTab = document.querySelector(`.nav-link[href*="category=${initialCategory}"]`);
        if (activeTab) {
            activeTab.classList.add("active");
        }

        document.querySelectorAll(".tab-content").forEach(section => {
            section.style.display = "none";
        });
        const activeSection = document.getElementById(initialCategory);
        if (activeSection) {
            activeSection.style.display = "block";
        }

        const initialUrl = `${window.location.pathname}${window.location.search || `?category=${initialCategory}`}`;
        console.log(`Initial fetch URL: ${initialUrl}`);
        fetchData(initialUrl, initialCategory);

        initializeTabsAndPagination();
    }

    init();

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            const newCategory = this.getAttribute("href").split("category=")[1];
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.set("category", newCategory);
            window.history.pushState({}, "", "?" + urlParams.toString());

            document.querySelectorAll(".tab-content").forEach(div => div.style.display = "none");
            const activeTab = document.getElementById(newCategory);
            if (activeTab) {
                activeTab.style.display = "block";
            }
        });
    });
});
