#Task_1b


inp1= open('input1b.txt','r')
out1=open('output1b.txt','w')


test_case=int(inp1.readline())


for i in range(0, test_case):
  a=(inp1.readline()).split(' ')[1:]

  first=int(a[0])
  op=a[1]
  last=int(a[2])


  if op=='+':
    res= first+last
    print('The result of {} {} {} is {}'.format(first,op,last,res),file=out1)

  if op=='-':
    res= first-last
    print('The result of {} {} {} is {}'.format(first,op,last,res),file=out1)

  if op=='*':
    res= first*last
    print('The result of {} {} {} is {}'.format(first,op,last,res),file=out1)


  if op=='/':

    res= first/last
    print('The result of {} {} {} is {}'.format(first,op,last,res),file=out1)


out1.close()