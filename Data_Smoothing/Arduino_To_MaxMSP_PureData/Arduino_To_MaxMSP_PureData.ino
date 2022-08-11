int val[6]; //Array. 6 sensors total

void setup(){
  Serial.begin(38400); //Serial communication set up
}

void loop(){
  //Read analog inputs one by one and send them to Pure Data or MaxMSP
  for(int i = 0; i < 6; i++){
    val[i] = analogRead(i);
    Serial.print(val[i]);
    Serial.print(" ");
  }
  Serial.println();
  delay(10); 
}
