import streamlit as st
import random

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="顏色排序謎題", layout="centered")

# --- 2. 顏色資料庫定義 ---
# 定義 10 種顏色與其對應的 Emoji 方塊，方便玩家視覺辨識，同時不依賴複雜 CSS
COLOR_DICTS = {
    "🟥 紅色方塊": "🟥",
    "🟩 綠色方塊": "🟩",
    "🟦 藍色方塊": "🟦",
    "🟪 紫色方塊": "🟪",
    "🟧 橘色方塊": "🟧",
    "🟨 黃色方塊": "🟨",
    "🟫 棕色方塊": "🟫",
    "⬛ 黑色方塊": "⬛",
    "⬜ 白色方塊": "⬜",
    "🔵 藍色圓形": "🔵"
}
COLOR_LIST = list(COLOR_DICTS.keys())

# --- 3. 初始化遊戲狀態 (Session State) ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 4  # 預設難度：4 個方塊
    # 從顏色庫中隨機挑選不重複的顏色作為答案
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:st.session_state.difficulty], st.session_state.difficulty)
    # 玩家目前的排列順序（預設跟初始一樣，讓玩家去調整）
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    # 亂序打亂玩家的初始方塊，讓他們動手排
    random.shuffle(st.session_state.player_sequence)
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# 重置遊戲函數
def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:difficulty_num], difficulty_num)
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    random.shuffle(st.session_state.player_sequence)
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# --- 4. 遊戲控制側邊欄 ---
with st.sidebar:
    st.header("⚙️ 遊戲控制")
    new_diff = st.slider("選擇方塊數量 (難度)", min_value=3, max_value=8, value=st.session_state.difficulty)
    
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    if st.button("🔄 開始新遊戲", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()

# --- 5. 主畫面主要邏輯區 ---
st.title("🧪 顏色方塊排序谜題")
st.write("請調整下方的顏色方塊順序，讓它與箱子內隱藏的正確答案完全一致！")
st.markdown("---")

# 【步驟 A】神秘箱子區（顯示隱藏答案或鎖定狀態）
st.subheader("📦 神秘箱子")
if st.session_state.show_answer or st.session_state.game_over:
    # 用橫向欄位顯示正確答案的 Emoji
    secret_cols = st.columns(st.session_state.difficulty)
    for i, color in enumerate(st.session_state.secret_sequence):
        with secret_cols[i]:
            st.info(color)
    if st.session_state.game_over:
        st.success(f"🎉 恭喜闖關成功！共花了 {len(st.session_state.history)} 回合！")
else:
    st.warning(f"🔒 箱子內藏有 {st.session_state.difficulty} 個方塊的正確順序（已鎖定）")

st.markdown("---")

# 【步驟 B】玩家操作區（確保操作絕對流暢、不影響按鈕）
st.subheader("🖐️ 玩家操作區")
st.write("👉 **拖動或點擊下方的顏色標籤來調整順序**（越左邊代表第 1 個）：")

# 使用 Streamlit 最穩定的多選元件作為排序器。玩家可以隨意點叉叉移除、或點擊選單重新排列順序。
user_sort = st.multiselect(
    label="當前排列順序 (可自由增刪排序)",
    options=COLOR_LIST[:st.session_state.difficulty],
    default=st.session_state.player_sequence,
    label_visibility="collapsed"
)

# 即時將玩家調整的最新順序存回系統
if user_sort:
    st.session_state.player_sequence = user_sort

st.write("")

# 【步驟 C】功能控制按鈕（與方塊完全分離，回復正常功能）
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    # 確定檢查按鈕
    if st.button("✅ 確定檢查答案", type="primary", use_container_width=True, disabled=st.session_state.game_over):
        # 檢查玩家選的數量是否跟難度一樣
        if len(st.session_state.player_sequence) != st.session_state.difficulty:
            st.error(f"請確保您選滿了 {st.session_state.difficulty} 個方塊再進行檢查！")
        else:
            current_order = list(st.session_state.player_sequence)
            # 100% 精準比對位置與顏色完全正確的數量
            correct_count = sum(1 for p, s in zip(current_order, st.session_state.secret_sequence) if p == s)
            
            # 將結果記錄到歷史紀錄
            st.session_state.history.append({
                "round": len(st.session_state.history) + 1,
                "sequence": current_order,
                "correct": correct_count
            })
            
            # 如果全對則結束遊戲
            if correct_count == st.session_state.difficulty:
                st.session_state.game_over = True
            st.rerun()

with btn_col2:
    # 揭曉答案按鈕
    if st.button("👁️ 揭曉神秘箱答案", type="secondary", use_container_width=True):
        st.session_state.show_answer = True
        st.rerun()

st.markdown("---")

# 【步驟 D】右側歷史紀錄區
st.subheader("📊 歷史比對紀錄")
if not st.session_state.history:
    st.info("尚未提交任何答案，開始排列方塊吧！")
else:
    for record in reversed(st.session_state.history):
        # 將玩家當時提交的方塊序列轉換成一整串 Emoji 字串
        emoji_line = " ".join([COLOR_DICTS[name] for name in record["sequence"]])
        
        st.markdown(f"""
        **第 {record["round"]} 回合**：  
        {emoji_line}  
        🎯 位置與顏色完全正確： `{record["correct"]}` 個
        """)
