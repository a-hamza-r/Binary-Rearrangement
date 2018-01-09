#include <stdio.h>
// using namespace std;

int factorial(int n) {
	if (n == 0 || n == 1)
	{
		return 1;
	}
	return n*factorial(n-1);
}

void print() {
	printf("I am a barbie girl in the barbie world :)\n");
}


int main(int argc, char const *argv[])
{
	factorial(6);
	factorial(10);
	factorial(10);
	printf("%d\n", factorial(10));
	print();
	print();
	return 0;
}