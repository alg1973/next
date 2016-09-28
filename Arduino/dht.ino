#include "DHT.h"

DHT dht;

void setup()
{
  Serial.begin(9600);

  dht.setup(2); // data pin 2
}

void loop()
{
  delay(dht.getMinimumSamplingPeriod());
  while (Serial.read() != '\n') {  
          ; 
  }   
  

  Serial.print(dht.getHumidity());
  Serial.print("\t");
  Serial.print(dht.getTemperature());
  Serial.print("\n");
}
