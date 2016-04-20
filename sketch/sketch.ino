#include <ArduinoJson.h>

float val, val2;
int data, data2;

void setup() {
  Serial.begin(9600);
}

void loop() {

  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["sensor"] = "voltage";
  
  data = analogRead(A0);
  data2 = analogRead(A1);

  val = data * (50.0/1023.0);
  val2 = data2 * (50.0 / 1023.0);

  JsonArray& data = root.createNestedArray("data1");
  data.add(val);
  data.add(val2);

  root.printTo(Serial);

  Serial.println();
  delay(1000);
}
