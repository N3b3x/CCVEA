#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <printf.h>

//
// Payload
//

const int min_payload_size = 4;
const int max_payload_size = 32;
char receive_payload[max_payload_size + 1]; // +1 to allow room for a terminating NULL char


RF24 radio(9, 10); // CE, CSN
// Radio pipe addresses for the 2 nodes to communicate.
const uint64_t pipes[2] = { 0xF0F0F0F0E1LL, 0xF0F0F0F0D2LL };

void setup() {
  Serial.begin(115200);
  printf_begin();                 // CRUCIALLLLLL (Necessary to direct stdout to the Arduino Serial library, which enables 'printf')

  radio.begin();
  radio.setChannel(2);
  radio.enableDynamicPayloads();  // Enable dynamic payloads
  radio.setRetries(5, 15);        // Optionally, increase the delay between retries & # of retries

  radio.openReadingPipe(0, pipes[0]);   //Setting the address at which we will receive the data
  radio.setPALevel(RF24_PA_MIN);       //You can set this as minimum or maximum depending on the distance between the transmitter and receiver.
  radio.startListening();              //This sets the module as receiver
}
void loop()
{
  while (radio.available()) {

    // Fetch the payload, and see if this was the last one.
    uint8_t len = radio.getDynamicPayloadSize();

    // If a corrupt dynamic payload is received, it will be flushed
    if (!len) {
      continue;
    }

    radio.read(receive_payload, len);
    Serial.println(receive_payload);
  }
}