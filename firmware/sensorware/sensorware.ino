
#include <MemoryFree.h>

const int ledPin = 11;

unsigned int rpmcount = 0;
unsigned int last_send_time;
boolean hitsensor = false;
boolean sensorclear = false;

int circle_buff[10];
int cbuff_ptr = 0;
int sensorState;
boolean rpm_watch()
{
  sensorState = digitalRead(PIN_D4);
  if(sensorState == LOW)
  {
    hitsensor = true;
  }
  else
  {
    digitalWrite(ledPin, LOW);
    hitsensor = false;
    sensorclear = true;
  }
  
  if(hitsensor == true && sensorclear)
  {
    sensorclear = false;
    digitalWrite(ledPin, HIGH);
    rpmcount++;
    return true;
  }

  return false;
}

void setup() {
  Serial.begin(9600);      // open the serial port at 9600 bps:   
  
  pinMode(ledPin, OUTPUT);
  pinMode(PIN_D4, INPUT_PULLUP);
  
  rpmcount = 0;
  last_send_time = 0;
  
  cbuff_ptr = 0;
  for(int i=0; i < 10; i++) circle_buff[i] = 0;
}

int x = 0;
int SEND_RATE = 200;
int last_clear_time = 0;
int total_rpm = 0;
int i = 0;
elapsedMillis elapsedSinceSend;

void loop() {
  rpm_watch();
  if(elapsedSinceSend >= SEND_RATE)
  {
    circle_buff[cbuff_ptr] = rpmcount;
    
    total_rpm = 0;
    for(i=0; i < 10; i++) total_rpm += circle_buff[i];
    
    cbuff_ptr++;
    if(cbuff_ptr > 9) cbuff_ptr = 0;
 
    rpmcount = 0;
    
    //two seconds worth of sample points
    Serial.print("R");
    Serial.println(30*total_rpm);
    elapsedSinceSend = 0;
    
    
  } 
}
