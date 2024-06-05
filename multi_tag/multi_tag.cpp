#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <iostream>
#include <string>

#define RST_PIN         22  // Configurável, veja o layout típico dos pinos acima
#define SS_1_PIN        21  // Configurável, escolha um pino não utilizado, apenas HIGH/LOW é necessário, deve ser diferente de SS 2
#define SS_2_PIN        5   // Configurável, escolha um pino não utilizado, apenas HIGH/LOW é necessário, deve ser diferente de SS 1
#define SS_3_PIN        4 

#define NR_OF_READERS   3

byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN};
String tagIDs[] = {
  "be41cd1d", // A
  "ce24251d", // E
  "53cef2f6", // B
  "ddb93e2d", // D
  "ceb9211d", // F
  "53e51df5", // C
  "83df46f5", // I
  "b3c424f5", // O
  "2301e8f6", // R
  "736347fa", // A
  "f37aebf6", // E
  "c3a526f5", // U
  "53400ef5", // M
  "73540ff5", // R
  "63d939f5", // L
  "731409f5", // Z
  "535837f5", // S
  "13701bf5"  // N
};
char tagLetters[] = {'A', 'E', 'B', 'D', 'F', 'C', 'I', 'O', 'R', 'A', 'E', 'U', 'M', 'R', 'L', 'Z', 'S', 'N'};

String dump_byte_array(byte *buffer, byte bufferSize) {
  String tag = "";
  for (byte i = 0; i < bufferSize; i++) {
    if (buffer[i] < 0x10) {
      tag += "0";
    }
    tag += String(buffer[i], HEX);
  }
  return tag;
}

char Dicionario(String tagID, String tagIDs[], int numTags) {
  for (int i = 0; i < numTags; i++) {
    if (tagID == tagIDs[i]) {
      return tagLetters[i];
    }
  }
  return '0';
}

MFRC522 mfrc522[NR_OF_READERS]; // Criar instância MFRC522.

/**
 * Inicializa.
 */
void setup() {
  Serial.begin(9600); // Inicializa a comunicação serial com o PC
  while (!Serial);    // Não faz nada se nenhuma porta serial for aberta (adicionado para Arduinos baseados no ATMEGA32U4)

  SPI.begin(); // Inicia o barramento SPI

  for (uint8_t leitor = 0; leitor < NR_OF_READERS; leitor++) {
    mfrc522[leitor].PCD_Init(ssPins[leitor], RST_PIN); // Inicializa cada cartão MFRC522
    mfrc522[leitor].PCD_DumpVersionToSerial();
  }
}

void loop() {
  for (uint8_t leitor = 0; leitor < NR_OF_READERS; leitor++) {
    // Procura novos cartões
    if (mfrc522[leitor].PICC_IsNewCardPresent() && mfrc522[leitor].PICC_ReadCardSerial()) {
      String tag = dump_byte_array(mfrc522[leitor].uid.uidByte, mfrc522[leitor].uid.size);
      //Serial.println(tag);
      char letra = Dicionario(tag, tagIDs, sizeof(tagIDs) / sizeof(tagIDs[0]));
      std::string numero_str = std::to_string(leitor);
      std::string resultado = numero_str + letra;
      std::cout << resultado << std::endl;
      
      // Para o PICC
      mfrc522[leitor].PICC_HaltA();
      // Para a criptografia no PCD
      mfrc522[leitor].PCD_StopCrypto1();
    }
  }
}
