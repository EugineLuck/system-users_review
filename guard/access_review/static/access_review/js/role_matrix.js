document.addEventListener("DOMContentLoaded", function () {
    const rolesTabsContainer = document.querySelector("#rolesTabsContainer");
    const filtersContainer = document.querySelector(".row.mt-2.mb-2.justify-content-between");
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
        console.log(`Fetching data for: ${category}`);

        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const newDocument = parser.parseFromString(html, "text/html");
                const activeTab = document.getElementById(category);

                if (!activeTab) {
                    console.warn(`No section found for category: ${category}`);
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
                    currentPagination.innerHTML = newPagination.innerHTML;
                    initializePaginationLinks();
                }

                updatePageTitle(category);
                hideSpinner();
            })
            .catch(error => {
                console.error("Fetch error:", error);
                hideSpinner();
            });
    }

    function handleTabClick(event) {
        event.preventDefault();
        const target = event.target.closest(".nav-link");
        if (!target) return;

        const categoryUrl = target.getAttribute("href");
        const category = new URL(categoryUrl, window.location.origin).searchParams.get("category") || "headers";

        rolesTabsContainer.querySelectorAll(".nav-link").forEach(tab => tab.classList.remove("active"));
        target.classList.add("active");

        document.querySelectorAll(".tab-content").forEach(tab => tab.style.display = "none");
        document.getElementById(category).style.display = "block";

        fetchData(categoryUrl, category);
    }

    function handlePaginationClick(event) {
        event.preventDefault();
        const link = event.target.closest(".page-link");
        if (!link) return;

        const activeTab = document.querySelector(".nav-link.active");
        if (!activeTab) return;

        const category = activeTab.getAttribute("data-category");
        fetchData(link.href, category);
    }

    function initializePaginationLinks() {
        document.querySelectorAll(".page-link").forEach(link => {
            link.addEventListener("click", handlePaginationClick);
        });
    }

    function initializeTabs() {
        rolesTabsContainer.addEventListener("click", handleTabClick);
    }

    function init() {
        const initialCategory = new URLSearchParams(window.location.search).get("category") || "headers";
        const initialTab = document.querySelector(`.nav-link[data-category="${initialCategory}"]`);

        if (initialTab) {
            initialTab.classList.add("active");
            document.getElementById(initialCategory).style.display = "block";
            fetchData(initialTab.href, initialCategory);
        }

        initializeTabs();
        initializePaginationLinks();
    }

    init();
});
