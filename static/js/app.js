document.addEventListener('DOMContentLoaded', () => {
    // Navigation Logic
    const navLinks = document.querySelectorAll('.nav-links li');
    const sections = document.querySelectorAll('.view-section');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Update active nav state
            navLinks.forEach(nav => nav.classList.remove('active'));
            link.classList.add('active');

            // Show target section
            const targetId = link.getAttribute('data-target');
            sections.forEach(section => {
                if (section.id === targetId) {
                    section.classList.remove('hidden');
                } else {
                    section.classList.add('hidden');
                }
            });

            // Load history if history tab clicked
            if (targetId === 'history-view') {
                loadHistory();
            }
        });
    });

    // Single Generation Form
    const singleForm = document.getElementById('single-form');
    const singleInput = document.getElementById('single-input');
    const singleSubmitBtn = singleForm.querySelector('button[type="submit"]');
    const singleResultContainer = document.getElementById('single-result-container');
    const singleResult = document.getElementById('single-result');

    singleForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const inputVal = singleInput.value.trim();
        if (!inputVal) return;

        // UI Loading state
        singleSubmitBtn.disabled = true;
        singleResultContainer.classList.add('hidden');

        try {
            const res = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userInput: inputVal })
            });
            const data = await res.json();

            if (!res.ok) throw new Error(data.error || 'Server error');

            singleResult.textContent = data.response;
            singleResultContainer.classList.remove('hidden');
        } catch (error) {
            singleResult.textContent = `Error: ${error.message}`;
            singleResult.style.color = '#ef4444';
            singleResultContainer.classList.remove('hidden');
        } finally {
            singleSubmitBtn.disabled = false;
        }
    });

    // Batch Generation Form
    const batchForm = document.getElementById('batch-form');
    const addInputBtn = document.getElementById('add-input-btn');
    const batchInputsContainer = document.getElementById('batch-inputs-container');
    const batchSubmitBtn = batchForm.querySelector('button[type="submit"]');
    const batchResultContainer = document.getElementById('batch-result-container');
    const batchResultsList = document.getElementById('batch-results-list');

    let inputCount = 1;

    addInputBtn.addEventListener('click', () => {
        inputCount++;
        const row = document.createElement('div');
        row.className = 'input-group batch-row';
        row.innerHTML = `
            <label>Input ${inputCount}</label>
            <div class="row-flex">
                <input type="text" class="batch-input" placeholder="e.g. Another question..." required>
                <button type="button" class="remove-btn" title="Remove">&times;</button>
            </div>
        `;
        batchInputsContainer.appendChild(row);

        // Remove functionality
        row.querySelector('.remove-btn').addEventListener('click', () => {
            row.remove();
        });
    });

    batchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const inputs = Array.from(document.querySelectorAll('.batch-input'))
            .map(input => input.value.trim())
            .filter(val => val !== '');

        if (inputs.length === 0) return;

        // UI Loading state
        batchSubmitBtn.disabled = true;
        batchResultContainer.classList.add('hidden');
        batchResultsList.innerHTML = '';

        try {
            const res = await fetch('/generate-batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ inputs })
            });
            const data = await res.json();

            if (!res.ok) throw new Error(data.error || 'Server error');

            // Render batch responses
            const resultCard = document.createElement('div');
            resultCard.className = 'card glass';
            
            data.responses.forEach((response, index) => {
                const item = document.createElement('div');
                item.className = 'batch-result-item';
                item.innerHTML = `
                    <div class="badge">Input: ${inputs[index]}</div>
                    <div class="response-text">${response}</div>
                `;
                resultCard.appendChild(item);
            });

            batchResultsList.appendChild(resultCard);
            batchResultContainer.classList.remove('hidden');

        } catch (error) {
            batchResultsList.innerHTML = `<div class="card glass" style="color: #ef4444;">Error: ${error.message}</div>`;
            batchResultContainer.classList.remove('hidden');
        } finally {
            batchSubmitBtn.disabled = false;
        }
    });

    // History View
    const refreshHistoryBtn = document.getElementById('refresh-history-btn');
    const historyContainer = document.getElementById('history-container');

    refreshHistoryBtn.addEventListener('click', loadHistory);

    async function loadHistory() {
        historyContainer.innerHTML = '<div class="loader">Loading history...</div>';
        try {
            const res = await fetch('/history');
            const data = await res.json();

            if (!res.ok) throw new Error(data.error || 'Failed to load history');

            if (data.history.length === 0) {
                historyContainer.innerHTML = '<div class="loader">No history found.</div>';
                return;
            }

            historyContainer.innerHTML = '';
            
            data.history.forEach(record => {
                const date = new Date(record.timestamp).toLocaleString();
                const typeLabel = record.requestType === 'batch' 
                    ? `<span class="badge" style="background: rgba(168, 85, 247, 0.15); color: #c084fc;">Batch</span>`
                    : `<span class="badge">Single</span>`;

                const card = document.createElement('div');
                card.className = 'card glass history-card';
                card.innerHTML = `
                    <div class="history-header">
                        <div>${typeLabel}</div>
                        <div>${date}</div>
                    </div>
                    <div class="history-body">
                        <strong>User Input:</strong>
                        <p>${record.userInput}</p>
                        <strong>AI Response:</strong>
                        <p>${record.response}</p>
                    </div>
                `;
                historyContainer.appendChild(card);
            });

        } catch (error) {
            historyContainer.innerHTML = `<div class="loader" style="color: #ef4444;">Error: ${error.message}</div>`;
        }
    }
});