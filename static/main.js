document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('lookup-form');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const lookupValue = document.getElementById('lookup-value').value;
        const dataExtensions = document.querySelectorAll('.data-extension');

        dataExtensions.forEach((de) => {
            const externalKey = de.id.replace('de-', '');

            // Send request to backend for each data extension
            fetch('/lookup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    lookup_value: lookupValue,
                    external_key: externalKey
                })
            })
            .then(response => response.json())
            .then(data => {
                // Replace the placeholder with the retrieved data
                de.innerHTML = `<h2>${data.external_key}</h2><p>${JSON.stringify(data.data)}</p>`;
            })
            .catch(error => {
                de.innerHTML = `<h2>${externalKey}</h2><p>Error loading data</p>`;
            });
        });
    });
});