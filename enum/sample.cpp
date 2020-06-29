#include <iostream>

// Enum Example1
enum ENUM_EXE_01_F{
    EXE_YOUSO_01_01_F = 0,
    EXE_YOUSO_01_02_F = 5,
    EXE_YOUSO_01_03_F,
    EXE_YOUSO_01_04_F, /* Comment In */
    EXE_YOUSO_01_05_F, // Comment In
    EXE_YOUSO_01_06_F = 10, /* Comment In */ // CommentIn
    EXE_YOUSO_01_07_F = EXE_YOUSO_01_03_F, /* Comment In */ // CommentIn
    EXE_YOUSO_01_08_F = EXE_YOUSO_01_07_F + 1, /* Comment In */ // CommentIn
    EXE_YOUSO_01_08_F = EXE_YOUSO_01_07_F - 10, /* Comment In */ /* CommentIn
*/    EXE_YOUSO_01_09_F = EXE_YOUSO_01_07_F * EXE_YOUSO_01_08, /* Comment In */ // CommentIn
};
enum ENUM_EXE_02_F{
    EXE_YOUSO_02_01_F = EXE_YOUSO_01_08_F,};
        enum ENUM_EXE_03{EXE_YOUSO_03_01=0,EXE_YOUSO_03_02,};
void call() {
    std::cout << "Helloworld" << std::endl;
    printf("Helloworld");
}
int main(void){
    // main文
    call();
}
