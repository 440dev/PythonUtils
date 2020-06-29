import re

sample = """
#include <iostream>
// Enum Example1
enum ENUM_EXE_01{
    EXE_YOUSO_01_01 = 0,
    EXE_YOUSO_01_02 = 5,
    EXE_YOUSO_01_03,
    EXE_YOUSO_01_04, /* Comment In */
    EXE_YOUSO_01_05, // Comment In
    EXE_YOUSO_01_06 = 10, /* Comment In */ // CommentIn
    EXE_YOUSO_01_07 = EXE_YOUSO_01_03, /* Comment In */ // CommentIn
    EXE_YOUSO_01_08 = EXE_YOUSO_01_07 + 1, /* Comment In */ // CommentIn
    EXE_YOUSO_01_08 = EXE_YOUSO_01_07 - 10, /* Comment In */ /* CommentIn
*/    EXE_YOUSO_01_09 = EXE_YOUSO_01_07 * EXE_YOUSO_01_08, /* Comment In */ // CommentIn
};
enum ENUM_EXE_02{
    EXE_YOUSO_02_01 = EXE_YOUSO_01_08,};
        enum ENUM_EXE_03{EXE_YOUSO_03_01=0,EXE_YOUSO_03_02,};
void call() {
    std::cout << "Helloworld" << std::endl;
    printf("Helloworld");
}
int main(void){
    // main文
    call();
}
"""

def EnumParser(textstr):
    textlist = textstr.splitlines()

    # 余分なものを削ぎ落とす
    # 空白 /* */ or // or /* or */の周りで実体のコードに影響を与えない箇所を消す
    textlist = [re.sub(r'(\/\*.+?\*\/|\/\/.+|\/\*.+|^(\/\*).+\*\/)', '', text) for text in textlist]
    textline = ''.join([text for text in textlist if text !=''])

    for enumtext in re.findall(r'enum\s+(.*?){(.*?)};', textline):
        print('Enum:' + enumtext[0])
        youso = enumtext[1].replace(' ','')
        print('Youso')
        for yousolist in re.findall(r'(\w+)=?(\w*)([\+|\-|\*|\/])?(\w+)?,', youso):
            print(yousolist)
        print()

if __name__ == "__main__":
    import sys
    args = sys.argv

    if len(args) > 1:
        # Open File
        with open(args[1],'r',encoding='utf-8') as f:
            EnumParser(f.read())
    else:
        EnumParser(sample)
