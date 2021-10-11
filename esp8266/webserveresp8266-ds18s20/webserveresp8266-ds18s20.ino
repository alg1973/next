#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
//#include <WiFi.h>
#include <ESP8266WiFi.h>
 
const char* ssid = "dacha";
//const char* ssid = "sliz";
const char* password = "9166034125";


//Pin 5(GPIO5) corrensponds to scl/d1 in wemos d1 r2, 4(GPIO4) is d2 
//https://cyaninfinite.com/getting-started-with-the-wemos-d1-esp8266-wifi-board/

/*
 * for wemos d1
#define DHTPIN 5
#define ONE_WIRE_PIN 4
 * this for esp8622
#define DHTPIN 2
#define ONE_WIRE_PIN 3
*/
//For the nodeMCU v2 one_wire_pin 5 it's d1 on nodeMCU
#define DHTPIN 6
#define ONE_WIRE_PIN 4



#define DHTTYPE DHT11 

//int LED_BUILTIN = 26;
//DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_PIN);
DallasTemperature sensors(&oneWire);

WiFiServer server(80);

//IPAddress ip(192, 168, 8, 250); // where xx is the desired IP Address
//IPAddress gateway(192, 168, 8, 1); // set gateway to match your network

IPAddress ip(192, 168, 8, 251); // where xx is the desired IP Address
IPAddress gateway(192, 168, 8, 1); // set gateway to match your network
 
void setup() {
  ESP.wdtDisable();
  ESP.wdtEnable(5500);
  Serial.begin(115200);
  delay(10);
 
  pinMode(LED_BUILTIN, OUTPUT);

  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  IPAddress subnet(255, 255, 255, 0); // set subnet mask to match your network
  WiFi.config(ip, gateway, subnet); 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL : ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
  digitalWrite(LED_BUILTIN, HIGH);
  sensors.begin();  
}

bool dht_inited = false;

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
 
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  client.flush();
  Serial.println(request);
  digitalWrite(LED_BUILTIN, LOW);   // Turn the LED on (Note that LOW is the voltage level
  // but actually the LED is on; this is because
  // it is active low on the ESP-01)
        
  // Match the request
 Serial.print("Reading temp...");
 sensors.requestTemperatures();
 delay(200);
 float t = sensors.getTempCByIndex(0); 
 float h = 0.0;
 
 if (isnan(t)) 
 {
    Serial.println("Failed to read from DHT or 1wire sensor!");
    t = -128;
  }
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" degrees Celsius Humidity: ");
  Serial.println(h);
  // Return the response
  client.println("HTTP/1.0 200 OK");
  client.println("Content-Type: text/text");
  client.print("\r\n\r\n"); //  do not forget this one
  
  String s = "";
  s += String(t);
  s += " ";
  s += String(h);
  client.println(s);
  //delay(1);
  //Serial.println("Client disconnected");
  //Serial.println("");
  delay(500);                      // Wait for a second
  digitalWrite(LED_BUILTIN, HIGH);  // Turn the LED off by making the voltage HIGH
  //client.flush();
  //client.stop();
}
