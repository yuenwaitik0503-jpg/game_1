import streamlit as st
import random
from streamlit_sortables import sort_items

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字卡片排序謎題", layout="centered")

# --- 2. 初始化遊戲狀態 ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 5  # 預設難度：5 個數字
    # 建立純數字清單：['1', '2', '3', '4', '5']
    base_numbers = [str(i) for i in range(1, st.session_state.difficulty + 1)]
    # 隨機打亂作為神秘箱的正確答案
    st.session_state.secret_sequence = random.sample(base_numbers, st.session_state.difficulty)
    # 玩家目前的排列（初始先打亂）
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
        # 精準比對位置與數字完全正確的數量
        correct_count = sum(1 for p, s in zip(current_order, st.session_state.secret_sequence) if p == s)
        
        # 紀錄至歷史比對紀錄
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
        
    # 防誤觸設計：利用大間隔與分隔線將重開按鈕隔離在最下方
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
st.write("請在操作區直接用滑鼠左右拖拉數字。調整完後，請使用左側設定區的「確定檢查答案」按鈕！")
st.markdown("---")

# 【步驟 A】📦 神秘箱子區
st.subheader("📦 神秘箱子")
if st.session_state.show_answer or st.session_state.game_over:
    # 顯示正確的純數字順序
    secret_display = " ".join([f"[{num}]" for num in st.session_state.secret_sequence])
    st.markdown(f"<h1 style='letter-spacing: 10px; text-align: center; color: #4CAF50;'>{secret_display}</h1>", unsafe_allow_html=True)
    if st.session_state.game_over:
        st.success(f"🎉 恭喜闖關成功！共花了 {len(st.session_state.history)} 回合！")
else:
    # 未揭曉時顯示鎖定狀態
    locks = " ".join(["🔒"] * st.session_state.difficulty)
    st.warning(f"內部數字順序已鎖定：{locks}")

st.markdown("---")

# 【步驟 B】🖐️ 玩家操作區
st.subheader("🖐️ 玩家操作區")
st.caption("👇 請直接用滑鼠點住數字「左右拖拉」來調換順序：")

# ⭐ 核心改動：直接把純數字字串丟進去，不加任何“卡片”字眼
drag_items = list(st.session_state.player_sequence)

# 呼叫橫向拖曳組件
sorted_items = sort_items(drag_items, direction="horizontal", key=f"isolated_num_drag_{len(st.session_state.history)}_{st.session_state.difficulty}")

# 當玩家拖曳時，直接把最新的純數字順序存回系統
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
        # 歷史紀錄採用 [1] [2] [3] 的純數字方框
        history_display = " ".join([f"[{num}]" for num in record["sequence"]])
        
        st.markdown(f"""
        **第 {record["round"]} 回合**：  
        <span style='font-size: 22px; letter-spacing: 8px; font-family: monospace; color: #2196F3;'>{history_display}</span>  
        🎯 位置完全正確： `{record["correct"]}` / {st.session_state.difficulty} 個
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 15px; border-bottom: 1px dashed #cccccc;'></div>", unsafe_allow_html=True)
