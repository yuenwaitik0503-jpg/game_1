import streamlit as st
import random
from streamlit_drag_drop_sortable import drag_drop_sortable

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字排序謎題", layout="centered")

# --- 2. 核心狀態安全初始化 ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 5  # 預設難度
    base_numbers = [str(i) for i in range(1, st.session_state.difficulty + 1)]
    # 隨機答案
    st.session_state.secret_sequence = random.sample(base_numbers, st.session_state.difficulty)
    # 玩家當前排列
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
        
    # 防誤觸設計：利用大間隔將重開按鈕隔離在最下方
    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.caption("⚠️ 危險區域")
    if st.button("🔄 重新開啟新局", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()

# --- 4. 主畫面主要邏輯區 ---
st.title("🔢 數字排序謎題")
st.write("請直接用滑鼠「按住並左右拖曳」下方的數字卡片來調整順序，完成後點擊左側的檢查按鈕！")
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
    st.warning(f"內部數字順序已鎖定：{locks} （請在下方排列完成後檢查）")

st.markdown("---")

# 【步驟 B】🖐️ 玩家操作區（重新迎回最流暢的原生拖曳引擎）
st.subheader("🖐️ 玩家操作區")
st.caption("🔍 當前排列如下，請用滑鼠按住數字卡片直接進行拖曳：")

# 視覺保護 CSS：確保拖曳元件長得乾淨大氣
st.markdown("""
    <style>
    /* 調整元件樣式，確保只有純數字與乾淨的主題灰色背景，絕無紅色跑版 */
    div[data-sortable-id] div, div[data-sortable-id] li {
        background-color: transparent !important;
        background: transparent !important;
    }
    div[data-sortable-id] li button {
        background-color: transparent !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# 這裡塞入的全部都是純數字，不帶任何英文或代碼
drag_items = [f" {num} " for num in st.session_state.player_sequence]

# 調用最乾淨、最穩定的橫向拖曳排序元件
sorted_items = drag_drop_sortable(
    items=drag_items,
    direction="horizontal",
    key=f"drag_sort_v3_{len(st.session_state.history)}_{st.session_state.difficulty}"
)

# 當玩家完成拖曳，即時更新最新數字序列
if sorted_items:
    st.session_state.player_sequence = [item.replace(" ", "").strip() for item in sorted_items]

st.write("")
st.write("")
st.markdown("---")

# 【步驟 C】📊 歷史紀錄區（直接在操作區下方，展示純數字對比）
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
