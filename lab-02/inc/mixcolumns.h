#ifndef MIXCOLUMNS_H
#define MIXCOLUMNS_H

#include <stdint.h>

void mix_columns(uint8_t state[4][4]);
void inv_mix_columns(uint8_t state[4][4]);

void mix_columns_simd(uint8_t state[4][4]);
void inv_mix_columns_simd(uint8_t state[4][4]);

#endif // MIXCOLUMNS_H
