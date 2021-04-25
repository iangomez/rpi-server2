// ESP8266 NodeMCU (ESP-12E)
// https://www.electronicshub.org/connect-esp8266-to-wifi/
// https://lastminuteengineers.com/esp8266-ota-updates-arduino-ide/

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>

// WiFi the ESP connects to
const char* ssid = "Little Wood";  // Enter SSID here
const char* password = "dummy";  //Enter Password 

// Server on WiFi we want to send outgoing POST requests to
String serverName = "http://192.168.1.121:5000/shower";

// Reporting interval and output data (temperature)
unsigned long previousMillis = 0;  // will store last time LED was updated
long intervalOn = 1000;     // interval at which to report while on (milliseconds)
long intervalOff = 12000;   // slower interval ~2 minutes
long interval = intervalOn; // current interval
float temperatureF = 0;

void handleRoot();              // function prototypes for HTTP handlers
void handleReporting();
void handleNotFound();

// Set up a small webserver to listen for incoming POST requests
ESP8266WebServer server(80);    // Create a webserver object that listens for HTTP request on port 80

void setup() {
  Serial.begin(115200);
 
  // Connect to WiFi
  Serial.println("Connecting to Wifi.."); 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
     delay(500);
     Serial.print("*");
  }

  // Set up code for Over The Air (OTA) updates
  // Port defaults to 8266
  ArduinoOTA.setPort(8266);

  // Hostname defaults to esp8266-[ChipID]
  ArduinoOTA.setHostname("esp8266-shower-temp");

  // No authentication by default
//  ArduinoOTA.setPassword("deadhorse123");

  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH)
      type = "sketch";
    else // U_SPIFFS
      type = "filesystem";

    // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
    Serial.println("Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });
  ArduinoOTA.begin();
  
  
  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());


  server.on("/", HTTP_GET, handleRoot);     // Call the 'handleRoot' function when a client requests URI "/"
  server.on("/reporting", HTTP_POST, handleReporting);  // Call the 'handleLED' function when a POST request is made to URI "/reporting"
  server.onNotFound(handleNotFound);        // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"

  server.begin();                           // Actually start the server
  Serial.println("HTTP server started");
}

void loop() {
  ArduinoOTA.handle();    // Listen for OTA requests
  server.handleClient();  // Listen for HTTP requests from clients
  getTemp();              // Get temperature data from TMP36 sensor
  postData();             // POST data to raspberry pi
}


// Get data from TMP36 sensor and modify the temperatureF global variable directly
void getTemp() {
  // converting that reading to voltage
  int tmpValue = analogRead(A0);  
  float voltage = tmpValue * 3.3;
  voltage = voltage / 1024.0;

  // converting from 10 mv per degree wit 500 mV offset to degrees ((voltage - 500mV) times 100)
  float temperatureC = (voltage - 0.5) * 100 ;    
  temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;  //now convert to Fahrenheit
}

// Send a post request to our specified server location
void postData() {
  
  // timer that allows the ESP to be responsive to OTA requests
  unsigned long currentMillis = millis();
  unsigned long diff  = currentMillis - previousMillis;
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    // POST request  
    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
      
      HTTPClient http;             //Declare object of class HTTPClient
      http.begin(serverName);      //Specify request destination
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");  //Specify content-type header
      int httpCode = http.POST("temperature=" + String(temperatureF));   //Send the request
      String payload = http.getString(); //Get the response payload

//      Serial.print("http code: ");
//      Serial.println(httpCode);   //Print HTTP return code
//      Serial.println(payload);    //Print request response payload
   
      http.end();  //Close connection
    
     } else {
      Serial.println("Error in WiFi connection");
    }
  }
}

void handleRoot() {                         // When URI / is requested, send a web page with a button to toggle the LED
  Serial.println("Index accessed");
  server.send(200, "text/html", "<form action=\"/reporting\" method=\"POST\"><input type=\"submit\" value=\"Toggle reporting\"></form>");
}

void handleReporting() {                          // If a POST request is made to URI /LED
  Serial.println("Post request to reporting");
  if (interval==intervalOn) {
    Serial.println("Switch to slow reporting");
    interval = intervalOff;
  } else {
    Serial.println("Switch to fast reporting");
    interval = intervalOn;
  }
  
  server.sendHeader("Location","/");        // Add a header to respond with a new location for the browser to go to the home page again
  server.send(303);                         // Send it back to the browser with an HTTP status 303 (See Other) to redirect
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found"); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}
