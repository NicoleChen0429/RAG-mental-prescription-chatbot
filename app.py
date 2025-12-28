import streamlit as st
from generator import generate_prescription
from rag import RAGRetriever

st.set_page_config(page_title="心靈處方籤機器人（RAG）", layout="centered")

st.title("🧾 心靈處方籤機器人（RAG）")
st.caption("輸入你的心情或困擾，我會從籤詩庫中找出最貼近的一段話給你。")

@st.cache_resource
def get_retriever():
    return RAGRetriever()

try:
    retriever = get_retriever()
except Exception as e:
    st.error("RAG 向量庫不存在或載入失敗。請確認已把 rag_store/ 一起上傳到 GitHub。")
    st.exception(e)
    st.stop()

query = st.text_area(
    "你現在的心情/困擾是什麼？",
    placeholder="例如：我最近很焦慮，覺得自己一直失敗…",
    height=120
)

k = st.slider("想找幾段候選籤詩？", 1, 5, 3)

if st.button("🔎 抽出最適合的一張籤", use_container_width=True):
    if not query.strip():
        st.warning("請先輸入你的心情或困擾。")
    else:
        results = retriever.search(query, k=k)

        best = results[0]

        st.subheader("🎯 你的心靈處方籤")

        with st.spinner("正在為你整理這張處方籤…"):
            prescription = generate_prescription(query, best["text"])

        st.markdown(prescription)

        st.divider()
        st.subheader("📌 其他相近候選（可選）")
        for i, item in enumerate(results, 1):
            with st.expander(f"TOP {i}（相似度 {item['score']:.3f}）"):
                st.write(item["text"])
