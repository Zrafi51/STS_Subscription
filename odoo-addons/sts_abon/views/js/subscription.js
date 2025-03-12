function updateTariff() {
    const routeId = document.getElementById('routeSelect').value;

    if (routeId) {
        fetch(`/api/route/tariff?route_id=${routeId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error('Error:', data.error);
                    alert('Error fetching tariff: ' + data.error);
                    return;
                }
                // Update the tariff display
                document.getElementById('tariff_display').textContent = `${data.tariff} TND`;
            })
            .catch(error => {
                console.error('Error loading tariff:', error);
                alert('Failed to load tariff. Please try again later.');
            });
    } else {
        // If no route is selected, reset the tariff display
        document.getElementById('tariff_display').textContent = '--';
    }
}

// Load routes when the page is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Loading routes...');
    fetch('/api/routes')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Routes loaded:', data.routes);
            const routeSelect = document.getElementById('routeSelect');
            routeSelect.innerHTML = '<option value="">Select Route</option>';
            data.routes.forEach(route => {
                const option = document.createElement('option');
                option.value = route.id;
                option.textContent = route.departure_stop_id.name + ' → ' + route.arrival_stop_id.name;
                routeSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading routes:', error);
            alert('Failed to load routes. Please try again later.');
        });
});