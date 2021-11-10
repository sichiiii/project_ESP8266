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
    http.begin(client, "http://192.168.1.6:8090/statuses"); 
    int httpCode = http.GET(); 
    if (httpCode > 0) {
      String payload = http.getString();
      deserializeJson(doc, payload);
      if (doc["ports"]["1"] == 1){
        digitalWrite(pin_1, HIGH);
      }
      else{
        digitalWrite(pin_1, LOW);
      }
      if (doc["ports"]["2"] == 1){
        digitalWrite(pin_2, HIGH);
      }
      else{
        digitalWrite(pin_2, LOW);
      }
      if (doc["ports"]["3"] == 1){
        digitalWrite(pin_3, HIGH);
      }
      else{
        digitalWrite(pin_3, LOW);
      }
      if (doc["ports"]["4"] == 1){
        digitalWrite(pin_4, HIGH);
      }
      else{
        digitalWrite(pin_4, LOW);
      }
      if (doc["ports"]["7"] == 1){
        digitalWrite(pin_7, HIGH);
      }
      else{
        digitalWrite(pin_7, LOW);
      }
      if (doc["ports"]["8"] == 1){
        digitalWrite(pin_8, HIGH);
      }
      else{
        digitalWrite(pin_8, LOW);
      }
      if (doc["ports"]["9"] == 1){
        digitalWrite(pin_9, HIGH);
      }
      else{
        digitalWrite(pin_9, LOW);
      }
      if (doc["ports"]["10"] == 1){
        digitalWrite(pin_10, HIGH);
      }
      else{
        digitalWrite(pin_10, LOW);
      }
      if (doc["ports"]["11"] == 1){
        digitalWrite(pin_11, HIGH);
      }
      else{
        digitalWrite(pin_11, LOW);
      }
      if (doc["ports"]["13"] == 1){
        digitalWrite(pin_13, HIGH);
      }
      else{
        digitalWrite(pin_13, LOW);
      }
      if (doc["ports"]["14"] == 1){
        digitalWrite(pin_14, HIGH);
      }
      else{
        digitalWrite(pin_14, LOW);
      }
      if (doc["ports"]["15"] == 1){
        digitalWrite(pin_15, HIGH);
      }
      else{
        digitalWrite(pin_15, LOW);
      }
      if (doc["ports"]["16"] == 1){
        digitalWrite(pin_16, HIGH);
      }
      else{
        digitalWrite(pin_16, LOW);
      }
      
      String output;
      serializeJson(doc, output); 
      Serial.println(output); 
    }else Serial.println("An error ocurred");
    http.end();  
  }
  delay(1000);   
}
