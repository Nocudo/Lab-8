const int pinInductivo = 12;      // PR12-4DN (Metales)
const int pinFotoelectrico = 13;  // BMS2M-MDT (Fotoeléctrico)
const int pinCapacitivo = 14;     // CR18-8DN (Capacitivo)

volatile int cuentaInductivo = 0;
volatile int cuentaFoto = 0;
volatile int cuentaCapacitivo = 0;

volatile unsigned long lastTimeInd = 0;
volatile unsigned long lastTimeFoto = 0;
volatile unsigned long lastTimeCap = 0;

const unsigned long debounceTime = 300; 

void IRAM_ATTR isrInductivo() {
  unsigned long now = millis();
  if (now - lastTimeInd > debounceTime) {
    if (digitalRead(pinInductivo) == LOW) {
      cuentaInductivo++;
      lastTimeInd = now;
    }
  }
}

void IRAM_ATTR isrFoto() {
  unsigned long now = millis();
  if (now - lastTimeFoto > debounceTime) {
    if (digitalRead(pinFotoelectrico) == LOW) {
      cuentaFoto++;
      lastTimeFoto = now;
    }
  }
}

void IRAM_ATTR isrCapacitivo() {
  unsigned long now = millis();
  if (now - lastTimeCap > debounceTime) {
    if (digitalRead(pinCapacitivo) == LOW) {
      cuentaCapacitivo++;
      lastTimeCap = now;
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(pinInductivo, INPUT_PULLUP);
  pinMode(pinFotoelectrico, INPUT_PULLUP);
  pinMode(pinCapacitivo, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinInductivo), isrInductivo, FALLING);
  attachInterrupt(digitalPinToInterrupt(pinFotoelectrico), isrFoto, FALLING);
  attachInterrupt(digitalPinToInterrupt(pinCapacitivo), isrCapacitivo, FALLING);
}

void loop() {
  Serial.print(cuentaInductivo);
  Serial.print(",");
  Serial.print(cuentaFoto);
  Serial.print(",");
  Serial.println(cuentaCapacitivo);
  delay(100); 
}