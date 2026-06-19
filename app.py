import streamlit as st
import random

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="顏色方塊排序謎題", layout="centered")

# --- 2. 顏色資料庫（最純粹的設計，鍵名即是 Emoji） ---
COLOR_MAP = {
    "🟥": "紅色", "🟩": "綠色", "🟦": "藍色", "🟪": "紫色", 
    "🟧": "橘色", "🟨": "黃色", "🟫": "棕色", "⬛": "黑色", 
    "⬜": "白色", "🟪": "紫色"
}
COLOR_LIST = list(COLOR_MAP.keys())

# --- 3. 初始化遊戲狀態 (Session State) ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 4  # 預設難度
    st.session_state.secret_sequence = COLOR_LIST[:st.session_state.difficulty]
    random.shuffle(st.session_state.secret_sequence) # 秘密正確答案
    
    # 玩家目前的排列（初始為空，讓玩家自己選）
    st.session_state.player_sequence = [None] * st.session_state.difficulty
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# 重置遊戲安全函數
def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    # 確保重新抽取的答案絕不重複
    st.session_state.secret_sequence = random.sample(COLOR_LIST, difficulty_num)
    st.session_state.player_sequence = [None] * difficulty_num
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# --- 4. 遊戲控制側邊欄 ---
with st.sidebar:
    st.header("⚙️ 遊戲控制")
    new_diff = st.slider("選擇方塊數量 (難度)", min_value=3, max_value=8, value=st.session_state.difficulty)
    
    # 只要難度一變，立刻安全重置，防止緩存殘留
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    if st.button("🔄 開始新遊戲", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()

# --- 5. 主畫面主要邏輯區 ---
st.title("🧪 顏色方塊排序謎題")
st.write("請在操作區選擇顏色方塊的順序，讓它與箱子內隱藏的正確答案完全一致！")
st.markdown("---")

# 【步驟 A】📦 神秘箱子區
st.subheader("📦 神秘箱子")
if st.session_state.show_answer or st.session_state.game_over:
    # 橫向並排顯示正確答案
    secret_cols = st.columns(st.session_state.difficulty)
    for i, color in enumerate(st.session_state.secret_sequence):
        with secret_cols[i]:
            st.markdown(f"<h1 style='text-align: center; margin:0;'>{color}</h1>", unsafe_allow_html=True)
    if st.session_state.game_over:
        st.success(f"🎉 恭喜闖關成功！共花了 {len(st.session_state.history)} 回合！")
else:
    # 鎖定狀態
    lock_box = " ".join(["🔒"] * st.session_state.difficulty)
    st.warning(f"內部順序： {lock_box} （請在下方排列完成後檢查）")

st.markdown("---")

# 【步驟 B】🖐️ 玩家操作區（確保操作絕對流暢、不影響按鈕）
st.subheader("🖐️ 玩家操作區")
st.caption("請為下方由左至右的各個位置，挑選你認為正確的顏色方塊：")

# 建立橫向排列的下拉選單，讓玩家一目了然
player_cols = st.columns(st.session_state.difficulty)
available_options = ["請選擇..."] + COLOR_LIST  # 讓初始狀態乾淨

for i in range(st.session_state.difficulty):
    with player_cols[i]:
        # 上方顯示目前選擇的顏色大圖標，未選則顯示問號
        current_val = st.session_state.player_sequence[i]
        display_emoji = current_val if current_val else "❓"
        st.markdown(f"<h1 style='text-align: center; margin-bottom: 10px;'>{display_emoji}</h1>", unsafe_allow_html=True)
        
        # 下方對應位置的下拉選擇器
        chosen = st.selectbox(
            label=f"位置 {i+1}",
            options=available_options,
            index=available_options.index(current_val) if current_val in available_options else 0,
            key=f"pos_{i}",
            label_visibility="collapsed"
        )
        
        # 將玩家選擇的內容即時更新回狀態中
        st.session_state.player_sequence[i] = chosen if chosen != "請選擇..." else None

st.write("")

# 【步驟 C】✅ 功能控制按鈕（功能保證百分之百正確）
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("✅ 確定檢查答案", type="primary", use_container_width=True, disabled=st.session_state.game_over):
        # 核心防呆：檢查是否還有位置沒選顏色
        if None in st.session_state.player_sequence:
            st.error("⚠️ 請確保所有位置都填上了顏色方塊，再點擊檢查！")
        else:
            current_order = list(st.session_state.player_sequence)
            
            # 核心邏輯：100% 精準比對位置與顏色完全一致的數量
            correct_count = sum(1 for p, s in zip(current_order, st.session_state.secret_sequence) if p == s)
            
            # 將比對結果寫入歷史紀錄
            st.session_state.history.append({
                "round": len(st.session_state.history) + 1,
                "sequence": current_order,
                "correct": correct_count
            })
            
            # 如果完全答對
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
    st.info("尚未提交任何答案，在上方選好顏色後點擊檢查吧！")
else:
    for record in reversed(st.session_state.history):
        emoji_line = " ".join(record["sequence"])
        st.markdown(f"""
        **第 {record["round"]} 回合**：  
        {emoji_line}  
        🎯 位置與顏色完全正確： `{record["correct"]}` / {st.session_state.difficulty} 個
        """)
