document.addEventListener("DOMContentLoaded", function () {
    console.log("📌 Document loaded and JavaScript executed.");

    const paginationLinks = document.querySelectorAll(".page-link");
    const employeeTabsContainer = document.querySelector("#employeeTabsContainer"); // Renamed selector
    const tableBody = document.querySelector(".scrollable-tbody");
    const filtersContainer = document.querySelector(".row.mt-2.mb-2.justify-content-between"); // The section you want to update
    const pageTitle = document.querySelector("h2.text-center.mb-4");

    function showSpinner() {
        document.getElementById("loadingSpinner").style.display = "block";
    }

    function hideSpinner() {
        document.getElementById("loadingSpinner").style.display = "none";
    }

    // Function to update the page title and "No users available" message
    function updatePageTitle(category) {
        const categoryNames = {
            active: "ACTIVE EMPLOYEES",
            ex_employees: "EX EMPLOYEES",
            suspended: "SUSPENDED EMPLOYEES",
            contingent: "CONTINGENT WORKERS",
            service_accounts: "SERVICE ACCOUNTS",
        };

        const newTitle = categoryNames[category] || "SYSTEM USERS";
        
        if (pageTitle) {
            pageTitle.innerText = newTitle;
        }

        const noUsersRow = document.querySelector("td[colspan='8']");
        if (noUsersRow) {
            noUsersRow.innerText = `NO ${newTitle} AVAILABLE`;
        }

        console.log(`🔹 Page title updated to: ${newTitle}`);
    }

    // Function to fetch and update data including the filters section
    function fetchData(url, category = "active") {
        showSpinner();
        console.log(`🚀 Fetching data from: ${url}`);

        fetch(url)
            .then((response) => response.text())
            .then((html) => {
                const parser = new DOMParser();
                const newDocument = parser.parseFromString(html, "text/html");

                const newTableBody = newDocument.querySelector(".scrollable-tbody");
                const newPagination = newDocument.querySelector(".pagination");
                const newFiltersContainer = newDocument.querySelector(".row.mt-2.mb-2.justify-content-between");

                if (newTableBody) {
                    tableBody.innerHTML = newTableBody.innerHTML;
                }

                if (newPagination) {
                    const existingPagination = document.querySelector(".pagination");
                    if (existingPagination) {
                        existingPagination.innerHTML = newPagination.innerHTML;
                    }
                }

                if (newFiltersContainer) {
                    filtersContainer.innerHTML = newFiltersContainer.innerHTML;
                }
                updatePageTitle(category); // Update title dynamically
                hideSpinner();
            })
            .catch((error) => {
                console.error("❌ Error fetching data:", error);
                hideSpinner();
            });
    }

    // Handle pagination clicks
    paginationLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            fetchData(this.getAttribute("href"));
        });
    });

    // Event delegation to handle tab clicks inside #employeeTabsContainer only
    if (employeeTabsContainer) {
        employeeTabsContainer.addEventListener("click", function (e) {
            if (e.target.classList.contains("nav-link")) {
                e.preventDefault();
                const categoryUrl = e.target.getAttribute("href");

                // Extract the category from the href URL
                const urlParams = new URLSearchParams(new URL(categoryUrl, window.location.origin).search);
                const category = urlParams.get("category") || "active"; 

                console.log(`📌 Category tab clicked: ${categoryUrl}, Extracted category: ${category}`);

                // Remove 'active' class from all tabs
                employeeTabsContainer.querySelectorAll(".nav-link").forEach((tab) => {
                    tab.classList.remove("active");
                });
                e.target.classList.add("active");

                // Fetch the relevant category data
                fetchData(categoryUrl, category);
            }
        });
        console.log("✅ Click event attached to employee category tabs only.");
    } else {
        console.warn("⚠️ employeeTabsContainer not found.");
    }

    // Initial title update based on current URL
    const initialParams = new URLSearchParams(window.location.search);
    const initialCategory = initialParams.get("category") || "active";
    updatePageTitle(initialCategory);
});