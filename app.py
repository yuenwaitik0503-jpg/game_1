import streamlit as st
import random
from streamlit_sortables import sort_items

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="顏色方塊排序謎題", layout="centered")

# --- 2. 顏色資料庫（只使用最直覺、不會跑版的 Emoji 彩色方塊） ---
COLOR_MAP = {
    "🟥 紅色方塊": "🟥",
    "🟩 綠色方塊": "🟩",
    "🟦 藍色方塊": "🟦",
    "🟪 紫色方塊": "🟪",
    "🟧 橘色方塊": "🟧",
    "🟨 黃色方塊": "🟨",
    "🟫 棕色方塊": "🟫",
    "⬛ 黑色方塊": "⬛"
}
COLOR_LIST = list(COLOR_MAP.keys())

# --- 3. 初始化遊戲狀態 ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 4  # 預設 4 個方塊
    # 隨機抽取正確答案
    st.session_state.secret_sequence = random.sample(COLOR_LIST, st.session_state.difficulty)
    # 玩家目前的排列順序（初始先打亂）
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    random.shuffle(st.session_state.player_sequence)
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# 重置遊戲安全函數
def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    st.session_state.secret_sequence = random.sample(COLOR_LIST, difficulty_num)
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    random.shuffle(st.session_state.player_sequence)
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# --- 4. 側邊欄控制 ---
with st.sidebar:
    st.header("⚙️ 遊戲設定")
    new_diff = st.slider("選擇方塊數量 (難度)", min_value=3, max_value=6, value=st.session_state.difficulty)
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    if st.button("🔄 重新開始新局", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()

# --- 5. 主畫面主要邏輯區 ---
st.title("🧪 顏色方塊排序謎題")
st.write("請用滑鼠直接「左右拖曳」下方的顏色方塊，排好順序後點擊檢查！")
st.markdown("---")

# 【步驟 A】📦 神秘箱子區
st.subheader("📦 神秘箱子")
if st.session_state.show_answer or st.session_state.game_over:
    # 遊戲結束或揭曉答案時，秀出正確的方塊順序
    secret_emojis = [COLOR_MAP[name] for name in st.session_state.secret_sequence]
    st.markdown(f"<h1 style='letter-spacing: 20px;'>{' '.join(secret_emojis)}</h1>", unsafe_allow_html=True)
    if st.session_state.game_over:
        st.success(f"🎉 恭喜闖關成功！共花了 {len(st.session_state.history)} 回合！")
else:
    st.warning("🔒 箱子內藏有正確的顏色順序（請調整下方方塊進行挑戰）")

st.markdown("---")

# 【步驟 B】🖐️ 玩家操作區（純淨流暢的拖曳引擎）
st.subheader("🖐️ 玩家操作區")
st.caption("👇 請直接用滑鼠點住方塊「左右拖拉」來調換順序：")

# 這裡我們只放純粹的 Emoji 讓玩家拖曳，完全不帶任何干擾的文字
drag_items = [COLOR_MAP[name] for name in st.session_state.player_sequence]

# 調用最穩定的橫向拖曳組件
sorted_emojis = sort_items(drag_items, direction="horizontal", key=f"drag_game_{len(st.session_state.history)}")

# 將玩家拖曳後的最新 Emoji 順序，反向解析並存回系統
if sorted_emojis:
    # 建立一個從 Emoji 對應回原本名稱的反查表
    reverse_map = {v: k for k, v in COLOR_MAP.items()}
    st.session_state.player_sequence = [reverse_map[emoji] for emoji in sorted_emojis]

st.write("")
st.write("")

# 【步驟 C】✅ 功能控制按鈕（與方塊完全分離，外觀絕對正常）
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("✅ 確定檢查答案", type="primary", use_container_width=True, disabled=st.session_state.game_over):
        current_order = list(st.session_state.player_sequence)
        
        # 100% 精準比對位置與顏色完全正確的數量
        correct_count = sum(1 for p, s in zip(current_order, st.session_state.secret_sequence) if p == s)
        
        # 紀錄至歷史比對紀錄
        st.session_state.history.append({
            "round": len(st.session_state.history) + 1,
            "sequence": current_order,
            "correct": correct_count
        })
        
        # 如果全對則通關
        if correct_count == st.session_state.difficulty:
            st.session_state.game_over = True
        st.rerun()

with btn_col2:
    if st.button("👁️ 揭曉神秘箱答案", type="secondary", use_container_width=True):
        st.session_state.show_answer = True
        st.rerun()

st.markdown("---")

# 【步驟 D】📊 歷史比對紀錄區
st.subheader("📊 歷史比對紀錄")
if not st.session_state.history:
    st.info("尚未提交任何答案，開始拖動方塊吧！")
else:
    for record in reversed(st.session_state.history):
        emoji_line = " ".join([COLOR_MAP[name] for name in record["sequence"]])
        st.markdown(f"""
        **第 {record["round"]} 回合**：  
        <span style='font-size: 24px;'>{emoji_line}</span>  
        🎯 位置與顏色完全正確： `{record["correct"]}` / {st.session_state.difficulty} 個
        """, unsafe_allow_html=True)
