import requests
import json
import re


def get_entity():
    import sqlite3

    file_path = "sqlite3.sql"
    db = sqlite3.connect(file_path)
    cursor = db.cursor()
    res = cursor.execute("select * from entity")
    for i in res.fetchall():
        yield i[0]


def info_extract(title, retires=3):
    def question(title):
        content = requests.post(
            "http://localhost:11434/api/generate",
            # json={
            #     "model": "codellama:7b",
            #     "messages": [
            #         {
            #             "role": "user",
            #             "content": title
            #             + " 按格式 {字幕组: '', 标题: '', 清晰度: '', 集数: ''} 提取这条信息中的字幕组, 标题, 清晰度和集数",
            #         },
            #         # {"role": "assistant", "content": "due to rayleigh scattering."},
            #         # {"role": "user", "content": "how is that different than mie scattering?"},
            #     ],
            #     "stream": True,
            # },
            json={
                "model": "codellama:7b",
                "prompt": title
                + " 按格式 {字幕组: '', 标题: '', 清晰度: '', 集数: ''} 提取这条信息中的字幕组, 标题, 清晰度和集数",
                "stream": False,
            },
        )

        print(content.json()["response"])

    question(title)


if __name__ == "__main__":
    title = "	[jibaketa合成&音頻壓制][TVB粵語]閃躍吧！星夢☆頻道 / 美妙☆频道 / Kiratto Pri-chan - 98 [粵日雙語+內封繁體中文字幕][WEB 1920x1080 x264 AACx2 SRT TVB CHT]"  # "【喵萌奶茶屋】★01月新番★[反派千金Lv99 雖然我是隱藏BOSS但我可不是魔王 / Akuyaku Reijou Level 99][03][1080p][繁日雙語][招募翻譯]"
    info_extract(title)
    # for title in get_entity():
    #     print(title)
    #     print(
    #         info_extract(
    #             title
    #         )
    #     )
