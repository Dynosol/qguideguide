$(document).ready(function () {
    // Initialize DataTables with server-side processing
    $('#courses').DataTable({
        'serverSide': true,           // Use server-side processing
        'processing': true,           // Show a processing indicator while fetching data
        'ajax': {
            'url': '/api/?format=datatables', // The API endpoint URL
            'type': 'GET'             // Use GET method for the AJAX request
        },
        'lengthMenu': [
            [10, 25, 50, 100, 200, 500, 1000, -1],
            [10, 25, 50, 100, 200, 500, 1000, 'Show all']
        ],
        'order': [], // Disable initial automatic sorting
        'columns': [
            {'data': 'title'},
            {'data': 'department'},
            {'data': 'instructor.name'}, // Accessing nested serializer field 'instructor.name'
            {'data': 'term'},
            {'data': 'students_enrolled'},
            {'data': 'response_count'},
            {'data': 'response_rate'}
        ],
        'error': function(xhr, error, thrown) {
            console.error("DataTables Error: ", error);
            console.error("Thrown Error: ", thrown);
            console.error("Response: ", xhr.responseText);
        }
    });
});
