int RelayPin = 4;    // Digital Arduino Pin used to control the motor
String cmd = "";
 
// the setup routine runs once when you press reset:
void setup()  {
    // declare pin 5 to be an output:
    pinMode(RelayPin, OUTPUT);
    Serial.begin(9600);
    while (!Serial) {
      ; // wait for serial port to connect. Needed for native USB port only
    }
    Serial.println("Start state is ON. Waiting for relay cmd>");
    digitalWrite(RelayPin,HIGH); 

}


int read_command() { 
  int ch=0;
  while(Serial.available()>0) { 
    ch=Serial.read();
    //Serial.print("receive: ");
    //Serial.println(ch, DEC);
    if (isSpace(ch)) { 
      if (cmd.length()==0) { // Leading space, skip
        continue;
      } else { // Get word
        return 1; 
      }
    } else {
      cmd+=char(ch);  
    }   
  }
  return 0;  
}
 
// the loop routine runs over and over again forever:
void loop()  {
      if (read_command()) {
        if (cmd=="11") {  
          digitalWrite(RelayPin,HIGH);// NO3 and COM3 Connected (the motor is running)
          Serial.println("ON");
        } else if (cmd=="00") { 
          digitalWrite(RelayPin,LOW);// NO3 and COM3 Disconnected (the motor is not running)
          Serial.println("OFF");
        } else if (cmd.length()==0) {
          return;
        } else {
          Serial.print("Unknown cmd \'");
          Serial.print(cmd);
          Serial.println("\'");
        }
      cmd="";
    }
}

