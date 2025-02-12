document.addEventListener("DOMContentLoaded", function () {
    console.log("📌 Document loaded and JavaScript executed.");

    const paginationLinks = document.querySelectorAll(".page-link");
    const employeeTabsContainer = document.querySelector("#employeeTabsContainer"); // Renamed selector
    const tableBody = document.querySelector(".scrollable-tbody");
    const filtersContainer = document.querySelector(".row.mt-2.mb-2.justify-content-between"); // The section you want to update

    function showSpinner() {
        document.getElementById("loadingSpinner").style.display = "block";
    }

    function hideSpinner() {
        document.getElementById("loadingSpinner").style.display = "none";
    }

    // Function to fetch and update data including the filters section
    function fetchData(url) {
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
                    document.querySelector(".pagination").innerHTML = newPagination.innerHTML;
                }

                if (newFiltersContainer) {
                    filtersContainer.innerHTML = newFiltersContainer.innerHTML;
                }

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

                console.log(`📌 Category tab clicked: ${categoryUrl}`);

                // Remove 'active' class from all tabs
                employeeTabsContainer.querySelectorAll(".nav-link").forEach((tab) => {
                    tab.classList.remove("active");
                });
                e.target.classList.add("active");

                // Fetch the relevant category data
                fetchData(categoryUrl);
            }
        });
        console.log("✅ Click event attached to employee category tabs only.");
    } else {
        console.warn("⚠️ employeeTabsContainer not found.");
    }
});
