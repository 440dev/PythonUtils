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
    EXE_YOUSO_01_07 = 3, /* Comment In */ // CommentIn
    EXE_YOUSO_01_08 = EXE_YOUSO_01_07 + 1, /* Comment In */ // CommentIn
    EXE_YOUSO_01_09 = EXE_YOUSO_01_07 - 10, /* Comment In */ /* CommentIn
*/    EXE_YOUSO_01_10 = EXE_YOUSO_01_07 + EXE_YOUSO_01_08, /* Comment In */ // CommentIn
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

enums = []
yousos = []

class Youso:
    def __init__(self, name, value=''):
        self.name=name
        self.value=value

class Enum:
    def __init__(self, name):
        self.name=name
        self.youso = []
    def __str__(self):
        ret = self.name + '->'
        for y in self.youso:
            ret = ret + '\n' + y.name + ':' + str(y.value)
        return ret

def Analyze(enumtext, yousolist):
    # TODO
    # 煩雑、4桁が限界で行っている。おそらく再起を使って二メモリずつ進めればいくらでも可能
    # 現在四則演算は+-のみ、*/は非対応
    prev = 0
    enumins = Enum(enumtext)
    for youso in yousolist:
        yousoins = Youso(youso[0])
        if youso[1] == '':
            # 一つ目が空なら此処で終わり
            yousoins.value = prev + 1
            prev = yousoins.value
        elif youso[1].isdecimal():
            # 一つ目が数値 さらに先まで見る
            yousoins.value = int(youso[1])
            if youso[2] == '+':
                if youso[3].isdecimal():
                    yousoins.value += int(youso[3])
                else:
                    found=next((t for t in yousos if t.name==youso[3]) ,None)
                    yousoins.value += found.value
            if youso[2] == '-':
                if youso[3].isdecimal():
                    yousoins.value -= int(youso[3])
                else:
                    found=next((t for t in yousos if t.name==youso[3]) ,None)
                    yousoins.value -= found.value
        else:
            # 一つ目が文字列
            # yousosから検索
            found=next((t for t in yousos if t.name==youso[1]) ,None)
            if found:
                yousoins.value = found.value
            if youso[2] == '+':
                if youso[3].isdecimal():
                    yousoins.value += int(youso[3])
                else:
                    found=next((t for t in yousos if t.name==youso[3]) ,None)
                    yousoins.value += found.value
            if youso[2] == '-':
                if youso[3].isdecimal():
                    yousoins.value -= int(youso[3])
                else:
                    found=next((t for t in yousos if t.name==youso[3]) ,None)
                    yousoins.value -= found.value
        prev = yousoins.value
        yousos.append(yousoins)
        enumins.youso.append(yousoins)

    print(str(enumins))
    return enumins

def EnumParser(textstr):
    textlist = textstr.splitlines()

    # 余分なものを削ぎ落とす
    # 空白 /* */ or // or /* or */の周りで実体のコードに影響を与えない箇所を消す
    textlist = [re.sub(r'(\/\*.+?\*\/|\/\/.+|\/\*.+|^(\/\*)\*\/)', '', text) for text in textlist]
    textline = ''.join([text for text in textlist if text !=''])

    for enumtext in re.findall(r'enum\s+(.*?){(.*?)};', textline):
        #print('Enum:' + enumtext[0])

        youso = enumtext[1].replace(' ','')
        #print('Youso')
        yousolist = [yousolist for yousolist in re.findall(r'(\w+)=?(\w*)([\+|\-|\*|\/])?(\w+)?,', youso)]
        #print(yousolist)
        Analyze(enumtext[0], yousolist)

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
