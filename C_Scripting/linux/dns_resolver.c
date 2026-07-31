#include <stdio.h>
#include <netdb.h>
#include <arpa/inet.h>

int main(int argc, char *argv[]){
	
	if (argc<2) {
	fprintf(stderr, "Usage: %s <hostname>\n", argv[0]);
	return 1;
	}

	char *ip;

	struct hostent *target = gethostbyname(argv[1]);
	if (target == NULL) {
		fprintf(stderr, "Could not resolve host.\n");
		return 1;
	} else {
		ip = inet_ntoa(*((struct in_addr *)target->h_addr));
		printf("IP: %s\n",ip);
		return 0;
	}
}