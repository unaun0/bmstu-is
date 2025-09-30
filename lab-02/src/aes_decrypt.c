#include "aes_decrypt.h"
#include "add_round_key.h"
#include "key_expansion.h"
#include "mixcolumns.h"
#include "sbox.h"
#include "shiftrows.h"

#define KEY_SIZE Nb * (Nr + 1)*4

static void inv_sub_bytes(uint8_t state[4][4]) {
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            state[i][j] = inv_sbox_get(state[i][j]);
}

void aes_decrypt(const uint8_t* input, uint8_t* output, const uint8_t* key) {
    uint8_t state[4][4];
    uint8_t expandedKeys[KEY_SIZE];

    key_expansion(key, expandedKeys);

    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            state[j][i] = input[i * 4 + j];

    add_round_key(state, (uint8_t (*)[4])(expandedKeys + Nr * Nb * 4));

    for (int round = Nr - 1; round > 0; round--) {
        inv_shift_rows(state);
        inv_sub_bytes(state);
        add_round_key(state, (uint8_t (*)[4])(expandedKeys + round * Nb * 4));
        inv_mix_columns(state);
    }

    inv_shift_rows(state);
    inv_sub_bytes(state);
    add_round_key(state, (uint8_t (*)[4])expandedKeys);

    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            output[i * 4 + j] = state[j][i];
}

void aes_ecb_decrypt(const uint8_t* input, uint8_t* output, size_t length, const uint8_t* key) {
    if (length % 16 != 0) return;

    size_t blocks = length / 16;
    for (size_t i = 0; i < blocks; i++) {
        aes_decrypt(input + i*16, output + i*16, key);
    }
}

// ------------------------------------------------------------------------------

#include <pthread.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <emmintrin.h>
#include <tmmintrin.h>

static void inv_sub_bytes_simd(uint8_t state[4][4]) {
    inv_sbox_sub_bytes_simd((uint8_t*)state);
}

static inline void load_state(uint8_t state[4][4], const uint8_t* input) {
    __m128i data = _mm_loadu_si128((const __m128i*)input);

    const __m128i shuffle_mask = _mm_set_epi8(
        15, 11, 7, 3,
        14, 10, 6, 2,
        13, 9, 5, 1,
        12, 8, 4, 0
    );
    __m128i transposed = _mm_shuffle_epi8(data, shuffle_mask);
    _mm_storeu_si128((__m128i*)state[0], transposed);
}

void aes_decrypt_upd(const uint8_t* input, uint8_t* output, const uint8_t* key) {
    uint8_t state[4][4];
    uint8_t expandedKeys[KEY_SIZE];

    key_expansion(key, expandedKeys);

    load_state(state, input);

    add_round_key_simd(state, (uint8_t (*)[4])(expandedKeys + Nr * Nb * 4));

    for (int round = Nr - 1; round > 0; round--) {
        inv_shift_rows_simd(state);
        inv_sub_bytes_simd(state);
        add_round_key_simd(state, (uint8_t (*)[4])(expandedKeys + round * Nb * 4));
        inv_mix_columns_simd(state);
    }

    inv_shift_rows_simd(state);
    inv_sub_bytes_simd(state);
    add_round_key_simd(state, (uint8_t (*)[4])expandedKeys);

    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            output[i * 4 + j] = state[j][i];
}

typedef struct {
    const uint8_t* input;
    uint8_t* output;
    size_t start_block;
    size_t num_blocks;
    size_t length;
    const uint8_t* key;
} aes_thread_task_t;

void* aes_decrypt_worker(void* arg) {
    aes_thread_task_t* task = (aes_thread_task_t*)arg;

    for (size_t i = 0; i < task->num_blocks; i++) {
        size_t block_index = task->start_block + i;
        size_t offset = block_index * 16;
        size_t bytes_to_copy = (task->length - offset >= 16) ? 16 : (task->length - offset);

        uint8_t block[16] = {0};
        memcpy(block, task->input + offset, bytes_to_copy);

        aes_decrypt_upd(block, task->output + offset, task->key);
    }

    free(task);
    return NULL;
}

void aes_ecb_decrypt_upd(const uint8_t* input, uint8_t* output, size_t length, const uint8_t* key) {
    if (length % 16 != 0) return;

    size_t blocks = length / 16;
    size_t num_threads = 8; // можно брать число ядер CPU
    pthread_t threads[num_threads];

    size_t blocks_per_thread = (blocks + num_threads - 1) / num_threads;

    for (size_t t = 0; t < num_threads; t++) {
        aes_thread_task_t* task = malloc(sizeof(aes_thread_task_t));
        task->input = input;
        task->output = output;
        task->start_block = t * blocks_per_thread;
        task->num_blocks = (task->start_block + blocks_per_thread <= blocks) ? blocks_per_thread : (blocks - task->start_block);
        task->length = length;
        task->key = key;

        pthread_create(&threads[t], NULL, aes_decrypt_worker, task);
    }

    for (size_t t = 0; t < num_threads; t++) {
        pthread_join(threads[t], NULL);
    }
}