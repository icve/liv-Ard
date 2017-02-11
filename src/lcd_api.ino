#include <Wire.h>  // Comes with Arduino IDE
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);


void setup()   /*----( SETUP: RUNS ONCE )----*/
{
  Serial.begin(9600);  // Used to type in characters

  lcd.begin(16,2);   // initialize the lcd for 16 chars 2 lines, turn on backlight

  lcd.print("HELLO");

  
}/*--(end setup )---*/


void loop()  {

if (Serial.available() > 1){
	   
    lcdparse(Serial.readStringUntil(';'));
}
}

void lcdparse(String cmd){
	byte func = cmd.charAt(0);
	switch (func){
		
		case 32:
			lcd.setCursor(cmd.charAt(1), cmd.charAt(2));
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


	}

}

