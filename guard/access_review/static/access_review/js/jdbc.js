$(document).ready(function () {
    console.log("JavaScript is running!");

    // Function to get the CSRF token from the meta tag
    function getCSRFToken() {
        return document.querySelector("meta[name='csrf-token']").getAttribute("content");
    }

    // Show the loading spinner
    function showSpinner() {
        document.getElementById('loadingSpinner').style.display = 'block';
    }

    // Hide the loading spinner
    function hideSpinner() {
        document.getElementById('loadingSpinner').style.display = 'none';
    }

    // Handle form submission
    $("#jdbcForm").on("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Collect form data
        let formData = {
            application: $("#applicationSelect").val(),
            username: $("#username").val(),
            password: $("#password").val(),
            host: $("#host").val(),
            port: $("#port").val(),
            service_name: $("#service_name").val()
        };

        showSpinner(); // Show the spinner

        // Send the form data to the server
        $.ajax({
            url: savejdbc,
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            },
            success: function (response) {
                hideSpinner(); // Hide the spinner
                Swal.fire({
                    icon: "success",
                    title: "Success!",
                    text: "JDBC saved successfully!",
                    confirmButtonColor: "#28a745"
                });
                $("#jdbcForm")[0].reset(); // Reset the form
            },
            error: function (xhr) {
                hideSpinner(); // Hide the spinner
                Swal.fire({
                    icon: "error",
                    title: "Save Failed",
                    text: "Error: " + xhr.responseText,
                    confirmButtonColor: "#d33"
                });
            }
        });
    });
});