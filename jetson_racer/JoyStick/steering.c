#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>


//buffer[5] :: 200 LEFT | 177 RIGHT
int steering(char* path){
    int fd = open(path, O_RDONLY | O_NOCTTY);
    char buffer[32];
	int j=0;
    while(1){
		//if( j == 5){
        int n = read(fd, buffer, sizeof(buffer));
        if (n < 0) fputs("read failed!\n", stderr);
        /*data*/
        short is_pressed = buffer[4];
        int direction = buffer[5];
        short operation = buffer[7];
        short toggle = buffer[6];
		if (toggle == 2) {	
/*
        if (is_pressed==1 || is_pressed == 0xffffffff) {
            printf("Pressed ");
        }
        else printf("Released ");

        if(toggle == 1){
            switch(operation){
                //case 0: printf("Y"); break;
                case 1:  return -1;
                case 2:  return 0;
                case 3:  return 1;
                default: return 0;
            }
        }

*/

        if(direction==128) {
			printf("GO LEFT");	
			printf("\n");		
			return 0;
		}
        if(direction==127) {
			printf("GO RIGHT");
			printf("\n");
			return 1;
		}
        printf("\n");
		

    }
j++;
	
}
    return 7;
//}
}
float main(){
    char* path = "/dev/input/by-id/usb-ShanWan_PC_PS3_Android-joystick";
  //printf("%f",steering(path));
	int x = steering(path);
return x;

}
