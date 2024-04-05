#include <Servo.h>

Servo pan_servo;
Servo tilt_servo;

int center_x;
int center_y;
int error_pan;
int error_tilt;

int pixel_x=240;
int pixel_y=320;

int pan_pos = 90;  
int tilt_pos = 90;  

void setup() 
{
  pan_servo.attach(9); 
  tilt_servo.attach(10); 
  pan_servo.write(90); 
  tilt_servo.write(90); 
  Serial.begin(9600);
}



void loop()
{
  if (Serial.available() > 0) 
    {
   
        String data = Serial.readStringUntil('\n');
        int commaIndex = data.indexOf(',');
        String xString = data.substring(0, commaIndex);
        String yString = data.substring(commaIndex + 1);
        center_x = xString.toFloat();
        center_y = yString.toFloat();
      
        error_pan=center_x-pixel_x;
        error_tilt=center_y-pixel_y;
        Serial.println(error_pan);
        Serial.println(error_tilt);
        if (abs(error_pan) > 10)          // the number here will depend on camera
        {
          pan_pos=pan_pos-error_pan/12;    // the number here will depend on camera
        }
      
        if (abs(error_tilt) > 10)          // the number here will depend on camera
        {
          tilt_pos=tilt_pos-error_tilt/12 ;   // the number here will depend on camera
        }
      
        if (pan_pos>145)  //max displacement of 45 degree form center of 90 degrees.
        {
          pan_pos=145;
        }
        if (pan_pos<35) 
        {
          pan_pos=35;
        }
      
        if (tilt_pos>145)  //max displacement of 45 degree form center of 90 degrees.
        {
          tilt_pos=145;
        }
        if (tilt_pos<35) 
        {
          tilt_pos=35;
        }
      
        pan_servo.write(pan_pos);
        tilt_servo.write(tilt_pos);
//        pixel_x=center_x;
//        pixel_y=center_y;
//        Serial.println(pan_pos);
//        Serial.println(tilt_pos);
      }
}
