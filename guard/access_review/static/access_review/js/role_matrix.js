document.addEventListener("DOMContentLoaded", function () {
    const rolesTabsContainer = document.querySelector("#rolesTabsContainer");
    const filtersContainer = document.querySelector(".row.mt-2.mb-2.justify-content-between");
    const pageTitle = document.querySelector("h2.text-center.mb-4");

    
    const categoryNames = {
        headers: "DEFINITION OF HEADERS",
        roles: "SYSTEM ROLE MATRIXES",
        user_mappings: "USERS ROLE MAPPING",
        maker_checker: "MAKER CHECKER",
        sys_limits: "SYSTEM LIMITS",
        default: "ROLE MATRIXES",
    };

    function showSpinner() {
        document.getElementById("loadingSpinner").style.display = "block";
    }

    function hideSpinner() {
        document.getElementById("loadingSpinner").style.display = "none";
    }

    function updatePageTitle(category) {
        const newTitle = categoryNames[category] || categoryNames.default;
        if (pageTitle) pageTitle.innerText = newTitle;
        const noUsersRow = document.querySelector("td[colspan='8']");
        if (noUsersRow) noUsersRow.innerText = `NO ${newTitle} AVAILABLE`;
    }

    function fetchData(url, category = "active") {  
        showSpinner();
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const newDocument = parser.parseFromString(html, "text/html");
                const activeTab = document.getElementById(category);
                if (!activeTab) {
                    hideSpinner();
                    return;
                }
                const newTableBody = newDocument.querySelector(`#${category} .scrollable-tbody`);
                const currentTableBody = activeTab.querySelector(".scrollable-tbody");
                if (newTableBody && currentTableBody) {
                    currentTableBody.innerHTML = newTableBody.innerHTML;
                }
                const newPagination = newDocument.querySelector(`#${category} .pagination`);
                const currentPagination = activeTab.querySelector(".pagination");
                if (newPagination && currentPagination) {
                    currentPagination.replaceWith(newPagination);
                }
                updatePageTitle(category);
                hideSpinner();
            })
            .catch(error => {
                hideSpinner();
            });
    }

    function handleTabClick(event) {
        event.preventDefault();
        const target = event.target;
        if (!target.classList.contains("nav-link")) return;
        const categoryUrl = target.getAttribute("href");
        const category = new URL(categoryUrl, window.location.origin).searchParams.get("category") || "active";
        rolesTabsContainer.querySelectorAll(".nav-link").forEach(tab => tab.classList.remove("active"));
        target.classList.add("active");
        fetchData(categoryUrl, category);
    }

    function handlePaginationClick(event) {
        event.preventDefault();
        fetchData(event.target.getAttribute("href"));
    }

    function initializeTabsAndPagination() {
        if (rolesTabsContainer) {
            rolesTabsContainer.addEventListener("click", handleTabClick);
        }
        document.querySelectorAll(".page-link").forEach(link => {
            link.addEventListener("click", handlePaginationClick);
        });
    }

    function initializeTabSections() {
        const tabs = document.querySelectorAll(".nav-link[data-category]");
        const sections = document.querySelectorAll(".tab-content");
        tabs.forEach(tab => {
            tab.addEventListener("click", function (event) {
                event.preventDefault();
                const category = this.getAttribute("data-category");
                sections.forEach(section => (section.style.display = "none"));
                document.getElementById(category).style.display = "block";
                tabs.forEach(t => t.classList.remove("active"));
                this.classList.add("active");
            });
        });
    }

    function init() {
        const initialCategory = new URLSearchParams(window.location.search).get("category") || "active";
        updatePageTitle(initialCategory);
        initializeTabsAndPagination();
        initializeTabSections();
    }

    init();
});
