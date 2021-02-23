"""
BullshitGenerator extension for ME

@author: Reproduce by Tang142857
@project: MyEditor
@file: maker.py
@date: 2021-02-23
"""
import os, re
import random, readJSON

data = readJSON.read_json("data.json")
famous_saying = data["famous"]  # a 代表前面垫话，b代表后面垫话
foreground_saying = data["before"]  # 在名人名言前面弄点废话
background_saying = data['after']  # 在名人名言后面弄点废话
litter = data['bosh']  # 代表文章主要废话来源

topic = "学生会退会"

repeat_index = 2


def shuffle_list(l):
    global repeat_index
    saying_pool = list(l) * repeat_index
    while True:
        random.shuffle(saying_pool)
        for element in saying_pool:
            yield element


next_sentence = shuffle_list(litter)
next_famous_saying = shuffle_list(famous_saying)


def get_famous_saying():
    global next_famous_saying
    result = next(next_famous_saying)
    result = result.replace("a", random.choice(foreground_saying))
    result = result.replace("b", random.choice(background_saying))
    return result


def new_passage():
    # result = ". "
    result = "\n"
    # result += ""
    return result

def make(topic):
    """
    Make a litter ,
    """
if __name__ == "__main__":
    topic = input("请输入文章主题:")
    for x in topic:
        tmp = str()
        while (len(tmp) < 6000):
            branch = random.randint(0, 100)
            if branch < 5:
                tmp += new_passage()
            elif branch < 20:
                tmp += get_famous_saying()
            else:
                tmp += next(next_sentence)
        tmp = tmp.replace("x", topic)
        print(tmp)