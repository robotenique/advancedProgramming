#ifndef GLOBALS_H
#define GLOBALS_H

#include <sched.h>
#include <time.h>

#define MAX_PROCESSES 32768
#define GLOBALS_AWAIT(x) while (!(x)) sched_yield();
//#define GLOBALS_AWAIT(x) while (!(x)) nanosleep((const struct timespec[]){{0, 10L}}, NULL);

#endif /*GLOBALS_H*/
