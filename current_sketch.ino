#include "LedControl.h"

#define motionSensor 5
#define motionLED 6
LedControl lc=LedControl(2,3,4,1);


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
      case 'b':
        // inverse byte to sink active-low LED
        digitalWrite(motionLED, !cmd.charAt(1));
      break;
      case 'm':
        Serial.write(digitalRead(motionSensor));
      break;
      // 7 Segment display controll
      //character
      case 'a':
         lc.setChar(0, char2i(cmd.charAt(1)), cmd.charAt(2), char2i(cmd.charAt(3)));
      break;
      //digit d0F1 (digit)(value)(dot)
      case 'd':
         lc.setDigit(0, char2i(cmd.charAt(1)), strtol(cmd.substring(2,3).c_str(), NULL, 16), cmd.charAt(3) - '0');
      break;

      case 'r': 
         lc.setRow(0, char2i(cmd.charAt(1)), strtol(cmd.substring(2).c_str(), NULL, 16));
      break;

      case 'c':
         lc.setColumn(0, char2i(cmd.charAt(1)), strtol(cmd.substring(2).c_str(), NULL, 16));
      break;

      case 'l': 
         lc.setLed(0, char2i(cmd.charAt(1)), char2i(cmd.charAt(2)), char2i(cmd.charAt(3)));
      break;
      case 's':
            //int state = cmd.chatAt(1).
            lc.shutdown(0, char2i(cmd.charAt(1)));
            lc.setDigit(0, 1, 10, true);
        break;
      
       //intensity
        case 'i':
           lc.setIntensity(0, cmd.substring(1).toInt());
        break;

      //clear
      case '0':
        lc.clearDisplay(0);
        break;
            
         default:
            Serial.println(char2i(cmd.charAt(1)));
         break;
    }
}


void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available() > 0){
        parseRun(Serial.readStringUntil(';'));
    }

    
}
