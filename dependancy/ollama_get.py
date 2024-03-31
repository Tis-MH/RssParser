import requests
import json
import re

def info_extract(title, retires=3):
    def question(title):
        content = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "yi",
                "messages": [
                    {
                        "role": "user",
                        "content": title
                        + " 提取这条信息中的字幕组, 标题, 清晰度和集数, 按格式 {字幕组: '', 标题: '', 清晰度: '', 集数: ''} 返回 ",
                    },
                    # {"role": "assistant", "content": "due to rayleigh scattering."},
                    # {"role": "user", "content": "how is that different than mie scattering?"},
                ],
                "stream": True,
            },
        )

        res = ""
        lines = content.text.split("\n")
        for i in lines[:-1]:
            print(i)
            res += json.loads(i)["message"]["content"]
        return res

    for _ in range(retires):
        answer = question(title)
        try:
            return re.search("{.*?}", answer)
        except Exception as e:
            print(e)

    raise TimeoutError

if __name__ == "__main__":
    print(
        info_extract(
            "【喵萌奶茶屋】★01月新番★[反派千金Lv99 雖然我是隱藏BOSS但我可不是魔王 / Akuyaku Reijou Level 99][03][1080p][繁日雙語][招募翻譯]"
        )
    )
