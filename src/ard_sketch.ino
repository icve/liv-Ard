#include <LedControl.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// pin to sink LED current from 3.3 v source
#define motionSensor 5
#define motionLED 6
#define numOfDisplay 2
#define RELAY_PIN 7
#define CURRENT_SENSOR_PIN 0
#define MAX7219_DATA 2
#define MAX7219_CLOCK 3
#define MAX7219_CS 4
#define PHOTO_RESISTOR 1

LedControl lc(MAX7219_DATA, MAX7219_CLOCK, MAX7219_CS,numOfDisplay);
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
  lcd.print("STARTING");


}
void setup() {
    //motionSensor
    motSetup();
    //7 sevgment displays setup
    ssvgSetup();
    //lcd setup
    lcdSetup();

    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, HIGH);
    Serial.begin(9600);
}

void parseRun(String cmd){
    char func = cmd.charAt(0);
    switch (func){
        // i2c 16x2 charactors lcd api
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
            break;

        case 53:
            lcd.rightToLeft();
            break;

            // reserved for lcd 54 - 74

            //---------------
            // motionLogging
        case 75:
            // inverse byte to sink active-low LED
            digitalWrite(motionLED, !cmd.charAt(1));
            break;
        case 76:
            Serial.write(digitalRead(motionSensor));
            break;

            // -------------------------
            // 7 Segment display controll
            //character
        case 77:
            lc.setChar(cmd.charAt(1), cmd.charAt(2), cmd.charAt(3), cmd.charAt(4));
            break;
        case 78:
            lc.setDigit(cmd.charAt(1), cmd.charAt(2), cmd.charAt(3), cmd.charAt(4));
            break;

        case 79:
            lc.setRow(cmd.charAt(1), cmd.charAt(2), cmd.charAt(3));
            break;

        case 80:
            lc.setColumn(cmd.charAt(1), cmd.charAt(2), cmd.charAt(3));
            break;

        case 81:
            lc.setLed(cmd.charAt(1), cmd.charAt(2), cmd.charAt(3), cmd.charAt(4));
            break;

        case 82:
            lc.shutdown(cmd.charAt(1), cmd.charAt(2));
            break;

        case 83:
            lc.setIntensity(cmd.charAt(1), cmd.charAt(2));
            break;

            //clear
        case 84:
            lc.clearDisplay(cmd.charAt(1));
            break;

            // relay
        case 85:
            digitalWrite(RELAY_PIN, !cmd.charAt(1));
            break;

            // current sensor
        case 86:
            send_int(analogRead(CURRENT_SENSOR_PIN));
            break;

            // reset lcd matrix
        case 87:
        // temporary hack to fix signal corruption due to poor signal integrity
        // by reseting matrix device
                digitalWrite(MAX7219_CS, HIGH);
                // 1. turn on
                digitalWrite(MAX7219_CS, LOW);
                // turn on mtx
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0x0c);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0x01);
                digitalWrite(MAX7219_CS, HIGH);
                // no op for clock
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0);

                // 2. decode mode
                digitalWrite(MAX7219_CS, LOW);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0x09);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0x00);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0);
                digitalWrite(MAX7219_CS, HIGH);
                // 3. intensity
                digitalWrite(MAX7219_CS, LOW);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0x0a);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0x00);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0);
                digitalWrite(MAX7219_CS, HIGH);
                // 4. number of row (scan limit)
                digitalWrite(MAX7219_CS, LOW);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0x0b);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0x07);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0);
                shiftOut(MAX7219_DATA, MAX7219_CLOCK, MSBFIRST, 0);
                digitalWrite(MAX7219_CS, HIGH);
                break;
        case 88: 
                send_int(analogRead(PHOTO_RESISTOR));
                break;

        default:
            Serial.print("ERR");
            Serial.print(func);
            break;
    }
    Serial.flush();
}

void send_int(int i){
    byte l = (byte) i;
    byte h = i>>8;
    Serial.write(h);
    Serial.write(l);
}


void loop() {
    // put your main code here, to run repeatedly:
    if (Serial.available() > 0){
        parseRun(Serial.readStringUntil(';'));
    }


}
