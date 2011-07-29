//#include <stdio.h> // for size_t
//#include <stdlib.h>

//#pragma library c

#define DEC 10
#define HEX 16
#define OCT 8
#define BIN 2
#define BYTE 0

// run led pin
#define RUNLED PORTAbits.RA4

// commands
#define LCD_CLEARDISPLAY 0x01
#define LCD_RETURNHOME 0x02
#define LCD_ENTRYMODESET 0x04
#define LCD_DISPLAYCONTROL 0x08
#define LCD_CURSORSHIFT 0x10
#define LCD_FUNCTIONSET 0x20
#define LCD_SETCGRAMADDR 0x40
#define LCD_SETDDRAMADDR 0x80

// flags for display entry mode
#define LCD_ENTRYRIGHT 0x00
#define LCD_ENTRYLEFT 0x02
#define LCD_ENTRYSHIFTINCREMENT 0x01
#define LCD_ENTRYSHIFTDECREMENT 0x00

// flags for display on/off control
#define LCD_DISPLAYON 0x04
#define LCD_DISPLAYOFF 0x00
#define LCD_CURSORON 0x02
#define LCD_CURSOROFF 0x00
#define LCD_BLINKON 0x01
#define LCD_BLINKOFF 0x00

// flags for display/cursor shift
#define LCD_DISPLAYMOVE 0x08
#define LCD_CURSORMOVE 0x00
#define LCD_MOVERIGHT 0x04
#define LCD_MOVELEFT 0x00

// flags for function set
#define LCD_8BITMODE 0x10
#define LCD_4BITMODE 0x00
#define LCD_2LINE 0x08
#define LCD_1LINE 0x00
#define LCD_5x10DOTS 0x04
#define LCD_5x8DOTS 0x00

u8 _rs_pin = 8; // LOW: command.  HIGH: character.
u8 _rw_pin = -1; // LOW: write to LCD.  HIGH: read from LCD.
u8 _enable_pin = 9; // activated by a HIGH pulse.
u8 _data_pins[8];

u8 _displayfunction;
u8 _displaycontrol;
u8 _displaymode;

u8 _initialized;

u8 _numlines,_currline;

void lcd(u8 rs, u8 enable, u8 d0, u8 d1, u8 d2, u8 d3, 
			u8 d4, u8 d5, u8 d6, u8 d7);
void init(u8 fourbitmode, u8 rs, u8 rw, u8 enable, 
			u8 d0, u8 d1, u8 d2, u8 d3,
			u8 d4, u8 d5, u8 d6, u8 d7);
void begin(u8 lines, u8 dotsize);
void noAutoscroll(void);
void autoscroll(void);
void rightToLeft(void);
void leftToRight(void);
void scrollDisplayRight(void);
void scrollDisplayLeft(void);
void blink();
void noBlink();
void cursor();
void noCursor();
void display();
void noDisplay();
void clear();
void home();
void printNumber(u16 n, u8 base);
void printFloat(float number, u8 digits);
void lcdPrint(char *string);
void setCursor(u8 col, u8 row);
void command(uchar value);
void write(uchar value);
void send(u8 value, u8 mode);
void write8bits(u8 value);
void write4bits(u8 value);
void pulseEnable(void);
