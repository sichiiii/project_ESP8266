#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <Arduino_JSON.h>


const int pin_1 = 1;
const int pin_2 = 2;
const int pin_3 = 3;
const int pin_4 = 4;
const int pin_7 = 7;
const int pin_8 = 8;
const int pin_9 = 9;
const int pin_10 = 10;
const int pin_11 = 11;
const int pin_13 = 13;
const int pin_14 = 14;
const int pin_15 = 15;
const int pin_16 = 16;


void setup () {
  Serial.begin(115200);
  WiFi.begin("KGB-USSR", "paintnet24");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }
  Serial.println("Connected to WiFi Network");
}
 
void loop() {
  if (WiFi.status() == WL_CONNECTED) { 
    WiFiClient client;
    HTTPClient http;
    DynamicJsonDocument doc(1024); 
    http.begin(client, "http://192.168.1.6:8090/"); 
    int httpCode = http.GET(); 
    if (httpCode > 0) {
      String payload = http.getString();
      //deserializeJson(doc, payload);
      doc["1"] = digitalRead(pin_1);
      doc["2"] = digitalRead(pin_2);
      doc["3"] = digitalRead(pin_3);
      doc["4"] = digitalRead(pin_4);
      doc["5"] = "-";
      doc["6"] = "-";
      doc["7"] = digitalRead(pin_7);
      doc["8"] = digitalRead(pin_8);
      doc["9"] = digitalRead(pin_9);
      doc["10"] = digitalRead(pin_10);
      doc["11"] = digitalRead(pin_11);
      doc["12"] = "-";
      doc["13"] = digitalRead(pin_13);
      doc["14"] = digitalRead(pin_14);
      doc["15"] = digitalRead(pin_15);
      doc["16"] = digitalRead(pin_16);
        
      String output;
      serializeJson(doc, output); 
      Serial.println(output); 
    }else Serial.println("An error ocurred");
    http.end();  
  }
  delay(10000);   
}