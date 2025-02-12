document.addEventListener("DOMContentLoaded", function () {
    console.log("📌 Document loaded and JavaScript executed.");

    const paginationLinks = document.querySelectorAll(".page-link");
    const insightsTabsContainer = document.querySelector("#insightsTabsContainer");
    const tableBody = document.querySelector(".scrollable-tbody");
    const filtersContainer = document.querySelector(".row.mt-2.mb-2.justify-content-between");
    const pageTitle = document.querySelector("h2.text-center.mb-4");

    function showSpinner() {
        const spinner = document.getElementById("loadingSpinner");
        if (spinner) {
            spinner.style.display = "block";
        }
    }

    function hideSpinner() {
        const spinner = document.getElementById("loadingSpinner");
        if (spinner) {
            spinner.style.display = "none";
        }
    }

    // Function to update the page title and "No users available" message
    function updatePageTitle(category) {
        const categoryNames = {
            violations: "SYSTEM VIOLATIONS",
            idle: "IDLE ACCOUNTS",
            dormant: "DORMANT ACCOUNTS",
            mismatch: "DATA MISMATCH ACCOUNTS",
            duplicates: "DUPLICATE ACCOUNTS",
            delayed: "DELAYED DEACTIVATIONS"
        };

        const newTitle = categoryNames[category] || "ACCESS INSIGHTS";

        if (pageTitle) {
            pageTitle.innerText = newTitle;
        }

        const noUsersRow = document.querySelector("td[colspan='8']");
        if (noUsersRow) {
            noUsersRow.innerText = `NO ${newTitle} AVAILABLE`;
        }

        console.log(`🔹 Page title updated to: ${newTitle}`);
    }

    // Function to fetch and update data, including the filters section
    function fetchData(url, category = "violations") {
        showSpinner();
        console.log(`🚀 Fetching data from: ${url}`);

        fetch(url)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.text();
            })
            .then((html) => {
                const parser = new DOMParser();
                const newDocument = parser.parseFromString(html, "text/html");

                const newTableBody = newDocument.querySelector(".scrollable-tbody");
                const newPagination = newDocument.querySelector(".pagination");
                const newFiltersContainer = newDocument.querySelector(".row.mt-2.mb-2.justify-content-between");

                if (newTableBody && tableBody) {
                    tableBody.innerHTML = newTableBody.innerHTML;
                }

                if (newPagination) {
                    const existingPagination = document.querySelector(".pagination");
                    if (existingPagination) {
                        existingPagination.innerHTML = newPagination.innerHTML;
                    }
                }

                if (newFiltersContainer && filtersContainer) {
                    filtersContainer.innerHTML = newFiltersContainer.innerHTML;
                }

                updatePageTitle(category); // Update title dynamically
            })
            .catch((error) => {
                console.error("❌ Error fetching data:", error);
            })
            .finally(() => {
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

    // Event delegation to handle tab clicks inside #insightsTabsContainer only
    if (insightsTabsContainer) {
        insightsTabsContainer.addEventListener("click", function (e) {
            if (e.target.classList.contains("nav-link")) {
                e.preventDefault();
                const categoryUrl = e.target.getAttribute("href");

                // Extract the category from the href URL
                const urlParams = new URLSearchParams(new URL(categoryUrl, window.location.origin).search);
                const category = urlParams.get("category") || "violations";

                console.log(`📌 Category tab clicked: ${categoryUrl}, Extracted category: ${category}`);

                // Remove 'active' class from all tabs
                insightsTabsContainer.querySelectorAll(".nav-link").forEach((tab) => {
                    tab.classList.remove("active");
                });
                e.target.classList.add("active");

                // Fetch the relevant category data
                fetchData(categoryUrl, category);
            }
        });
        console.log("✅ Click event attached to insights category tabs only.");
    } else {
        console.warn("⚠️ insightsTabsContainer not found.");
    }

    // Initial title update based on current URL
    const initialParams = new URLSearchParams(window.location.search);
    const initialCategory = initialParams.get("category") || "violations";
    updatePageTitle(initialCategory);
});