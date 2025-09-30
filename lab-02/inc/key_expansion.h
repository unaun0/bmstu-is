#ifndef KEY_EXPANSION_H
#define KEY_EXPANSION_H

#include <stdint.h>

#define Nb 4
#define Nk 4
#define Nr 10

#define AES_KEY_SIZE (Nk * 4) // 128 бит = 16 байт

void key_expansion(const uint8_t* key, uint8_t* expandedKeys);
void generate_key(uint8_t* key);

#endif // KEY_EXPANSION_H
