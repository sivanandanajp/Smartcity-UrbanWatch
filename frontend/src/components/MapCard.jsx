import { useMemo } from "react";

import Map, {
  Marker
} from "react-map-gl/maplibre";

import "maplibre-gl/dist/maplibre-gl.css";

import "../styles/mapcard.css";

function MapCard({ selectedJunction }) {

  const junctionCoordinates = {

    "Attakulangara JN":
      { lat: 8.4775, lon: 76.9505 },

    "Chanthavila":
      { lat: 8.6035, lon: 76.9185 },

    "Chenkottukonam Jn":
      { lat: 8.5710, lon: 76.8880 },

    "JAGATHY":
      { lat: 8.5068, lon: 76.9710 },

    "Kaimanam Jn":
      { lat: 8.4630, lon: 76.9590 },

    "Karakkamandapam Jn":
      { lat: 8.4705, lon: 76.9670 },

    "Kazhakkoottam Jn":
      { lat: 8.5585, lon: 76.8755 },

    "Kesavadasapuram JN":
      { lat: 8.5275, lon: 76.9435 },

    "Kizhakke Mukkola":
      { lat: 8.5490, lon: 76.9900 },

    "Kundamankadavu":
      { lat: 8.4820, lon: 76.9950 },

    "MANNATHALLA":
      { lat: 8.5860, lon: 76.9500 },

    "Mankuzhy":
      { lat: 8.5050, lon: 76.9300 },

    "Nemom Jn":
      { lat: 8.4515, lon: 76.9720 },

    "PATTOOR":
      { lat: 8.4935, lon: 76.9490 },

    "Pappanamcode Jn":
      { lat: 8.4715, lon: 76.9605 },

    "Poojapura Jn":
      { lat: 8.4890, lon: 76.9780 },

    "Poonkulam Jn":
      { lat: 8.4450, lon: 76.9850 },

    "STATUE NORTH":
      { lat: 8.4923, lon: 76.9478 },

    "Shangumugham Jn":
      { lat: 8.4825, lon: 76.9120 },

    "Statue South":
      { lat: 8.4900, lon: 76.9480 },

    "Thirumala JN":
      { lat: 8.5015, lon: 76.9915 },

    "VJT JN":
      { lat: 8.4915, lon: 76.9495 },

    "Veli Bridge Rd":
      { lat: 8.5060, lon: 76.8960 },

    "Vellayambalam":
      { lat: 8.5100, lon: 76.9600 },

    "Vellayani Jn":
      { lat: 8.4275, lon: 76.9990 }

  };

  const location = useMemo(() => {

    return (
      junctionCoordinates[selectedJunction]
      ||
      {
        lat: 8.5241,
        lon: 76.9366
      }
    );

  }, [selectedJunction]);

  return (

    <div className="map-card">

      <h2>
        Traffic Overview
      </h2>

      <Map

        key={selectedJunction}

        initialViewState={{

          longitude: location.lon,

          latitude: location.lat,

          zoom: 15

        }}

        style={{
          width: "100%",
          height: "700px"
        }}

        mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"

      >

        <Marker

          longitude={location.lon}

          latitude={location.lat}

          anchor="center"

        >

          <div
            className="junction-marker"
          />

        </Marker>

      </Map>

    </div>

  );
}

export default MapCard;