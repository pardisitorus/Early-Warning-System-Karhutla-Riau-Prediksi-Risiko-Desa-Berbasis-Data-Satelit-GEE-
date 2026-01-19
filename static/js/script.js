document.addEventListener('DOMContentLoaded', function() {
    // Initialize map
    var map = L.map('map').setView([0.5, 101.5], 7); // Center on Riau

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    var markers = [];

    document.getElementById('predict-form').addEventListener('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Clear previous markers
            markers.forEach(marker => map.removeLayer(marker));
            markers = [];

            // Clear village list
            var villageList = document.getElementById('village-list');
            villageList.innerHTML = '';

            // Determine notification level
            var hasDanger = data.some(v => v.level === 'Danger');
            var hasWarning = data.some(v => v.level === 'Warning');
            var notificationText = '';
            if (hasDanger) {
                notificationText = 'Level Merah (Danger): Aktivasi regu pemadam desa dan larangan pembakaran total.';
            } else if (hasWarning) {
                notificationText = 'Level Kuning (Warning): Patroli rutin di lahan gambut serta pemantauan tinggi muka air tanah akibat kondisi vegetasi yang kering dan suhu ekstrem.';
            } else {
                notificationText = 'Level Hijau (Safe): Tidak ada instruksi khusus.';
            }
            document.getElementById('notification-text').textContent = notificationText;

            // Add markers and list items
            data.forEach(function(village) {
                var color = village.prob > 0.8 ? 'red' : (village.prob >= 0.64 ? 'yellow' : 'green');
                var marker = L.circleMarker([village.lat, village.lon], {
                    color: color,
                    fillColor: color,
                    fillOpacity: 0.5,
                    radius: 5
                }).addTo(map);
                marker.bindPopup(`<b>${village.name}</b><br>Prob: ${village.prob}<br>Level: ${village.level}`);
                markers.push(marker);

                var listItem = document.createElement('div');
                listItem.className = 'p-2 border-b border-gray-200';
                listItem.innerHTML = `<strong>${village.name}</strong> - Prob: ${village.prob} - ${village.level}<br><small>${village.instructions}</small>`;
                villageList.appendChild(listItem);
            });

            // Fit map to markers
            if (markers.length > 0) {
                var group = new L.featureGroup(markers);
                map.fitBounds(group.getBounds());
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
