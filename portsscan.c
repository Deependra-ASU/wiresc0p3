#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 



int main(int argc, char *argv[])
{
    char *hostname[5] = {"192.168.0.12","192.168.0.11","192.168.0.10","192.168.0.20","192.168.0.15"};
    
    //printf("%s",argv[1]);
    int x;
    sscanf(argv[1],"%d",&x);      //8080;
    int portno = x;	
   // char *hostname = "192.168.0.11";

    int sockfd;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    

    int len = sizeof(hostname) / sizeof(hostname[0]);
    
    
    for(int i = 0; i < len;i++)
    {
		    sockfd = socket(AF_INET, SOCK_STREAM, 0);
		    if (sockfd < 0) {
				printf("ERROR opening socket");
				exit(0);
			}
		    server = gethostbyname(hostname[i]);

		    if (server == NULL) {
			fprintf(stderr,"ERROR, no such host\n");
			exit(0);
		    }

		    bzero((char *) &serv_addr, sizeof(serv_addr));
		    serv_addr.sin_family = AF_INET;
		    bcopy((char *)server->h_addr, 
			 (char *)&serv_addr.sin_addr.s_addr,
			 server->h_length);

		    serv_addr.sin_port = htons(portno);
		    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) {
			printf("Port is closed\n");
		    } else {
			printf("Port is active\n");
		    }

		    close(sockfd);
   }
    return 0;
}
