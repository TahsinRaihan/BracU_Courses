#include "kernel/types.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
  if (argc != 2) {
    printf("Usage: test_scheduler <tickets>\n");
    exit(1);
  }

  int tickets = atoi(argv[1]);
  if (settickets(tickets) < 0) {
    printf("Error: settickets failed. Tickets must be > 0\n");
    exit(1);
  }

  // Spin in an infinite loop to keep the process alive
  while (1) {
  }

  return 0;
}
