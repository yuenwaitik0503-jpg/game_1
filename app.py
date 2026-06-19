import streamlit as st
import random
from streamlit_sortables import sort_items

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字卡片排序謎題", layout="centered")

# --- 🎯 獨家 CSS 強制覆蓋：徹底拿掉紅色，改成質感的獨立數字卡片 🎯 ---
st.markdown("""
    <style>
    /* 強制將原本的紅色背景改為優雅的深灰色，並去掉多餘文字污染 */
    div[data-sortable-id] div, 
    [class*="sortable-item"], 
    .st-emotion-cache-1gh7w33 {
        background-color: #2b303c !important;
        background: #2b303c !important;
        color: #ffffff !important;
        border: 1px solid #434956 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }
    
    /* 縮小區塊頂部的間距，讓操作區與歷史區整體升高 */
    .stMarkdown, .stVerticalBlock {
        margin-top: 0px !important;
        padding-top: 2px !important;
    }
    hr {
        margin-top: 15px !important;
        margin-bottom: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 初始化遊戲狀態 ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 5  # 預設難度：5 個數字
    base_numbers = [str(i) for i in range(1, st.session_state.difficulty + 1)]
    st.session_state.secret_sequence = random.sample(base_numbers, st.session_state.difficulty)
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    random.shuffle(st.session_state.player_sequence)
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# 重置遊戲安全函數
def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    base_numbers = [str(i) for i in range(1, difficulty_num + 1)]
    st.session_state.secret_sequence = random.sample(base_numbers, difficulty_num)
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    random.shuffle(st.session_state.player_sequence)
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# --- 3. 左邊【遊戲設定區域】（側邊欄） ---
with st.sidebar:
    st.header("⚙️ 遊戲設定")
    new_diff = st.slider("選擇數字數量 (難度)", min_value=3, max_value=10, value=st.session_state.difficulty)
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    # ⭐ 重新開啟新局直接放回難度滑桿下方
    if st.button("🔄 重新開啟新局", use_container_width=True):
        reset_game(st.session_state.difficulty)
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

# --- 4. 主畫面主要邏輯區 ---
# 拔掉了最上方的大標題和說明文字，直接切入核心操作畫面

# 【步驟 A】📦 神秘箱子區
st.subheader("📦 神秘箱子")
if st.session_state.show_answer or st.session_state.game_over:
    secret_display = " ".join([f"[{num}]" for num in st.session_state.secret_sequence])
    st.markdown(f"<h1 style='letter-spacing: 10px; text-align: center; color: #4CAF50; margin: 5px 0;'>{secret_display}</h1>", unsafe_allow_html=True)
    if st.session_state.game_over:
        st.success(f"🎉 恭喜闖關成功！共花了 {len(st.session_state.history)} 回合！")
else:
    locks = " ".join(["🔒"] * st.session_state.difficulty)
    st.warning(f"內部數字順序已鎖定：{locks}")

st.markdown("---")

# 【步驟 B】🖐️ 玩家操作區（整體往上升高）
st.subheader("🖐️ 玩家操作區")

# 確保每一次讀取，都進行一次嚴格的去重與乾淨化防禦
drag_items = list(dict.fromkeys([str(x).strip() for x in st.session_state.player_sequence]))

# 呼叫橫向拖曳組件
sorted_items = sort_items(
    drag_items, 
    direction="horizontal", 
    key=f"fixed_num_drag_v13_{len(st.session_state.history)}_{st.session_state.difficulty}_{len(drag_items)}"
)

# 當玩家拖曳時，精準存回系統
if sorted_items:
    st.session_state.player_sequence = [str(item).strip() for item in sorted_items]

st.markdown("---")

# 【步驟 C】📊 歷史紀錄區（也同步升高，方便直接對齊操作區）
st.subheader("📊 歷史比對紀錄")

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
        st.markdown("<div style='margin-bottom: 10px; border-bottom: 1px dashed #cccccc;'></div>", unsafe_allow_html=True)
