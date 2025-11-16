// Distância mínima em centímetros para detectar carro estacionado
const int distancia_carro = 10;  

// sensor
const int TRIG = 3; 
const int ECHO = 2; 

const int ledGreen = 7; 
const int ledRed = 8; 
const int buzzer = 9; 

// Variáveis para funcionamento do Buzzer 
float seno; 
int frequencia; 

// VARIÁVEIS DE CONTROLE
int distanciaAtual = 0;
int distanciaAnterior = 0;
unsigned long tempoImovel = 0;        // tempo em que o carro está imóvel
const unsigned long tempoLimite = 3000; // 3 segundos imóvel para parar buzzer
bool buzzerAtivo = false;

void setup() {
  Serial.begin(9600);
  
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  
  pinMode(ledGreen, OUTPUT);
  pinMode(ledRed, OUTPUT);
  pinMode(buzzer, OUTPUT); 
}

void loop() {
  distanciaAtual = sensor(TRIG, ECHO);

  // Verifica se há carro na vaga
  if (distanciaAtual <= distancia_carro) {
    digitalWrite(ledGreen, LOW);
    digitalWrite(ledRed, HIGH);

    // Envia informação para o computador
    Serial.println("Vaga Ocupada");

    // Detecta se o carro está imóvel (diferença menor que 1 cm)
    if (abs(distanciaAtual - distanciaAnterior) < 1) {
      if (millis() - tempoImovel > tempoLimite) {
        noTone(buzzer);
        buzzerAtivo = false;
      }
    } else {
      // Carro ainda se movendo — reseta o temporizador
      tempoImovel = millis();
      if (!buzzerAtivo) {
        tocaBuzzer();
        buzzerAtivo = true;
      }
    }
  } 
  else {
    // Vaga livre
    digitalWrite(ledGreen, HIGH);
    digitalWrite(ledRed, LOW);
    Serial.println("Vaga Livre");
    noTone(buzzer);
    buzzerAtivo = false;
    tempoImovel = millis(); // reseta o tempo
  }

  distanciaAnterior = distanciaAtual;
  delay(200);
}

int sensor(int pinotrig, int pinoecho) {
  digitalWrite(pinotrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinotrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinotrig, LOW);

  return pulseIn(pinoecho, HIGH) / 58; // converte para cm
}

void tocaBuzzer() {
  for (int x = 0; x < 180; x++) {
    seno = sin(x * 3.1416 / 180);
    // ajustei de 2000 para 500
    frequencia = 500 + int(seno * 1000);
    tone(buzzer, frequencia);
    delay(2);
  }
}
