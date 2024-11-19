$(document).ready(function () {
    // Initialize DataTables with server-side processing and responsive option
    var table = $('#courses').DataTable({
        'serverSide': true,
        'processing': true,
        'responsive': true,  // Enable responsive behavior
        'autoWidth': false,  // Disable autoWidth to allow full-width expansion
        'ajax': {
            'url': '/api/?format=datatables',
            'type': 'GET'
        },
        'lengthMenu': [
            [10, 25, 50, 100, 200, 500, 1000, -1],
            [10, 25, 50, 100, 200, 500, 1000, 'Show all']
        ],
        'order': [],
        'columns': [
            { 'data': 'title' },
            { 'data': 'department' },
            { 'data': 'instructor.name' },
            { 'data': 'term' },
            { 'data': 'students_enrolled' },
            { 'data': 'response_count' },
            { 'data': 'response_rate' }
        ],
        'error': function(xhr, error, thrown) {
            console.error("DataTables Error: ", error);
            console.error("Thrown Error: ", thrown);
            console.error("Response: ", xhr.responseText);
        }
    });

    // Listen for window resize events and adjust the DataTable accordingly
    $(window).on('resize', function () {
        // Use a slight delay to ensure layout has settled before resizing
        setTimeout(function () {
            table.columns.adjust().responsive.recalc();
        }, 300);
    });
});
