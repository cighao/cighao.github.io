#python多线程示例

from multiprocessing.dummy import Pool as ThreadPool

def printStr(str):
    print(str)
    return str

if __name__ == '__main__':
    strList = ['hello1','hello2','hello3','hello4']
    #两行代码即可搞定
    pool = ThreadPool(4)  #这里的4可以是cpu的核数
    results = pool.map(printStr,strList)

    print("结果")
    for each in results:
        print(each)