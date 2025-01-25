$(document).ready(function () {
    var table = $('#courses').DataTable({
        'serverSide': true,
        'processing': true,
        'responsive': true,
        'autoWidth': false,
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
            { 'data': 'instructor' },
            { 'data': 'term' },
            { 'data': 'invited_responses' },
            { 'data': 'course_mean_rating' },
            { 'data': 'hours_mean_rating' },
            { 'data': 'instructor_mean_rating'},
            { 
                'data': 'url',
                'render': function (data, type, row, meta) {
                    if (type === 'display') {
                        return `<a href="${data}" target="_blank">QGuide</a>`;
                    }
                    return data;
                }
            },
        ],
        'error': function(xhr, error, thrown) {
            console.error("DataTables Error: ", error);
            console.error("Thrown Error: ", thrown);
            console.error("Response: ", xhr.responseText);
        }
    }); 

    $(window).on('resize', function () {
        setTimeout(function () {
            table.columns.adjust().responsive.recalc();
        }, 300);
    });
});
