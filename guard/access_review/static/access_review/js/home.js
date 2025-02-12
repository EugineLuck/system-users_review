document.addEventListener('DOMContentLoaded', function () {
    const paginationLinks = document.querySelectorAll('.page-link');
    

    // Show the loading spinner
    function showSpinner() {
        document.getElementById('loadingSpinner').style.display = 'block';
    }

    // Hide the loading spinner
    function hideSpinner() {
        document.getElementById('loadingSpinner').style.display = 'none';
    }

    paginationLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('href');

            // Show loading spinner
            showSpinner();

            // Fetch the new page content
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const newDocument = parser.parseFromString(html, 'text/html');
                    const newTableBody = newDocument.querySelector('.scrollable-tbody');
                    const newPagination = newDocument.querySelector('.pagination');

                    // Update the table and pagination
                    document.querySelector('.scrollable-tbody').innerHTML = newTableBody.innerHTML;
                    document.querySelector('.pagination').innerHTML = newPagination.innerHTML;

                    // Hide loading spinner
                    hideSpinner();
                })
                .catch(error => {
                    console.error('Error loading page:', error);
                    hideSpinner();
                });
        });
    });
});

$(document).ready(function() {
    // Initialize Select2
    $('#applicationSelect').select2({
        placeholder: 'Search and select an Application',
        allowClear: true
    });

    // Initialize DataTable with features like search, pagination, etc.
    $('#systemUsersTable').DataTable({
        paging: true,       // Enable pagination
        searching: true,    // Enable search box
        ordering: true,     // Enable column sorting
        pageLength: 5,      // Set page length
        scrollY: '400px',   // Enable vertical scroll
        scrollCollapse: true,
        fixedHeader: true   // Keep the header fixed while scrolling
    });

    // Set the current year in footer
    document.getElementById('currentYear').textContent = new Date().getFullYear();

    // Update user count dynamically
    function updateUserCount() {
        var rowCount = $('#systemUsersTable tbody tr').length;
        $('#userCount').text(rowCount);
    }

    // Update user count on table redraw
    $('#systemUsersTable').on('draw.dt', function() {
        updateUserCount();
    });

    // Initial user count
    updateUserCount();
});
