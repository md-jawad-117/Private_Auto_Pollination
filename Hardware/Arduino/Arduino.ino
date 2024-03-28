#include <Servo.h>

Servo pan_servo;
Servo tilt_servo;

const int center_x=;
const int center_y=;
int error_pan;
int error_tilt;

int pixel_x=0;
int pixel_y=0;

int pan_pos = 90;  
int tilt_pos = 90;  

void setup() 
{
  pan_servo.attach(9); 
  tilt_servo.attach(9); 
  pan_servo.write(90); 
  tilt_servo.write(90); 
}



void loop()
{
  error_pan=center_x-pixel_x;
  error_tilt=center_y-pixel_y;
  if (abs(error_pan) > 15)          // the number here will depend on camera
  {
    pan_pos=pan_pos-error_pan/35    // the number here will depend on camera
  }

  if (abs(error_tilt) > 15)          // the number here will depend on camera
  {
    pan_pos=pan_pos-error_pan/35    // the number here will depend on camera
  }

  if (pan_pos>135)  //max displacement of 45 degree form center of 90 degrees.
  {
    pan_pos=135;
  }
  if (pan_pos<45) 
  {
    pan_pos=45;
  }

  if (tilt_pos>135)  //max displacement of 45 degree form center of 90 degrees.
  {
    tilt_pos=135;
  }
  if (tilt_pos<45) 
  {
    tilt_pos=45;
  }

  pan_servo.write(pan_pos);
  tilt_servo.write(tilt_pos);
  
}
