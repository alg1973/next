 /*
  Created by Igor Jarc
 See http://iot-playground.com for details
 Please use community fourum on website do not contact author directly
 
 Code based on https://github.com/DennisSc/easyIoT-ESPduino/blob/master/sketches/ds18b20.ino
 
 External libraries:
 - https://github.com/adamvr/arduino-base64
 - https://github.com/milesburton/Arduino-Temperature-Control-Library
 
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.
 */
#include <ESP8266WiFi.h>
#include <Base64.h>
#include <OneWire.h>
#include <DallasTemperature.h>

//AP definitions
#define AP_SSID "dacha"
#define AP_PASSWORD "9166034125"

// EasyIoT server definitions
#define EIOT_USERNAME    "admin"
#define EIOT_PASSWORD    "test"
#define EIOT_IP_ADDRESS  "192.168.8.202"
#define EIOT_PORT        10003
#define EIOT_NODE        "t1"

#define REPORT_INTERVAL 60 // in sec

//CH340 driver for Mac works only this way: https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver
//in order to program esp8266 set port speed to 115200
//And port reset method to "modemcu"
//esp8266 d1 mini
//Data Signal connected to D4
//Ground(-) connected to G nearest to D4
//V(+) connected to 5U(V) Nearest to G

#define ONE_WIRE_BUS 2  // DS18B20 pin
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS18B20(&oneWire);


#define USER_PWD_LEN 40
char unameenc[USER_PWD_LEN];
float oldTemp;


void setup() {
  Serial.begin(115200);
  
  wifiConnect();
    
  memset(unameenc,0,sizeof(unameenc));
  String str = base64::encode(String(EIOT_USERNAME)+":"+String(EIOT_PASSWORD)); 
  str.toCharArray(unameenc, USER_PWD_LEN); 

  oldTemp = -1;
}

void loop() {
  float temp;
  
  do {
    DS18B20.requestTemperatures(); 
    temp = DS18B20.getTempCByIndex(0);
    Serial.print("Temperature: ");
    Serial.println(temp);
  } while (temp == 85.0 || temp == (-127.0));
  
  sendTeperature(temp);
  
  int cnt = REPORT_INTERVAL;
  
  while(cnt--)
    delay(1000);
}

void wifiConnect()
{
    Serial.print("Connecting to AP");
    WiFi.begin(AP_SSID, AP_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");  
}

void sendTeperature(float temp)
{  
   WiFiClient client;
   
   while(!client.connect(EIOT_IP_ADDRESS, EIOT_PORT)) {
    Serial.println("connection failed");
    wifiConnect(); 
  }
 
  String url = "";
  url += "/set/thermometer?t="+ String(EIOT_NODE) + "&v="+String(temp); // t=[term_name], v=[teperature]

  Serial.print("POST data to URL: ");
  Serial.println(url);
  
  client.print(String("GET ") + url + " HTTP/1.0\r\n" +
               "Host: " + String(EIOT_IP_ADDRESS) + "\r\n" + 
               "Connection: close\r\n" + 
               "Authorization: Basic " + unameenc + " \r\n" + 
               "Content-Length: 0\r\n" + 
               "\r\n");

  delay(100);
    while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
  
  Serial.println();
  Serial.println("Connection closed");
}


