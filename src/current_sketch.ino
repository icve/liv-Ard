#include "LedControl.h"

#define motionSensor 5
#define motionLED 6
#define numOfDisplay 2
LedControl lc=LedControl(2,3,4,numOfDisplay);


void setup() {
  // put your setup code here, to run once:
    // pin to sink LED current from 3.3 v source
    pinMode(motionLED, OUTPUT);
    digitalWrite(motionLED, HIGH);
    pinMode(motionSensor, INPUT);
    lc.shutdown(0, false);
    lc.setIntensity(0, 0);
    lc.clearDisplay(0);
    lc.setDigit(0, 2, 10, true);
    Serial.begin(9600);
    
}

int char2i(char x){
   return x - '0';
}

void parseRun(String cmd){
    char func = cmd.charAt(0);
    switch (func){
      //---------------
      // motionLogging
      case 'b':
        // inverse byte to sink active-low LED
        digitalWrite(motionLED, !cmd.charAt(1));
      break;
      case 'm':
        Serial.write(digitalRead(motionSensor));
      break;

      // -------------------------
      // 7 Segment display controll
      //character
      case 'a':
         lc.setChar(char2i(cmd.charAt(1)), char2i(cmd.charAt(2)), cmd.charAt(3), char2i(cmd.charAt(4)));
      break;
      //digit d0F1 (digit)(value)(dot)
      case 'd':
         lc.setDigit(char2i(cmd.charAt(1)), char2i(cmd.charAt(2)), strtol(cmd.substring(3,4).c_str(), NULL, 16), cmd.charAt(4) - '0');
      break;

      case 'r': 
         lc.setRow(char2i(cmd.charAt(1)), char2i(cmd.charAt(2)), strtol(cmd.substring(3).c_str(), NULL, 16));
      break;

      case 'c':
         lc.setColumn(char2i(cmd.charAt(1)), char2i(cmd.charAt(2)), strtol(cmd.substring(3).c_str(), NULL, 16));
      break;

      case 'l': 
         lc.setLed(char2i(cmd.charAt(1)), char2i(cmd.charAt(2)), char2i(cmd.charAt(3)), char2i(cmd.charAt(4)));
      break;
      case 's':
            //int state = cmd.chatAt(2).
            lc.shutdown(char2i(cmd.charAt(1)), char2i(cmd.charAt(2)));
            lc.setDigit(char2i(cmd.charAt(1)), 1, 10, true);
        break;
      
       //intensity
        case 'i':
           lc.setIntensity(char2i(cmd.charAt(1)), cmd.substring(2).toInt());
        break;

      //clear
      case '0':
        lc.clearDisplay(char2i(cmd.charAt(1)));
        break;
            
         default:
            Serial.println(char2i(cmd.charAt(2)));
         break;
    }
}


void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available() > 0){
        parseRun(Serial.readStringUntil(';'));
    }

    
}
