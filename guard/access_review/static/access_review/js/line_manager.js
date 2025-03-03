document.addEventListener('DOMContentLoaded', function () {
    // Show Spinner
    function showSpinner() {
        document.getElementById('loadingSpinner').style.display = 'block';
    }

    // Hide Spinner
    function hideSpinner() {
        document.getElementById('loadingSpinner').style.display = 'none';
    }

    // Attach Pagination Events
    function attachPaginationEvents() {
        document.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                const url = this.getAttribute('href');
                showSpinner();

                fetch(url)
                    .then(response => response.text())
                    .then(html => {
                        const parser = new DOMParser();
                        const newDocument = parser.parseFromString(html, 'text/html');
                        const newTableBody = newDocument.querySelector('.scrollable-tbody');
                        const newPagination = newDocument.querySelector('.pagination');

                        if (newTableBody && newPagination) {
                            document.querySelector('.scrollable-tbody').innerHTML = newTableBody.innerHTML;
                            document.querySelector('.pagination').innerHTML = newPagination.innerHTML;
                        } else {
                            console.error('Error: New table body or pagination not found in response.');
                        }
                        hideSpinner();
                        attachPaginationEvents(); // Reattach events after updating the DOM
                    })
                    .catch(error => {
                        console.error('Error loading page:', error);
                        hideSpinner();
                    });
            });
        });
    }

    // Initial Call to Attach Pagination Events
    attachPaginationEvents();

    // Review Modal Button Click
    document.querySelectorAll('.open-review-modal').forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.dataset.userId;
            showSpinner();

            fetch(`/user_review/${userId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('modalContent').innerHTML = `
                        <p><strong>Branch:</strong> ${data.branch}</p>
                        <p><strong>Department:</strong> ${data.department}</p>
                        <p><strong>Supervisor:</strong> ${data.supervisor}</p>
                        <p><strong>Email:</strong> ${data.email}</p>
                        <p><strong>Full Name:</strong> ${data.full_name}</p>
                    `;
                    hideSpinner();
                })
                .catch(error => {
                    console.error('Error loading user data:', error);
                    alert('Error loading user data.');
                    hideSpinner();
                });
        });
    });

    // Email Button Click
    const sendEmailsBtn = document.getElementById('sendEmailsBtn');
    if (sendEmailsBtn) {
        sendEmailsBtn.addEventListener('click', async function () {
            const url = sendEmailsBtn.dataset.url;
            const csrfToken = sendEmailsBtn.dataset.csrf;

            if (confirm("Are you sure you want to send emails to Supervisors?")) {
                showSpinner();
                sendEmailsBtn.textContent = "Sending Emails...";
                sendEmailsBtn.disabled = true;

                try {
                    const response = await fetch(url, {
                        method: 'GET',
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'Content-Type': 'application/json'
                        }
                    });
                    const data = await response.json();
                    alert(data.message);
                } catch (error) {
                    console.error('Failed to send emails:', error);
                    alert("Failed to send emails");
                } finally {
                    sendEmailsBtn.textContent = "Send Emails to Supervisors";
                    sendEmailsBtn.disabled = false;
                    hideSpinner();
                }
            }
        });
    }

    // DataTable Initialization
    if ($.fn.DataTable) {
        $('#systemUsersTable').DataTable({
            paging: true,
            searching: true,
            ordering: true,
            pageLength: 5,
            scrollY: '400px',
            scrollCollapse: true,
            fixedHeader: true
        });
    }

    // Select2 Initialization
    if ($.fn.select2) {
        $('#applicationSelect').select2({
            placeholder: 'Search and select an Application',
            allowClear: true
        });
    }

    // Update User Count
    function updateUserCount() {
        const rowCount = $('#systemUsersTable tbody tr').length;
        $('#userCount').text(rowCount);
    }

    if ($.fn.DataTable) {
        $('#systemUsersTable').on('draw.dt', updateUserCount);
    }
    updateUserCount();
// Toastr Auto Notification Handler
function showToastrAlerts(selector) {
    document.querySelectorAll(selector + ' .alert').forEach(alert => {
        const message = alert.textContent.trim();
        if (alert.classList.contains('status-success')) {
            toastr.success(message, '', { timeOut: 5000, closeButton: true, progressBar: true });
        } else if (alert.classList.contains('status-error') || alert.classList.contains('status-red')) {
            toastr.error(message, '', { timeOut: 5000, closeButton: true, progressBar: true });
        } else if (alert.classList.contains('status-warning')) {
            toastr.warning(message, '', { timeOut: 5000, closeButton: true, progressBar: true });
        }
    });
}

// Automatically Trigger Notifications
showToastrAlerts('#djangoMessages');
showToastrAlerts('#errorMessages');

    // Set Year Footer
    document.getElementById('currentYear').textContent = new Date().getFullYear();
});