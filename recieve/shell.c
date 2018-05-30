#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
int main(void) {
   char *buffer;
   char *args[5];
   int i;
   int pid;
   buffer = malloc(255);
   args[0] = "Stat";
   while(strcmp(args[0], "exit")) {
      printf(":");
      fgets(buffer, 255, stdin);
      buffer = strtok(buffer, "\n");
      args[0] = strtok(buffer, " ");
      i = 0;
      while(++i < 5 && (args[i] = strtok(NULL, " ")));
      if((pid = fork()) == -1) {
         printf("Failed to fork");
         exit(-1);
      }
      else if(pid == 0) {
         if(!strcmp(args[0], "test")) {
            execlp("/usr/local/bin/python3", "/usr/local/bin/python3",  "recieve.py", NULL);
            exit(0);
         }
         if(!strcmp(args[0], "report")) {
            execlp("/usr/local/bin/python3", "/usr/local/bin/python3",  "analyze.py", NULL);
            exit(0);
         }
      }
      else {
         wait(&i);
      }
   }
}