#include <stdio.h>

static void print(bool* ptr){
	printf("%x%x%x%x%x%x%x%x\n", *ptr, *(ptr+1), *(ptr+2), *(ptr+3), *(ptr+4), *(ptr+5), *(ptr+6), *(ptr+7));
}

static void print2(int* ptr){
	printf("%ld\n", intptr_t(ptr));
}

int main () {
	int* tmp;
	try {
		for(int i = -2416; i < 0; i+=1){
			print2(tmp+i);
		}
	} catch(SegmentationError e){

	}
	return 0;
}