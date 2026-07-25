#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <unistd.h>

int main(int argc, char *argv[]){
	
	if (argc<3){
		fprintf(stdout, "=|=|=|=|=|=|=|=|=| PortPeek_v2 |=|=|=|=|=|=|=|=|=\n");
		fprintf(stdout, "=|=| Usage: %s <IP/Domain> <Port> |=|=\n", argv[0]);
		fprintf(stdout, "=|=|=| Example: %s example.com 80 |=|=\n", argv[0]);
		fprintf(stdout, "=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=\n");
		return 1;
	}
	
	char *dst = argv[1];
	char *port = argv[2];

	int sockfd;
	int conn_result;

	struct addrinfo hints, *res, *rp;
	memset(&hints, 0, sizeof hints);
	hints.ai_family   = AF_UNSPEC; //aceita IPv4 e IPv6
	hints.ai_socktype = SOCK_STREAM;

	int status = getaddrinfo(dst, port, &hints, &res);
	if (status != 0){
		fprintf(stderr, "Error to resolve: %s: %s\n", dst, gai_strerror(status));
		return 1;
	}
	
	for (rp=res;rp!=NULL;rp=rp->ai_next) {

		sockfd = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
		if (sockfd<0){
			continue;
		}

		conn_result = connect(sockfd, rp->ai_addr, rp->ai_addrlen);
		if (conn_result == 0){
			break;
		}
		close(sockfd);
		sockfd = -1;
	}
	freeaddrinfo(res);
	
	if (sockfd<0){
		fprintf(stdout, "Port %s is closed.\n", port);
	} else {
		fprintf(stdout, "Port %s is open.\n", port);
		close(sockfd);
	}
	return 0;
}