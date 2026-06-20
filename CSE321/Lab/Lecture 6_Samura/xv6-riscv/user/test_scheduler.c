#include "kernel/types.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
  if (argc != 2){
    printf("Usage: test_scheduler <tickets>\n");
    exit(1);
  }

  int tickets = atoi(argv[1]);
  // Set the tickets for this process
  if (settickets(tickets) < 0){
    printf("settickets failed\n");
    exit(1);
  }

  // Spin in an infinite loop to use CPU time
  while(1){
  }

  exit(0);
}
