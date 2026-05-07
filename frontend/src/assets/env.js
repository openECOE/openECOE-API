(function(window) {
  window["env"] = window["env"] || {};
  
  
  var _api_location = "http://localhost:5001"; // El puerto de la API
  var _chrono_location = "http://localhost:5002"; // El puerto del Chrono

  // Environment variables
  window["env"]["debug"] = false;
  window["env"]["backUrl"] = _api_location;
  window["env"]["apiUrl"] = _api_location + "/backend";
  window["env"]["chronoUrl"] = _chrono_location; // Apunta al 5002 directamente  
})(this);