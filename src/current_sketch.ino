#include "LedControl.h"
#include <Wire.h>  // Comes with Arduino IDE
#include <LiquidCrystal_I2C.h>

// pin to sink LED current from 3.3 v source
#define motionSensor 5
#define motionLED 6
#define numOfDisplay 2
LedControl lc=LedControl(2,3,4,numOfDisplay);
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

//7svg serup
void ssvgSetup(){
    lc.shutdown(0, false);
    lc.setIntensity(0, 0);
    lc.clearDisplay(0);
    lc.setDigit(0, 2, 10, true);

}

void motSetup(){
    pinMode(motionLED, OUTPUT);
    digitalWrite(motionLED, HIGH);
    pinMode(motionSensor, INPUT);
}

void lcdSetup(){
    lcd.begin(16,2);
    lcd.print("HELLO");


}
void setup() {
    //motionSensor
    motSetup();
    //7 sevgment displays setup
    ssvgSetup();
    //lcd setup
    lcdSetup();

    Serial.begin(9600);


}

void lcdParse(String cmd){

    byte func = cmd.charAt(0);
    switch (func){

        case 32:
            lcd.setCursor(cmd.charAt(1) - 1, cmd.charAt(2) - 1);
            break;

        case 33:
            lcd.print(cmd.substring(1));
            break;

        case 34:
            lcd.backlight();
            break;

        case 35:
            lcd.noBacklight();
            break;

        case 36:
            lcd.blink();
            break;

        case 37:
            lcd.noBlink();
            break;

        case 38:
            lcd.cursor();
            break;

        case 39:
            lcd.noCursor();
            break;

        case 40:
            lcd.clear();
            break;

        case 41:
            lcd.home();
            break;

        case 42:
            lcd.moveCursorLeft();
            break;

        case 43:
            lcd.moveCursorRight();
            break;

        case 44:
            lcd.autoscroll();
            break;

        case 45:
            lcd.noAutoscroll();
            break;

        case 46:
            lcd.on();
            break;

        case 47:
            lcd.off();
            break;

        case 48:
            lcd.display();
            break;

        case 49:
            lcd.noDisplay();
            break;

        case 50:
            lcd.scrollDisplayLeft();
            break;

        case 51:
            lcd.scrollDisplayRight();
            break;

        case 52:
            lcd.leftToRight();

        case 53:
            lcd.rightToLeft();
            break;


    }}


int char2i(char x){
    return x - '0';
}

void parseRun(String cmd){
    char func = cmd.charAt(0);
    switch (func){
        // i2c 16x2 charactors lcd api
        case 'x':
            lcdParse(cmd.substring(1));
            break;
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
