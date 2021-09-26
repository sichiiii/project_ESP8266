#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
 
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
    http.begin(client, "http://192.168.1.6:8090/"); 
    int httpCode = http.GET(); 
    if (httpCode > 0) { 
      String payload = http.getString();  
      Serial.println(payload);            
    }else Serial.println("An error ocurred");
    http.end();  
  }
  delay(10000);   
}