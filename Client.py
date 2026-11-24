import json
import urllib.request
import urllib.error


def send_request(endpoint, data):

    json_data = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        f"http://localhost:8000{endpoint}",
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        error_data = json.loads(error.read().decode("utf-8"))
        print("Error:", error_data.get("error", "Request failed"))
        return None



city = input("Enter city: ")

location_response = send_request(
    "/locations",
    {"city": city}
)

if location_response is None:
    exit()

locations = location_response["locations"]

print("\nSelect a location:")

for index, location in enumerate(locations):
    print(
        index,
        location["name"],
        location.get("admin1"),
        location.get("country")
    )

try:
    choice = int(input("\nSelect your city number: "))

    if choice < 0 or choice >= len(locations):
        print("Invalid selection")
        exit()

except ValueError:
    print("Please enter a valid number")
    exit()

selected_location = locations[choice]

email = input("Enter email: ")

weather_response = send_request(
    "/weather",
    {
        "location": selected_location,
        "email": email
    }
)

if weather_response:
    print("\n", weather_response["message"])
    print(json.dumps(weather_response["weather"], indent=4))
