#Task_1
inp=open('input1a.txt','r')
out=open('output1a.txt','w')

test_case=int(inp.readline())

for i in range(0,test_case):
    num=int(inp.readline())
    check=num&1
    if check==0:
        print('{} is a Even number'.format(num),file=out)
    else:
        print('{} is a Odd number'.format(num),file=out)