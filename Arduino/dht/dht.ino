#include "DHT.h"

DHT dht;
int session_count=0;

void setup()
{
  Serial.begin(9600);

  dht.setup(2,DHT::DHT11); // data pin 2
  delay(dht.getMinimumSamplingPeriod());
}

void loop()
{
  /* delay(dht.getMinimumSamplingPeriod()); */
  int ch=0;
  do {
    ch=Serial.read();
    if (ch=='\r' || ch=='\n') {
      while (Serial.available()>0) {
        Serial.read();
        } 
        break;
      }   
    } while (1); 
  
  Serial.print(dht.getTemperature());
  Serial.print("\t");
  Serial.print(dht.getHumidity());
  Serial.print("\t");
  Serial.print(session_count);
  Serial.print("\n");
  session_count++;
}
