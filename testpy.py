# encoding=utf-8
import re
import jieba
import jieba.posseg as pseg

line = '迪卡侬滑板车儿童1-3-6岁男女孩单脚小孩宝宝折叠溜溜划板OXELO-S'

def compress_text(text: str):
    jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
    temp1 = list(jieba.cut(text, cut_all=False))

    char_list = [i for i in list(jieba.cut(text, cut_all=False)) if i != ' ']  # 把字符串转化列表自动按单个字符分词了
    # print(char_list)

    list1 = []
    list1.append(char_list[0])
    for char in char_list:
        if char not in list1:
            list1.append(char)

    return ''.join(list1)

print(compress_text(line))