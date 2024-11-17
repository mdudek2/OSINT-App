(function() {
    const videoSection = document.querySelector('section');
    fetch('https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=25&playlistId=UUBi2mrWuNuyYy4gbM6fU18Q&key=AIzaSyAs39T0aXoadAJ_SMclizosX1cbPmhq8rU')
        .then(res => res.json())
        .then(data => { 
            data.items.forEach(element => {
                const videoId = element.snippet.resourceId.videoId;
                const thumbnail = element.snippet.thumbnails.default.url;
                const title = element.snippet.title; 
                const link = document.createElement('a');
                link.href = `https://www.youtube.com/watch?v=${videoId}`;
                link.innerHTML = `<img src="${thumbnail}" alt="${title}" /><h3>${title}</h3>`;
                videoSection.appendChild(link);
            });
        })
        .catch(err => {
            console.error(err);
        });

    //creates the map
    let map;

    function initMap() {
      map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 37.7749, lng: -122.4194 }, 
        zoom: 8,
      });
    }

    document.getElementById('fileInput').addEventListener('change', function(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
    
        reader.onload = function(e) {
            const content = e.target.result;
            const lines = content.split('\n');
            const locations = lines.map(line => {
                const [lat, lng] = line.split(',').map(Number);
                console.log(`Parsed location: Lat=${lat}, Lng=${lng}`); // Debugging
                return { lat, lng };
            });
    
            // Add markers for valid locations
            locations.forEach(location => {
                if (!isNaN(location.lat) && !isNaN(location.lng)) {
                    new google.maps.Marker({
                        position: location,
                        map: map,
                    });
                } else {
                    console.error('Invalid location:', location);
                }
            });
    
            // Center the map on the first location if valid
            if (locations.length > 0 && !isNaN(locations[0].lat) && !isNaN(locations[0].lng)) {
                map.setCenter(locations[0]);
            } else {
                console.error('No valid locations to center on.');
            }
        };
    
        reader.readAsText(file);
    });

    window.onload = initMap;
})();
