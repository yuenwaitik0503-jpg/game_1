import streamlit as st
import random
from streamlit_sortables import sort_items

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字排序謎題", layout="centered")

# --- 🎯 終極 CSS 強制覆蓋：徹底拔除這個套件的預設紅色，改成內建主題灰色 🎯 ---
st.markdown("""
    <style>
    /* 強制將拖曳方塊的預設紅色背景改成優雅的深灰色，並去除任何殘留顏色 */
    div[data-sortable-id] div, 
    .st-emotion-cache-1gh7w33, 
    [class*="sortable-item"] {
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
    </style>
""", unsafe_allow_html=True)

# --- 2. 核心狀態安全初始化（徹底阻絕舊版 HTML 顏色資料的快取殘留） ---
if "difficulty" not in st.session_state:
    st.session_state.difficulty = 5

# 如果發現舊資料裡帶有 HTML 標籤（例如含有 <div ），一律強制重置清空
if "player_sequence" in st.session_state and any("<div" in str(x) for x in st.session_state.player_sequence):
    del st.session_state["secret_sequence"]
    del st.session_state["player_sequence"]
    del st.session_state["history"]

if "secret_sequence" not in st.session_state:
    base_numbers = [str(i) for i in range(1, st.session_state.difficulty + 1)]
    st.session_state.secret_sequence = random.sample(base_numbers, st.session_state.difficulty)

if "player_sequence" not in st.session_state:
    # 這裡確保只有最純粹、乾淨的 ['1', '2', '3'...] 獨立數字字串
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
        
    # 防誤觸設計：利用大間隔將重開按鈕徹底隔離在最下方
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
st.write("請直接用滑鼠「左右拖曳」下方的數字卡片。調整完後，請使用左側設定區的按鈕檢查答案！")
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

# 【步驟 B】🖐️ 玩家操作區（滑鼠左右拖曳排序）
st.subheader("🖐️ 玩家操作區")
st.caption("👇 請直接用滑鼠點住數字「左右拖拉」調換順序：")

# 這裡丟進去元件的只有最乾淨的 ['1', '2', '3'...]
drag_items = list(st.session_state.player_sequence)

# 呼叫你原本就有安裝的橫向拖曳組件，並加上動態 Key 確保每次提交能精準刷新狀態
sorted_items = sort_items(
    drag_items, 
    direction="horizontal", 
    key=f"clean_drag_v9_{len(st.session_state.history)}_{st.session_state.difficulty}"
)

# 當玩家完成拖曳，即時更新最新數字序列
if sorted_items:
    st.session_state.player_sequence = [str(item).strip() for item in sorted_items]

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
        # 歷史紀錄採用 [1] [2] [3] 的純數字方框外觀
        history_display = " ".join([f"[{num}]" for num in record["sequence"]])
        
        st.markdown(f"""
        **第 {record["round"]} 回合**：  
        <span style='font-size: 22px; letter-spacing: 8px; font-family: monospace; color: #2196F3;'>{history_display}</span>  
        🎯 位置完全正確： `{record["correct"]}` / {st.session_state.difficulty} 個
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 15px; border-bottom: 1px dashed #cccccc;'></div>", unsafe_allow_html=True)
