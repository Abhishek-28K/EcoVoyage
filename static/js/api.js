$(document).ready(function() {
const API_KEY = 'pk.8c9f36b3cfd8974de4ea7379ee5fac2a';
const baseUrl = 'https://api.locationiq.com/v1/autocomplete.php';
const limit = 5;

function autocomplete(selector) {
    $(selector).autocomplete({
        serviceUrl: baseUrl,
        params: {
            key: API_KEY,
            limit: limit,
        },
        paramName: 'q',
        transformResult: function(response) {
            return {
                suggestions: $.map(JSON.parse(response), function(item) {
                    return { 
                        value: item.display_name,
                        data: { 
                            lat: item.lat, 
                            lon: item.lon 
                        } 
                    };
                })
            };
        },
        onSelect: function (suggestion) {
            $(selector).data('lat', suggestion.data.lat);
            $(selector).data('lon', suggestion.data.lon);
        }
    });
}

autocomplete('#search-box-source');
autocomplete('#search-box-destination');

$('#distance-form').submit(function(event) {
    event.preventDefault(); // Prevent the default form submission

    const source = $('#search-box-source').val();
    const destination = $('#search-box-destination').val();
    const sourceLat = $('#search-box-source').data('lat');
    const sourceLon = $('#search-box-source').data('lon');
    const destinationLat = $('#search-box-destination').data('lat');
    const destinationLon = $('#search-box-destination').data('lon');
    const date = $('#date').val();
    const timeTaken = $('#time-taken').val();
    const is_electric = $('input[name="is_electric"]:checked').val();
    const modeOfTransport = $('#mode-of-transport').val();

    if (sourceLat && sourceLon && destinationLat && destinationLon) {
        const coordinates = `${sourceLon},${sourceLat};${destinationLon},${destinationLat}`;
        const url = `https://us1.locationiq.com/v1/directions/driving/${coordinates}?key=${API_KEY}&alternatives=false&steps=true&geometries=geojson&overview=full&annotations=true`;

        $.get(url, function(response) {
            const distance = response.routes[0].distance / 1000; // Convert meters to kilometers
            const distanceFormatted = distance.toFixed(2);

            $.ajax({
                url: storeDistanceDataUrl, // Use Django URL tag
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}' // CSRF token header
                },
                contentType: 'application/json',
                data: JSON.stringify({
                    source: source,
                    destination: destination,
                    source_lat: sourceLat,
                    source_lon: sourceLon,
                    destination_lat: destinationLat,
                    destination_lon: destinationLon,
                    distance: distanceFormatted,
                    date: date,
                    time_taken: timeTaken,
                    is_electric: is_electric,
                    mode_of_transport: modeOfTransport
                }),
                success: function(response) {
                    location.reload();
                },
                error: function() {
                    alert('Error storing data. Please try again.');
                }
            });
        }).fail(function() {
            alert('Error calculating distance. Please try again.');
        });
    } else {
        alert('Please select valid source and destination locations.');
    }
});
});