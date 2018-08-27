#include "string.h"
#include "stdio.h"
#include "stdlib.h"
#include "time.h"

#define BITS_PER_KEY 8
typedef unsigned int uint32_t;
typedef struct _bloom_filter{
	int k;
	char *array;
	int bits;
}Bloom_filter;
