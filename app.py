import streamlit as st
import random
import pandas as pd

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字排序謎題", layout="centered")

# --- 🎯 終極 CSS 微調：把表格完全偽裝成「極簡圓角數字卡片」並徹底去紅 🎯 ---
st.markdown("""
    <style>
    /* 隱藏資料編輯器多餘的工具列和序號 */
    [data-testid="stDataEditorToolbar"] { display: none !important; }
    
    /* 讓數字卡片外觀變大、變粗、圓角，呈現高質感的灰色，絕無紅色 */
    .stDataEditor div, [data-testid="stDataEditor"] {
        font-size: 22px !important;
        font-weight: bold !important;
        background-color: transparent !important;
    }
    
    /* 微調間距，讓操作感更像在拉獨立卡片 */
    .stDataFrame {
        margin: 0 auto !important;
        max-width: 600px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 核心狀態安全初始化 ---
if "difficulty" not in st.session_state:
    st.session_state.difficulty = 5

if "secret_sequence" not in st.session_state:
    base_numbers = [str(i) for i in range(1, st.session_state.difficulty + 1)]
    st.session_state.secret_sequence = random.sample(base_numbers, st.session_state.difficulty)

if "player_sequence" not in st.session_state:
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    random.shuffle(st.session_state.player_sequence)

if "history" not in st.session_state:
    st.session_state.history = []

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# --- 3. 重置遊戲安全函數 ---
def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    base_numbers = [str(i) for i in range(1, difficulty_num + 1)]
    st.session_state.secret_sequence = random.sample(base_numbers, difficulty_num)
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    random.shuffle(st.session_state.player_sequence)
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False


# --- 4. 左邊【遊戲設定區域】（側邊欄） ---
with st.sidebar:
    st.header("⚙️ 遊戲設定")
    new_diff = st.slider("選擇數字數量 (難度)", min_value=3, max_value=10, value=st.session_state.difficulty)
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    st.markdown("---")
    st.subheader("🎮 動作操作")
    
    # 按鈕 A：確定檢查答案
    if st.button("✅ 確定檢查答案", type="primary", use_container_width=True, disabled=st.session_state.game_over):
        current_order = list(st.session_state.player_sequence)
        correct_count = sum(1 for p, s in zip(current_order, st.session_state.secret_sequence) if p == s)
        
        st.session_state.history.append({
            "round": len(st.session_state.history) + 1,
            "sequence": current_order,
            "correct": correct_count
        })
        
        if correct_count == st.session_state.difficulty:
            st.session_state.game_over = True
        st.rerun()

    # 按鈕 B：揭曉神秘箱答案
    if st.button("👁️ 揭曉神秘箱答案", type="secondary", use_container_width=True):
        st.session_state.show_answer = True
        st.rerun()
        
    # 防誤觸設計：隔離重開按鈕在最下方
    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.caption("⚠️ 危險區域")
    if st.button("🔄 重新開啟新局", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()

# --- 5. 主畫面主要邏輯區 ---
st.title("🔢 數字排序謎題")
st.write("請直接用滑鼠「按住數字左側的 ⠿ 符號並上下拖曳」來調整數字順序，調整完點擊左側檢查答案！")
st.markdown("---")

# 【步驟 A】📦 神秘箱子區
st.subheader("📦 神秘箱子")
if st.session_state.show_answer or st.session_state.game_over:
    secret_display = " ".join([f"[{num}]" for num in st.session_state.secret_sequence])
    st.markdown(f"<h1 style='letter-spacing: 10px; text-align: center; color: #4CAF50;'>{secret_display}</h1>", unsafe_allow_html=True)
    if st.session_state.game_over:
        st.success(f"🎉 恭喜闖關成功！共花了 {len(st.session_state.history)} 回合！")
else:
    locks = " ".join(["🔒"] * st.session_state.difficulty)
    st.warning(f"內部數字順序已鎖定：{locks}")

st.markdown("---")

# 【步驟 B】🖐️ 玩家操作區（100% 聽話的官方原生拖曳卡片引擎）
st.subheader("🖐️ 玩家操作區")
st.caption("👇 用滑鼠按住數字左邊的 `⠿` 圖示即可直接「上下拖曳」調換位置，位置絕不亂跑：")

# 將當前陣列包裝成 Pandas DataFrame
df = pd.DataFrame({"當前數字排列": st.session_state.player_sequence})

# 調用官方專門設計用來排序和編輯的原生資料組件
# num_rows="fixed" 限制了行數，這意味著絕對不可能憑空多出、少掉或重複數字！
edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    disabled=["當前數字排列"], # 禁用手動打字修改，只允許滑鼠拖拽排序
    key=f"native_drag_engine_{len(st.session_state.history)}"
)

# 當玩家完成拖曳，精確、100% 無損地寫回系統陣列
if edited_df is not None:
    new_order = edited_df["當前數字排列"].tolist()
    if new_order != st.session_state.player_sequence:
        st.session_state.player_sequence = new_order

st.write("")
st.write("")
st.markdown("---")

# 【步驟 C】📊 歷史紀錄區
st.subheader("📊 歷史比對紀錄")
st.caption("您可以直接比對當前操作區的順序與先前各回合的分別：")

if not st.session_state.history:
    st.info("尚未提交任何答案。在上方調整好數字順序後，點擊左側的「確定檢查答案」吧！")
else:
    for record in reversed(st.session_state.history):
        history_display = " ".join([f"[{num}]" for num in record["sequence"]])
        
        st.markdown(f"""
        **第 {record["round"]} 回合**：  
        <span style='font-size: 22px; letter-spacing: 8px; font-family: monospace; color: #2196F3;'>{history_display}</span>  
        🎯 位置完全正確： `{record["correct"]}` / {st.session_state.difficulty} 個
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 15px; border-bottom: 1px dashed #cccccc;'></div>", unsafe_allow_html=True)
