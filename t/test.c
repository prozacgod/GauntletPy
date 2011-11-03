#define python_ignore /*  <- Leave this line break
"""*/

#include <asm/ioctl.h>
#include <linux/input.h>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>

#define test_bit(bit, array)    (array[bit/8] & (1<<(bit%8)))

int main(int argc, char* argv[]) {
	printf("%u\n", _IOC_DIRSHIFT);
	printf("%u\n", _IOC_TYPESHIFT);
	printf("%u\n", _IOC_NRSHIFT);
	printf("%u\n", _IOC_SIZESHIFT);
	
	printf("%u\n\n", _IOC_SIZEBITS);
	
	printf("%X\n", _IOC(_IOC_READ, 0, 0, 0));
	
	printf("%X\n", EVIOCGBIT(0, EV_MAX));


	int fd = 0;
	int yalv = 0;
	
	if ((fd = open(argv[1], O_RDONLY)) < 0) {
		perror("evdev open");
		exit(1);
	}

    unsigned char evtype_b[EV_MAX/8 + 1] = { };

	memset(evtype_b, 0, sizeof(evtype_b));
	if (ioctl(fd, EVIOCGBIT(0, EV_MAX), evtype_b) < 0) {
		perror("evdev ioctl");
	}

	printf("Supported event types:\n");

	for (yalv = 0; yalv < EV_MAX; yalv++) {
		if (test_bit(yalv, evtype_b)) {
		    /* the bit is set in the event types list */
		    printf("  Event type 0x%02x ", yalv);
		    switch ( yalv)
		        {
		        case EV_SYN :
		            printf(" (Synch Events)\n");
		            break;
		        case EV_KEY :
		            printf(" (Keys or Buttons)\n");
		            break;
		        case EV_REL :
		            printf(" (Relative Axes)\n");
		            break;
		        case EV_ABS :
		            printf(" (Absolute Axes)\n");
		            break;
		        case EV_MSC :
		            printf(" (Miscellaneous)\n");
		            break;
		        case EV_LED :
		            printf(" (LEDs)\n");
		            break;
		        case EV_SND :
		            printf(" (Sounds)\n");
		            break;
		        case EV_REP :
		            printf(" (Repeat)\n");
		            break;
		        case EV_FF :
		        case EV_FF_STATUS:
		            printf(" (Force Feedback)\n");
		            break;
		        case EV_PWR:
		            printf(" (Power Management)\n");
		            break;
		        default:
		            printf(" (Unknown: 0x%04hx)\n",
		         yalv);
		    }
		}
	}

	close(fd);
	
}
/* """ # */ /*
# python code
# taken from <asm/ioctl.h>
# look for errors here, may be platform specific (likely compatible across all x86 architectures tho

_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2

_IOC_NRBITS    = 8
_IOC_TYPEBITS  = 8
_IOC_SIZEBITS  = 14
_IOC_DIRBITS   = 2

_IOC_NRMASK    = ((1 << _IOC_NRBITS) - 1)
_IOC_TYPEMASK  = ((1 << _IOC_TYPEBITS) - 1)
_IOC_SIZEMASK  = ((1 << _IOC_SIZEBITS) - 1)
_IOC_DIRMASK   = ((1 << _IOC_DIRBITS) - 1)

_IOC_NRSHIFT   = 0
_IOC_TYPESHIFT = (_IOC_NRSHIFT+_IOC_NRBITS)
_IOC_SIZESHIFT = (_IOC_TYPESHIFT+_IOC_TYPEBITS)
_IOC_DIRSHIFT  = (_IOC_SIZESHIFT+_IOC_SIZEBITS)

def _IOC(dir, type, nr, size):
	return (dir << _IOC_DIRSHIFT) | (type << _IOC_TYPESHIFT) | (nr <<  _IOC_NRSHIFT) | (size << _IOC_SIZESHIFT)

# taken <linux/input.h>

EV_MAX = 0x1f

def EVIOCGBIT(ev, len):
	return _IOC(_IOC_READ, ord('E'), 0x20 + ev, len)


def hexInt(val, size=8):
	return ("%0"+ str(size) + "X") % (val) 
	
print hexInt(_IOC(_IOC_READ, 0, 0, 0))
print hexInt(EVIOCGBIT(0, EV_MAX))

# */

