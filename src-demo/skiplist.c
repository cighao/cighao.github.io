#include "stdio.h"
#include "stdlib.h"

#define MAX_LEVEL 4

 //每个结点的结构
typedef struct nodeStructure{
	int key;
	int value;
	struct nodeStructure *forward[1];
}nodeStructure;

//跳表的结构 
typedef struct skiplist{
	int level;
	nodeStructure *header;
}skiplist;

//结点的创建
nodeStructure* createNode(int level,int key,int value){
	nodeStructure *ns = (nodeStructure *)malloc(sizeof(nodeStructure)+level*sizeof(nodeStructure *));
	ns->key = key;
	ns->value = value;
	return ns;
}

//列表的初始化
skiplist* createSkiplist(){
	skiplist *sl = (skiplist *)malloc(sizeof(skiplist));
	sl->level = 0;
	sl->header = createNode(MAX_LEVEL-1,0,0); //初始化头部
	int i;
	for(i=0;i<MAX_LEVEL;i++){
		sl->header->forward[i] = NULL; //头部的每层指向NULL
	}
	return sl;
} 

//随机产生层数
static int randomLevel(){
	int k=1;
	while(rand()%2)
		k++;
	k = (k<MAX_LEVEL)?k:MAX_LEVEL;
	return k;
}

//插入
int insert(skiplist *sl,int key, int value){
	nodeStructure *update[MAX_LEVEL];  
	nodeStructure *p, *q = NULL;  
	p=sl->header;  
	int k=sl->level,i;
	//从最高层往下查找需要插入的位置，填充update
	for(i=k-1;i>=0;i--){
		while((q=p->forward[i])&&(q->key<key)){
			p=q;
		}
		update[i] = p;
	}
	//不插入相同的key
	if(q&&q->key == key)
		return 0;
	//产生一个随机层数
	k = randomLevel();
	if(k>(sl->level)){
		for(i=sl->level;i<k;i++){
			update[i] = sl->header;
		}
		sl->level = k;
	}
	//新建一个待插入结点
	q = createNode(k,key,value);
	//逐层更新节点的指针
	for(i=0;i<k;i++){
		q->forward[i] = update[i]->forward[i];
		update[i]->forward[i]=q;
	}
	return 1;
}

//删除
int deleteSL(skiplist *sl,int key){
	nodeStructure *update[MAX_LEVEL];  
	nodeStructure *p,*q=NULL;  
	p=sl->header;  
	int k=sl->level;  //从最高层开始搜  
	int i;
	for(i=k-1; i >= 0; i--){
		while((q=p->forward[i])&&(q->key<key)){
			p=q;
		}
		update[i]=p;
	}
	if(q&&q->key==key){
		//逐层删除，和普通列表删除一样  
		for(i=0; i<sl->level; i++){    
			if(update[i]->forward[i]==q){
				update[i]->forward[i]=q->forward[i];    
			}
		}   
		free(q);  
		//如果删除的是最大层的节点，那么需要重新维护跳表的  
		for(i=sl->level-1; i >= 0; i--){    
			if(sl->header->forward[i]==NULL){    
				sl->level--;    
			}
		}
		return 1;  
	}else  
		return 0;
}

//查找
int search(skiplist *sl,int key)  {  
	nodeStructure *p,*q=NULL;  
	p=sl->header;  
	//从最高层开始搜  
	int k=sl->level; 
	int i;
	for(i=k-1; i >= 0; i--){  
		while((q=p->forward[i])&&(q->key<=key)){  
			if(q->key == key){
				return q->value;
			}
			p=q;  
		}
	}
	return -1;  
}  

//
int main(){
	skiplist *sl=createSkiplist();
	int i;
	for(i=0;i<1000000;i++){
		insert(sl,random(),random());
	}
	printf("%d\n",search(sl,4));
	deleteSL(sl,4);
	printf("%d\n",search(sl,4));
	return 0;
}
