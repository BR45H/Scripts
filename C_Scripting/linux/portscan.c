#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

int main(int argc, char *argv[]){
	
	int sockfd; //variavel para armazenar FD do socket
	int conn_result;
	int port;
	int start = 0;
	int end = 65535;

	if (argc<2){
		printf("Portscan C script\n");
		printf("Usage: %s <IP>\n", argv[0]);
		return 1;
	}

	char *dst = argv[1];

	if (inet_addr(dst) == INADDR_NONE) {
		fprintf(stderr, "Invalid IP: %s\n", dst);
		return 1;
	}

	struct sockaddr_in target;
	struct timeval timeout;
	fd_set fdset; //variavel local: conjunto de FDs que eu escolho monitorar via select()

	for (port=start;port<=end;port++){
		sockfd = socket(AF_INET,SOCK_STREAM,0);
		if (sockfd < 0) { continue; }

		fcntl(sockfd, F_SETFL, O_NONBLOCK); //altera flag do socket para nao-bloqueante

		memset(&target, 0, sizeof(target)); //zera a struct, limpa lixo de memoria
		target.sin_family = AF_INET;
		target.sin_port = htons(port);
		target.sin_addr.s_addr = inet_addr(dst);

		conn_result = connect(sockfd, (struct sockaddr *)&target, sizeof target);
		//connect() tenta iniciar o handshake, como o socket e nao-bloqueante, retorna instantaneamente EINPROGRESS
		//conn_result armazena status do connect(), identificando numericamente se falhou instantaneamente ou esta em EINPROGRESS

		if (conn_result < 0 && errno == EINPROGRESS){
			FD_ZERO(&fdset); //macro que inicializa a var fdset
			FD_SET(sockfd, &fdset); //macro que liga o bit correspondente ao sockfd dentro do fdset
			timeout.tv_sec = 0;
			timeout.tv_usec = 200000;

			int sel = select(sockfd + 1, NULL, &fdset, NULL, &timeout);
			//espera o socket ficar pronto pra escrita

			if (sel > 0) {
				int so_error;
				socklen_t len = sizeof(so_error);
				getsockopt(sockfd, SOL_SOCKET, SO_ERROR, &so_error, &len);
				//Pergunta o codigo de erro no kernel e passa para a var so_error
				//so_error revela se foi sucesso (0) ou falha (!=0)
				
				if (so_error == 0) {
					fprintf(stdout, "[+] Port %i is open.\n",port);
				}
			}
		} else if (conn_result == 0){
			fprintf(stdout, "[+] Port %i is open.\n",port);
		}
		close(sockfd);
	}
	return 0;
}
