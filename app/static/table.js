document.addEventListener('DOMContentLoaded', function() {
    // Enable/disable delete button
    const deleteSelectedBtn = document.getElementById('deleteSelectedBtn');
    const checkboxes = document.querySelectorAll('.delete-checkbox');
    const selectAllCheckbox = document.getElementById('selectAll');

    function updateDeleteButtonState() {
        deleteSelectedBtn.disabled = !Array.from(checkboxes).some(checkbox => checkbox.checked);
    }

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateDeleteButtonState);
    });

    selectAllCheckbox.addEventListener('change', function() {
        const isChecked = selectAllCheckbox.checked;
        checkboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });
        updateDeleteButtonState();
    });

    // Sorting functionality
    document.querySelectorAll('th').forEach(th => {
        th.addEventListener('click', () => {
            const table = th.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const index = Array.from(th.parentNode.children).indexOf(th);
            const isAscending = th.classList.contains('asc');

            rows.sort((a, b) => {
                const aText = a.children[index].textContent.trim();
                const bText = b.children[index].textContent.trim();
                return isAscending ? aText.localeCompare(bText) : bText.localeCompare(aText);
            });

            rows.forEach(row => tbody.appendChild(row));
            th.classList.toggle('asc', !isAscending);
        });
    });

    // Delete functionality
    deleteSelectedBtn.addEventListener('click', () => {
        const selectedIds = Array.from(checkboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.closest('tr').dataset.id);

        if (selectedIds.length > 0 && confirm(`Deseja excluir ${selectedIds.length} itens? Esta ação não pode ser desfeita.`)) {
            fetch('/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ids: selectedIds })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    selectedIds.forEach(id => {
                        document.querySelector(`tr[data-id="${id}"]`).remove();
                    });
                    updateDeleteButtonState();
                }
            });
        }
    });

    // Hover effect
    document.querySelectorAll('tr').forEach(tr => {
        tr.addEventListener('mouseover', () => tr.style.backgroundColor = '#555');
        tr.addEventListener('mouseout', () => tr.style.backgroundColor = '');
    });

    // Edit functionality by clicking row
    document.querySelectorAll('.clickable-row').forEach(row => {
        row.addEventListener('click', (event) => {
            if (event.target.tagName !== 'INPUT' && !event.target.classList.contains('star')) {
                const id = row.dataset.id;
                const tableId = row.closest('table').id;
                const type = tableId.replace('Table', '').toLowerCase();
                window.location.href = `/edit/${type}/${id}`;
            }
        });
    });

    // Star rating functionality
    document.querySelectorAll('.star').forEach(star => {
        star.addEventListener('click', function(event) {
            event.stopPropagation();
            const value = this.dataset.value;
            const promptId = this.closest('tr').dataset.id;
            fetch(`/rate_prompt/${promptId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ rating: value })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const stars = this.closest('.stars').querySelectorAll('.star');
                    stars.forEach((s, index) => {
                        if (index < value) {
                            s.classList.add('filled');
                        } else {
                            s.classList.remove('filled');
                        }
                    });
                }
            });
        });
    });
});
