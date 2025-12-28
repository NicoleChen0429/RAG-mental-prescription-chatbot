# generator.py
# 規則式（Template-based）Generation：不依賴 OpenAI / API Key

def generate_prescription(user_query: str, quote_text: str) -> str:
    """
    規則式（Template-based）Generation
    不依賴任何外部 API，可穩定 demo 與交作業
    """

    user_query = (user_query or "").strip()

    # 可選：把使用者輸入做成一行摘要（太長就截斷）
    if len(user_query) > 60:
        user_line = user_query[:60] + "…"
    elif user_query:
        user_line = user_query
    else:
        user_line = "（你還沒輸入心情，但我仍想給你一段溫柔的話）"

    return f"""\
【給現在的你】
會有這樣的感受，是可以被理解的。
你願意停下來傾聽自己，本身就是一種勇氣。

【你此刻的心情】
{user_line}

【你的心靈處方籤】
{quote_text}

【小提醒】
- 不需要急著找到答案，慢慢走也是前進
- 今天只要完成一件照顧自己的小事，就已經很值得肯定

【給你的話】
請相信，這段路不會白走，你正在成為更溫柔地理解自己的人。
"""
