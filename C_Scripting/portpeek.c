#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

int main(int argc, char *argv[]){

	if (argc<3) {
	fprintf(stdout, "Usage: %s <IP> <Port>\n", argv[0]);
	return 1;
	}

	int sockfd;
	int conn_result;
	struct sockaddr_in target;

	sockfd = socket(AF_INET,SOCK_STREAM,0);
	if (sockfd < 0) {
		perror("socket");
			return 1;
	}

	target.sin_family = AF_INET;
	target.sin_port = htons(atoi(argv[2]));
	target.sin_addr.s_addr = inet_addr(argv[1]);

	conn_result = connect(sockfd, (struct sockaddr *)&target, sizeof target);

	if (conn_result == 0){
		fprintf(stdout, "Port %s is open.\n", argv[2]);
	} else {
		fprintf(stdout, "Port %s is closed.\n", argv[2]);
	}

	close(sockfd);
	return 0;
}