// static/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const tableBody = document.getElementById('pdf-table-body');

    tableBody.addEventListener('click', function(event) {
        const target = event.target;
        const row = target.closest('tr');

        if (target.classList.contains('move-up')) {
            const prevRow = row.previousElementSibling;
            if (prevRow) {
                tableBody.insertBefore(row, prevRow);
                updateOrderNumbers();
            }
        }

        if (target.classList.contains('move-down')) {
            const nextRow = row.nextElementSibling;
            if (nextRow) {
                tableBody.insertBefore(nextRow, row);
                updateOrderNumbers();
            }
        }

        if (target.classList.contains('remove-row')) {
            row.remove();
            updateOrderNumbers();
        }
    });

    function updateOrderNumbers() {
        const rows = tableBody.querySelectorAll('tr');
        rows.forEach((row, index) => {
            row.querySelector('.order').textContent = index + 1;
        });
    }
});
