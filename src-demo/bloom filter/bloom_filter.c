#include "bloom_filter.h"

static char* itoa(int num,char*str,int radix)
{/*索引表*/
	char index[]="0123456789ABCDEF";
	unsigned unum;/*中间变量*/
	int i=0,j,k;
	/*确定unum的值*/
	if(radix==10&&num<0)/*十进制负数*/
	{
		unum=(unsigned)-num;
		str[i++]='-';
	}
	else unum=(unsigned)num;/*其他情况*/
	/*转换*/
	do{
		str[i++]=index[unum%(unsigned)radix];
		unum/=radix;
	}while(unum);
	str[i]='\0';
	/*逆序*/
	if(str[0]=='-')k=1;/*十进制负数*/
	else k=0;
	char temp;
	for(j=k;j<=(i-1)/2;j++)
	{
		temp=str[j];
		str[j]=str[i-1+k-j];
		str[i-1+k-j]=temp;
	}
	return str;
}

static uint32_t DecodeFixed32(const char* ptr) {
  if (1) {
    // Load the raw bytes
    uint32_t result;
    memcpy(&result, ptr, sizeof(result));  // gcc optimizes this to a plain load
    return result;
  } else {
    return ( (uint32_t)((unsigned char)(ptr[0]))
        | ((uint32_t)((unsigned char)(ptr[1])) << 8)
        | ((uint32_t)((unsigned char)(ptr[2])) << 16)
        | ((uint32_t)((unsigned char)(ptr[3])) << 24) );
  }
}

static uint32_t BloomHash(const char* data, size_t n, uint32_t seed) {
	// Similar to murmur hash
	const uint32_t m = 0xc6a4a793;
	const uint32_t r = 24;
	const char* limit = data + n;
	uint32_t h = seed ^ (n * m);
	// Pick up four bytes at a time
	while (data + 4 <= limit) {
		uint32_t w = DecodeFixed32(data);
		data += 4;
		h += w;
		h *= m;
		h ^= (h >> 16);
	}
	// Pick up remaining bytes
	switch (limit - data) {
		case 3:
			h += (unsigned char)(data[2]) << 16;
			do { } while (0);
		case 2:
			h +=  (unsigned char)(data[1]) << 8;
			do { } while (0);
		case 1:
			h +=  (unsigned char)(data[0]);
			h *= m;
			h ^= (h >> r);
			break;
	}
	return h;
}


static void set_bloom_filter(Bloom_filter *bloom_filter,int key){
	int j;
	char str[10];
	itoa(key, str, 10);
	// Use double-hashing to generate a sequence of hash values.
	// See analysis in [Kirsch,Mitzenmacher 2006].
	uint32_t h = BloomHash(str,strlen(str),0xbc9f1d34);
	const uint32_t delta = (h >> 17) | (h << 15);  // Rotate right 17 bits
	for (j = 0; j<bloom_filter->k; j++) {
		const uint32_t bitpos = h % bloom_filter->bits;
		bloom_filter->array[bitpos/8] |= (1 << (bitpos % 8));
		h += delta;
	}
}
int search_bloom_filter(Bloom_filter *bloom_filter,int key){
	int j,results = 0;
	char str[10];
	itoa(key, str, 10);
	uint32_t h = BloomHash(str,strlen(str),0xbc9f1d34);
	const uint32_t delta = (h >> 17) | (h << 15);  // Rotate right 17 bits
	for (j = 0; j<bloom_filter->k; j++) {
		const uint32_t bitpos = h % bloom_filter->bits;
	 	if((bloom_filter->array[bitpos/8] & (1 << (bitpos % 8))) !=0 )
			results++;
		h += delta;
	}
	return (results==bloom_filter->k);
}


Bloom_filter * create_bloom_filter(int n,int key[]){
	Bloom_filter *bloom_filter = malloc(sizeof(Bloom_filter));
	bloom_filter->k = (size_t)(BITS_PER_KEY * 0.69); // 0.69=~ln(2)
	if(bloom_filter->k < 1) bloom_filter->k = 1;
	if(bloom_filter->k > 30) bloom_filter->k = 30;
	int bits = n * BITS_PER_KEY;
	int bytes = (bits+7)/8;
	bits = bytes * 8;
	bloom_filter->bits = bits;
	bloom_filter->array = malloc(sizeof(char)*bytes);
	memset(bloom_filter->array, 0, sizeof(char)*bytes);
	int i;
	for(i=0;i<n;i++){
		set_bloom_filter(bloom_filter,key[i]);
	}
	return bloom_filter;
}

int main(){
	int a[1000000],i,n;
	n = 1000000;
	for(i=0;i<n;i++)
		a[i] = i+10*n;
	Bloom_filter *bloom_filter = create_bloom_filter(n,a);
	int r;
	srand(time(NULL));  
	for(i=0;i<n;i++){
		
		r += search_bloom_filter(bloom_filter,rand()%n + 5*n);
		
	}
	printf("r=%d\n",r);
	return 0;
}












