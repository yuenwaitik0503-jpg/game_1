import streamlit as st
import random
from streamlit_sortables import sort_items

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="顏色方塊排序謎題", layout="centered")

# --- 2. 顏色資料庫（使用最純粹的 Emoji 方塊作為唯一 Key） ---
COLOR_MAP = {
    "🟥": "紅色",
    "🟩": "綠色",
    "🟦": "藍色",
    "🟪": "紫色",
    "🟧": "橘色",
    "🟨": "黃色",
    "🟫": "棕色",
    "⬛": "黑色"
}
# 取出所有的純顏色方塊符號
COLOR_LIST = list(COLOR_MAP.keys())

# --- 3. 初始化遊戲狀態 ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 4  # 預設 4 個方塊
    # 隨機抽取正確答案（純方塊符號清單，例如 ['🟥', '🟩', '🟦', '🟪']）
    st.session_state.secret_sequence = random.sample(COLOR_LIST, st.session_state.difficulty)
    # 玩家目前的排列順序（初始先複製一份正確答案，再打亂給玩家排）
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
        
    if st.button("🔄 重新開啟新局", use_container_width=True):
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
    secret_display = " ".join(st.session_state.secret_sequence)
    st.markdown(f"<h1 style='letter-spacing: 15px; text-align: center;'>{secret_display}</h1>", unsafe_allow_html=True)
    if st.session_state.game_over:
        st.success(f"🎉 恭喜闖關成功！共花了 {len(st.session_state.history)} 回合！")
else:
    # 未揭曉時顯示鎖定狀態
    locks = " ".join(["🔒"] * st.session_state.difficulty)
    st.warning(f"內部順序已鎖定：{locks} （請調整下方方塊進行挑戰）")

st.markdown("---")

# 【步驟 B】🖐️ 玩家操作區（純淨流暢的拖曳引擎）
st.subheader("🖐️ 玩家操作區")
st.caption("👇 請直接用滑鼠點住顏色方塊「左右拖拉」來調換順序：")

# 安全機制：確保拖曳的內容永遠是最純粹的方塊，且數量與當前難度絕對一致
drag_items = [item for item in st.session_state.player_sequence if item in COLOR_LIST]
if len(drag_items) != st.session_state.difficulty:
    drag_items = list(st.session_state.secret_sequence)

# 呼叫橫向拖曳組件
sorted_emojis = sort_items(drag_items, direction="horizontal", key=f"drag_engine_r{len(st.session_state.history)}_d{st.session_state.difficulty}")

# 只要玩家一拖曳，立刻即時更新最新順序
if sorted_emojis:
    st.session_state.player_sequence = list(sorted_emojis)

st.write("")
st.write("")

# 【步驟 C】✅ 功能控制按鈕（功能保證 100% 精準）
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
        emoji_line = " ".join(record["sequence"])
        st.markdown(f"""
        **第 {record["round"]} 回合**：  
        <span style='font-size: 24px; letter-spacing: 8px;'>{emoji_line}</span>  
        🎯 位置與顏色完全正確： `{record["correct"]}` / {st.session_state.difficulty} 個
        """, unsafe_allow_html=True)
