#include "key_expansion.h"
#include "sbox.h"

#define AES_EXPANDED_KEY_SIZE (Nb * (Nr + 1) * 4)       // 176 байт для AES-128
#define RCON_SIZE (Nr + 1)

const uint8_t Rcon[11] = {
    0x00, 0x01, 0x02, 0x04, 0x08,
    0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
};

static void rot_word(uint8_t* word) {
    uint8_t temp = word[0];
    word[0] = word[1];
    word[1] = word[2];
    word[2] = word[3];
    word[3] = temp;
}

static void sub_word(uint8_t* word) {
    for (int i = 0; i < 4; i++) {
        word[i] = sbox_get(word[i]);
    }
}

void key_expansion(const uint8_t* key, uint8_t* expandedKeys) {
    int i = 0;
    uint8_t temp[4];

    // Первые 16 байт — исходный ключ
    for (i = 0; i < AES_KEY_SIZE; i++) {
        expandedKeys[i] = key[i];
    }

    int bytesGenerated = AES_KEY_SIZE;
    int rconIteration = 1;

    while (bytesGenerated < AES_EXPANDED_KEY_SIZE) {
        // Последние 4 байта предыдущего слова
        for (int j = 0; j < 4; j++) {
            temp[j] = expandedKeys[bytesGenerated - 4 + j];
        }

        if (bytesGenerated % AES_KEY_SIZE == 0) {
            rot_word(temp);
            sub_word(temp);
            temp[0] ^= Rcon[rconIteration++];
        }

        for (int j = 0; j < 4; j++) {
            expandedKeys[bytesGenerated] = expandedKeys[bytesGenerated - AES_KEY_SIZE] ^ temp[j];
            bytesGenerated++;
        }
    }
}

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void generate_key(uint8_t* key) {
    srand((unsigned int)time(NULL));
    for (int i = 0; i < Nk * 4; i++) {
        key[i] = rand() % 256;
    }
}
