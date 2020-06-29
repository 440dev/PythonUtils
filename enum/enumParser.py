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
values = []

class Values:
    def __init__(self, name, value=''):
        self.name=name
        self.value=value

class Enum:
    def __init__(self, name):
        self.name=name
        self.values = []
    def __str__(self):
        ret = self.name + '->'
        for y in self.values:
            ret = ret + '\n' + y.name + ':' + str(y.value)
        return ret

def Analyze(enumtext, valuelist):
    # TODO
    # 煩雑、4桁が限界で行っている。おそらく再起を使って二メモリずつ進めればいくらでも可能
    # 現在四則演算は+-のみ、*/は非対応
    prev = 0
    enumins = Enum(enumtext)
    for value in valuelist:
        valueins = Values(value[0])
        if value[1] == '':
            # 一つ目が空なら此処で終わり
            valueins.value = prev + 1
            prev = valueins.value
        elif value[1].isdecimal():
            # 一つ目が数値 さらに先まで見る
            valueins.value = int(value[1])
            if value[2] == '+':
                if value[3].isdecimal():
                    valueins.value += int(value[3])
                else:
                    found=next((t for t in values if t.name==value[3]) ,None)
                    valueins.value += found.value
            if value[2] == '-':
                if value[3].isdecimal():
                    valueins.value -= int(value[3])
                else:
                    found=next((t for t in values if t.name==value[3]) ,None)
                    valueins.value -= found.value
        else:
            # 一つ目が文字列
            # valuesから検索
            found=next((t for t in values if t.name==value[1]) ,None)
            if found:
                valueins.value = found.value
            if value[2] == '+':
                if value[3].isdecimal():
                    valueins.value += int(value[3])
                else:
                    found=next((t for t in values if t.name==value[3]) ,None)
                    valueins.value += found.value
            if value[2] == '-':
                if value[3].isdecimal():
                    valueins.value -= int(value[3])
                else:
                    found=next((t for t in values if t.name==value[3]) ,None)
                    valueins.value -= found.value
        prev = valueins.value
        values.append(valueins)
        enumins.values.append(valueins)

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

        value = enumtext[1].replace(' ','')
        valuelist = [valuelist for valuelist in re.findall(r'(\w+)=?(\w*)([\+|\-|\*|\/])?(\w+)?,', value)]
        Analyze(enumtext[0], valuelist)

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
