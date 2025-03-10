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

function updateTariff() {
    const routeId = document.getElementById('routeSelect').value;
    const receivingPointSelect = document.getElementById('receivingPointSelect');

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
                document.getElementById('tariff_display').textContent = `${data.tariff} TND`;
                receivingPointSelect.innerHTML = '<option value="">Select Receiving Point</option>';
                data.receiving_points.forEach(point => {
                    const option = document.createElement('option');
                    option.value = point.id;
                    option.textContent = point.name;
                    receivingPointSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error loading tariff:', error);
                alert('Failed to load tariff. Please try again later.');
            });
    } else {
        document.getElementById('tariff_display').textContent = '--';
        receivingPointSelect.innerHTML = '<option value="">Select Receiving Point</option>';
    }
}