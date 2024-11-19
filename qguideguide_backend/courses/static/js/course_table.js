document.querySelectorAll('.course-table th').forEach(header => {
    header.addEventListener('click', () => {
        const table = header.closest('table');
        const tbody = table.querySelector('tbody');
        const index = Array.from(header.parentNode.children).indexOf(header);
        const isAscending = header.classList.contains('asc');

        // Remove active class from all headers
        document.querySelectorAll('.course-table th').forEach(th => th.classList.remove('active', 'asc', 'desc'));

        // Add active class to the clicked header
        header.classList.add('active');
        header.classList.toggle('asc', !isAscending);
        header.classList.toggle('desc', isAscending);

        // Sort rows
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort((rowA, rowB) => {
            const cellA = rowA.children[index].textContent.trim();
            const cellB = rowB.children[index].textContent.trim();

            // Check if the column is numeric and parse as float
            const numA = parseFloat(cellA);
            const numB = parseFloat(cellB);

            if (!isNaN(numA) && !isNaN(numB)) {
                return isAscending ? numA - numB : numB - numA;
            } else {
                return isAscending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
            }
        });

        // Append sorted rows to tbody
        rows.forEach(row => tbody.appendChild(row));
    });
});
