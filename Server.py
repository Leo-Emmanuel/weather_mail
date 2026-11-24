from http.server import BaseHTTPRequestHandler, HTTPServer
from weather import search_locations, get_city_weather
from email_service import send_weather_email
import json


class Myserver(BaseHTTPRequestHandler):

    def do_POST(self):

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        received_data = json.loads(body)

        if self.path == "/locations":

            city = received_data.get("city")

            locations = search_locations(city)

            if not locations:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response = {"error": "City not found"}
                self.wfile.write(json.dumps(response).encode())
                return

            response_data = {
                "message": "Locations found",
                "locations": locations
            }

        elif self.path == "/weather":

            location = received_data.get("location")
            email = received_data.get("email")

            if not location or not email:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response = {"error": "Location and email are required"}
                self.wfile.write(json.dumps(response).encode())
                return

            weather_result = get_city_weather(location)

            try:
                send_weather_email(email, weather_result)

            except Exception as error:
                print("Email error:", error)

                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response = {"error": "Failed to send weather email"}
                self.wfile.write(json.dumps(response).encode())
                return

            print("Weather:", weather_result)
            print("Email sent to:", email)

            response_data = {
                "message": "Weather report sent successfully",
                "weather": weather_result
            }

        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response_data).encode())


server = HTTPServer(("localhost", 8000), Myserver)

print("Server running on port 8000")

server.serve_forever()
