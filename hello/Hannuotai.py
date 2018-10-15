#汉诺塔:n个圆盘的时候 2的n次方减1; abc代表三根柱子
def Hannuotai(n,a,b,c):
    if n==1:
        print(a,'>>>>',c)
    else:
        Hannuotai(n-1,a,c,b) #把a上的(n-1)个盘子借助c移到b上
        print(a,'>>>>',c)
        Hannuotai(n-1,b,a,c)
#调用
#Hannuotai(4,'A','B','C')
L=list(range(100))
print(L[:2])
print(L[2,8])
#前10个数，每两个取一个
print(L[:10:2])
#所有数，每30个取一个
print(L[::30])
#倒数的两个
print(L[-2:])
#取倒数第三第四个
print(L[-2:2:])

