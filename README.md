# RAG-mental-prescription-chatbot
HW4
# 🧾 RAG 心靈處方籤機器人  
**Mental Prescription Chatbot with Retrieval-Augmented Generation (RAG)**

這是一個結合語意檢索與對話生成的心靈輔助系統，能根據使用者輸入的當下心情或困擾，在資料庫中檢索出最相關的籤詩段落，並再透過模板生成具有溫柔陪伴語氣的「心靈處方籤」。

系統特色：
- 📌 使用向量檢索（FAISS + Sentence-Transformers）從文本庫中找出最相關段落
- 💬 根據檢索結果產生結構化心靈處方籤（Regulated Generation）
- 🚀 使用 Streamlit 建立互動介面，可部署至 Streamlit Cloud 進行展示
- 📚 所有模組與內容皆可本機執行，不依賴第三方大型 API

---

## 🧠 系統架構
系統採用 RAG（Retrieval-Augmented Generation）架構：

使用者輸入困擾
↓
向量檢索（FAISS）
↓
取得最相關籤詩段落
↓
(可選) 模板式生成（或 LLM 生成）
↓
顯示結構化心靈處方籤


---

## 📁 專案結構

RAG-mental-prescription-chatbot/
├─ data/
│ └─ quotes.txt # 籤詩庫文本
├─ rag_store/
│ ├─ faiss.index # 向量檢索索引
│ └─ chunks.npy # 對應段落文字
├─ app.py # Streamlit 介面
├─ rag.py # 向量檢索功能
├─ generator.py # 心靈處方籤生成模板
├─ ingest.py # 建立向量庫腳本
├─ requirements.txt # 雲端部署相依套件
└─ README.md # 專題說明文件


---

## 📌 安裝與本機執行

請先確認你已安裝 Python 3.8 以上版本。

1. 下載或 clone 此專案：

```bash
git clone https://github.com/NicoleChen0429/RAG-mental-prescription-chatbot.git
cd RAG-mental-prescription-chatbot

2. 安裝相依套件：
pip install -r requirements.txt

3. 如果尚未建立向量庫，可執行：
python ingest.py

4. 執行 Streamlit 介面：
streamlit run app.py

