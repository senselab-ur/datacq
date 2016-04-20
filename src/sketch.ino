#include <ArduinoJson.h>

float val;
int data = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {

  StaticJsonBuffer<200> jsonBuffer;
  // not used in this example
  JsonObject& root = jsonBuffer.createObject();

  // Add values in the object
  //
  // Most of the time, you can rely on the implicit casts.
  // In other case, you can do root.set<long>("time", 1351824120);
  root["sensor"] = "voltage";
  data = analogRead(A0);
  val = data * (50.0/1023.0);
  // Add a nested array.
  //
  // It's also possible to create the array separately and add it to the
  // JsonObject but it's less efficient.
  JsonArray& data = root.createNestedArray("data");
  data.add(val);
  root.printTo(Serial);
  Serial.println();
  delay(1000);
}
