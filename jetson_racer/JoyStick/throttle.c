#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>

int throttle(char* path) {
    int fd = open(path, O_RDONLY | O_NOCTTY);
    char buffer[32];
	int j = 0;    
	while(1) {
        int n = read(fd, buffer, sizeof(buffer));
        if (n < 0) fputs("read failed!\n", stderr);
        /*data*/
        int is_pressed = buffer[4];
        int direction = buffer[5];
        int operation = buffer[7];
        int toggle = buffer[6];
	if(toggle ==2) continue;
	//printf("%d",buffer[4]);
	//printf("%d",buffer[7]);


		if(j==6) {
        if (is_pressed==1) {
            printf("Pressed ");
        }
        //else printf("Released ");
        if(toggle == 1){
            switch(operation) {
                case 3:  printf("X");  return 1;
				case 1:  printf("B");  return 0;
		default: break;
            }
        }
	
        //if(direction==0x7f) printf("Turn Right");
        //if(direction==0xffffff80) printf("Turn Left");
        printf("\n");
		}
		j++;
    }
    return 0;

}
int main(){
    char* path = "/dev/input/by-id/usb-ShanWan_PC_PS3_Android-joystick";
    int x = throttle(path);
	//throttle(path);
    printf("%d",x);
    return x;
}
