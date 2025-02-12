$(document).ready(function () {
    console.log("JavaScript is running!");

    let excelName = "";
    let modelFieldsMapping = {};
    let sankeyData = [];

    // Function to get the CSRF token from the meta tag
    function getCSRFToken() {
        return document.querySelector("meta[name='csrf-token']").getAttribute("content");
    }

    // Load Google Charts and initialize the Sankey chart
    google.charts.load('current', { 'packages': ['sankey'] });
    google.charts.setOnLoadCallback(drawSankey);

    // Enable drag-and-drop functionality for Excel headers and model fields
    function enableDragAndDrop() {
        $(".excel-header").draggable({
            revert: "invalid",
            helper: "clone"
        });

        $(".model-field").droppable({
            accept: ".excel-header",
            drop: function (event, ui) {
                let targetField = $(this).data("field");
                let excelHeader = ui.draggable.data("header");

                if (!targetField || !excelHeader) return;

                if (modelFieldsMapping[targetField]) {
                    Swal.fire({
                        icon: "warning",
                        title: "Mapping Exists",
                        text: `${targetField} is already mapped!`,
                        confirmButtonColor: "#3085d6"
                    });
                    return;
                }

                // Update the mapping and UI
                modelFieldsMapping[targetField] = excelHeader;
                updateSankeyChart();

                $(this)
                    .html(`${targetField} <span class="undo-mapping" style="color: red; cursor: pointer;">❌</span>`)
                    .addClass("mapped")
                    .data("excel-header", excelHeader);

                ui.draggable.closest("tr").remove();
                updateRowNumbers("#excelHeadersTable tbody");
            }
        });
    }

    // Handle undo mapping action
    $(document).on("click", ".undo-mapping", function () {
        let parent = $(this).closest(".model-field");
        let targetField = parent.data("field");
        let excelHeader = parent.data("excel-header");

        if (!targetField || !excelHeader) return;

        // Remove the mapping and update the UI
        delete modelFieldsMapping[targetField];

        $("#excelHeadersTable tbody").append(
            `<tr>
                <td>${$("#excelHeadersTable tbody tr").length + 1}</td>
                <td class="excel-header draggable" data-header="${excelHeader}">${excelHeader}</td>
            </tr>`
        );

        parent.html(targetField).removeClass("mapped");
        enableDragAndDrop();
        updateSankeyChart();
    });

    // Update the Sankey chart data and redraw it
    function updateSankeyChart() {
        sankeyData = Object.entries(modelFieldsMapping).map(([field, header]) => [`${header} (Excel)`, `${field} (Model)`, 1]);
        console.log("Updated Sankey Data:", sankeyData);
        drawSankey();
    }

    // Draw the Sankey chart using Google Charts
    function drawSankey() {
        if (!sankeyData.length) return console.log("No data for Sankey chart.");

        let data = new google.visualization.DataTable();
        data.addColumn('string', 'Excel Header');
        data.addColumn('string', 'Model Field');
        data.addColumn('number', 'Mappings');
        data.addRows(sankeyData);

        let chart = new google.visualization.Sankey(document.getElementById('sankeyChart'));
        chart.draw(data, { width: '100%', height: 500 });
    }

    // Show the loading spinner and reset the progress bar
    function showSpinner() {
        document.getElementById('loadingSpinner').style.display = 'block';
    }
    
    function hideSpinner() {
        document.getElementById('loadingSpinner').style.display = 'none';
    }
    

    // Handle Excel file upload
    $("#uploadForm").on("submit", function (event) {
        event.preventDefault();
        let formData = new FormData(this);

        showSpinner();

        $.ajax({
            url: uploadExcelUrl,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            xhr: function () {
                let xhr = new XMLHttpRequest();
                xhr.upload.onprogress = function (e) {
                    if (e.lengthComputable) {
                        let percent = (e.loaded / e.total) * 100;
                        $("#progressBar").css("width", percent + "%").text(Math.round(percent) + "%");
                    }
                };
                return xhr;
            },
            success: function (response) {
                hideSpinner();
                $("#excelHeadersTable tbody").empty();

                if (response.error) {
                    Swal.fire({
                        icon: "error",
                        title: "Upload Failed",
                        text: response.error,
                        confirmButtonColor: "#d33"
                    });
                    return;
                }

                excelName = response.excel_name.toUpperCase();
                $("#excel_name").text(excelName + " EXCEL FIELDS");

                response.excel_headers.forEach((header, index) => {
                    $("#excelHeadersTable tbody").append(
                        `<tr>
                            <td>${index + 1}</td>
                            <td class="excel-header draggable" data-header="${header}">${header}</td>
                        </tr>`
                    );
                });

                enableDragAndDrop();
            },
            error: function () {
                hideSpinner();
                Swal.fire({
                    icon: "error",
                    title: "Upload Failed",
                    text: "An error occurred while uploading the file.",
                    confirmButtonColor: "#d33"
                });
            }
        });
    });

    // Handle model selection change
    $("#applicationSelect").on("change", function () {
        let selectedModel = $(this).val();
        if (!selectedModel) return;

        showSpinner();

        $.ajax({
            url: getModelFieldsUrl,
            type: "GET",
            data: { model_name: selectedModel },
            success: function (response) {
                hideSpinner();
                $("#modelFieldsTable tbody").empty();

                if (response.error) {
                    Swal.fire({
                        icon: "error",
                        title: "Error",
                        text: response.error,
                        confirmButtonColor: "#d33"
                    });
                    return;
                }

                let modelName = response.model_name.toUpperCase();
                if (modelName === 'SYSTEM_USERS') {
                    modelName = 'SYSTEMS';
                }
                $("#modelFieldsHeader").text(modelName + " MODEL FIELDS");

                response.model_fields.forEach((field, index) => {
                    $("#modelFieldsTable tbody").append(
                        `<tr>
                            <td>${index + 1}</td>
                            <td class="model-field" data-field="${field}">${field}</td>
                        </tr>`
                    );
                });

                enableDragAndDrop();
            },
            error: function () {
                hideSpinner();
                Swal.fire({
                    icon: "error",
                    title: "Fetch Failed",
                    text: "Failed to retrieve model fields.",
                    confirmButtonColor: "#d33"
                });
            }
        });
    });

    // Save mappings to the server
    $("#saveMappings").on("click", function () {
        let mappings = [];

        if (!excelName) {
            Swal.fire({
                icon: "warning",
                title: "Missing Excel File",
                text: "Please upload an Excel file to save mappings.",
                confirmButtonColor: "#3085d6"
            });
            return;
        }

        $("#modelFieldsTable .model-field").each(function () {
            let modelField = $(this).data("field");
            let excelHeader = $(this).data("excel-header");

            if (modelField && excelHeader) {
                mappings.push({ model_field: modelField, excel_header: excelHeader });
            }
        });

        console.log("Mappings data to be saved:", mappings);
        if (!mappings.length) {
            Swal.fire({
                icon: "info",
                title: "No Mappings",
                text: "There are no mappings to save.",
                confirmButtonColor: "#3085d6"
            });
            return;
        }

        showSpinner();

        $.ajax({
            url: saveMappingsUrl,
            type: "POST",
            data: JSON.stringify({ model_name: excelName, mappings }),
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            },
            success: function () {
                hideSpinner();
                Swal.fire({
                    icon: "success",
                    title: "Success!",
                    text: "Mappings saved successfully!",
                    confirmButtonColor: "#28a745"
                });
            },
            error: function (xhr) {
                hideSpinner();
                Swal.fire({
                    icon: "error",
                    title: "Save Failed",
                    text: "Error: " + xhr.responseText,
                    confirmButtonColor: "#d33"
                });
            }
        });
    });

    // Update row numbers in a table
    function updateRowNumbers(tableSelector) {
        $(tableSelector).children("tr").each(function (index) {
            $(this).find("td:first").text(index + 1);
        });
    }

    // Initialize drag-and-drop functionality
    enableDragAndDrop();
});