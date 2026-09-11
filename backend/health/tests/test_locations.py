from unittest.mock import Mock, patch
import requests
from django.test import SimpleTestCase
from rest_framework.test import APIClient

class LocationUnitTests(SimpleTestCase):
    def test_geocode_requires_query(self):
        self.assertEqual(APIClient().get("/api/locations/geocode/").status_code, 400)

    @patch("health.views.requests.get")
    def test_geocode_success(self, m):
        r=Mock(); r.raise_for_status.return_value=None; r.json.return_value=[{"lat":"22.3072","lon":"73.1812","display_name":"Vadodara, India"}]; m.return_value=r
        x=APIClient().get("/api/locations/geocode/?q=Vadodara"); self.assertEqual(x.status_code,200); self.assertEqual(x.data["lat"],22.3072); self.assertEqual(x.data["lng"],73.1812)

    @patch("health.views.requests.get")
    def test_geocode_failure_returns_502(self,m):
        m.side_effect=requests.RequestException("down")
        self.assertEqual(APIClient().get("/api/locations/geocode/?q=Vadodara").status_code,502)

    def test_nearby_requires_coordinates(self):
        self.assertEqual(APIClient().get("/api/locations/nearby/").status_code,400)

    def test_nearby_rejects_invalid_coordinates(self):
        self.assertEqual(APIClient().get("/api/locations/nearby/?lat=100&lng=73").status_code,400)

    @patch("health.views.requests.post")
    def test_nearby_parses_node_and_way(self,m):
        r=Mock(); r.raise_for_status.return_value=None; r.json.return_value={"elements":[{"type":"node","lat":22.30,"lon":73.18,"tags":{"name":"Test Clinic","amenity":"clinic"}},{"type":"way","center":{"lat":22.31,"lon":73.19},"tags":{"name":"Test Hospital","amenity":"hospital","phone":"123"}}]}; m.return_value=r
        x=APIClient().get("/api/locations/nearby/?lat=22.30&lng=73.18"); self.assertEqual(x.status_code,200); self.assertEqual(len(x.data["results"]),2); self.assertEqual(x.data["results"][1]["phone"],"123")

    @patch("health.views.requests.post")
    def test_nearby_network_failure_returns_503(self,m):
        m.side_effect=requests.RequestException("network down")
        self.assertEqual(APIClient().get("/api/locations/nearby/?lat=22.30&lng=73.18").status_code,503)
