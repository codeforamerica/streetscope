// Create map object
window.MapBuilder = {};

// initialize map
MapBuilder.init = function(id) {
  // Create map container
  var leafletMap = L.mapbox.map(id, 'codeforamerica.jfnj92nm', {maxZoom: 17, minZoom: 10, accessToken: 'pk.eyJ1IjoiY29kZWZvcmFtZXJpY2EiLCJhIjoiSTZlTTZTcyJ9.3aSlHLNzvsTwK-CYfZsG_Q'}).setView([37.75,-122.43], 12);

  // Make layer group
  var addresses = L.layerGroup();

  return {
    addToMap: function (data) {
      addresses.clearLayers();
      var geoJsonResults = L.geoJson(data, {
        onEachFeature: function(feature, layer) {
          layer.bindPopup(feature.properties.formatted_address);
        }
      });
      addresses.addLayer(geoJsonResults).addTo(leafletMap);
    }
  }
}
