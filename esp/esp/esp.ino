#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <Arduino_JSON.h>


const int DIN_PIN = 7;

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
      deserializeJson(doc, payload);
      String output;
      serializeJson(doc, output); 
      //Serial.println(output);
      //Serial.write(output);
      int value;
      value = digitalRead( DIN_PIN );
      Serial.println( value );  
    }else Serial.println("An error ocurred");
    http.end();  
  }
  delay(10000);   
}