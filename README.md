# automake
automake for c implemented by python

使用：
automake.exe [main_file.c] [makefile]

示例：
automake.exe E:/word2vec/word2vec.c E:/word2vec/makefile

word2vec: word2vec.o random.o 
	gcc -g -o word2vec word2vec.o random.o 
word2vec.o: word2vec.c E:/cutils/random.h 
	gcc -g -c word2vec.c 
random.o: E:/cutils/random.c E:/cutils/random.h 
	gcc -g -c E:/cutils/random.c

