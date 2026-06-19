import streamlit as st
import random
from streamlit_sortables import sort_items

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字卡片排序謎題", layout="centered")

# --- 2. 初始化遊戲狀態 ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 4  # 預設 4 個數字
    # 根據難度生成數字清單（例如 4 號難度就是 [1, 2, 3, 4]）
    base_numbers = [str(i) for i in range(1, st.session_state.difficulty + 1)]
    # 隨機打亂作為正確答案
    st.session_state.secret_sequence = random.sample(base_numbers, st.session_state.difficulty)
    # 玩家目前的排列順序（初始先打亂）
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
    new_diff = st.slider("選擇數字卡數量 (難度)", min_value=3, max_value=10, value=st.session_state.difficulty)
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    st.markdown("---")
    
    # 將確定檢查與揭曉答案按鈕移至左側
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
        
    # ⭐ 防誤觸設計：利用大間隔與分隔線將重開按鈕徹底孤立在最下方
    st.write("")
    st.write("")
    st.write("")
    st.markdown("---")
    st.caption("⚠️ 危險區域")
    if st.button("🔄 重新開啟新局", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()

# --- 4. 主畫面主要邏輯區 ---
st.title("🔢 數字卡片排序謎題")
st.write("請在操作區直接用滑鼠左右拖拉數字卡片。調整完後，請使用左側設定區的「確定檢查答案」按鈕！")
st.markdown("---")

# 【步驟 A】📦 神秘箱子區
st.subheader("📦 神秘箱子")
if st.session_state.show_answer or st.session_state.game_over:
    # 遊戲結束或揭曉答案時，用帶有質感的方框格式秀出正確的數字卡順序
    secret_display = " ".join([f"[{num}]" for num in st.session_state.secret_sequence])
    st.markdown(f"<h1 style='letter-spacing: 10px; text-align: center; color: #4CAF50;'>{secret_display}</h1>", unsafe_allow_html=True)
    if st.session_state.game_over:
        st.success(f"🎉 恭喜闖關成功！共花了 {len(st.session_state.history)} 回合！")
else:
    # 未揭曉時顯示鎖定狀態
    locks = " ".join(["🔒"] * st.session_state.difficulty)
    st.warning(f"內部數字順序已鎖定：{locks}")

st.markdown("---")

# 【步驟 B】🖐️ 玩家操作區（數字卡片滑動引擎）
st.subheader("🖐️ 玩家操作區")
st.caption("👇 請直接用滑鼠點住數字卡片「左右拖拉」來調換順序：")

# 確保拖曳內容格式正確
drag_items = [f" 卡片 {num} " for num in st.session_state.player_sequence]

# 呼叫橫向拖曳組件
sorted_items = sort_items(drag_items, direction="horizontal", key=f"num_drag_v1_{len(st.session_state.history)}_{st.session_state.difficulty}")

# 只要玩家一拖曳，立刻即時更新最新順序
if sorted_items:
    # 從 " 卡片 X " 中把純數字 X 提取出來
    st.session_state.player_sequence = [item.replace(" 卡片 ", "").strip() for item in sorted_items]

st.write("")
st.write("")
st.markdown("---")

# 【步驟 C】📊 歷史紀錄區（直接串接在操作區下方，完美對比）
st.subheader("📊 歷史比對紀錄")
st.caption("您可以直接比對當前操作區的順序與先前各回合的分別：")

if not st.session_state.history:
    st.info("尚未提交任何答案。在上方調整好數字卡順序後，點擊左側的「確定檢查答案」吧！")
else:
    # 用表格或清晰的列表由新到舊排下來
    for record in reversed(st.session_state.history):
        # 將該回合歷史排列美化為卡片外觀
        history_display = " ".join([f"[{num}]" for num in record["sequence"]])
        
        # 計算不對的位置提示（選填，方便玩家看差距）
        st.markdown(f"""
        **第 {record["round"]} 回合**：  
        <span style='font-size: 22px; letter-spacing: 5px; font-family: monospace; color: #2196F3;'>{history_display}</span>  
        🎯 位置完全正確： `{record["correct"]}` / {st.session_state.difficulty} 個
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 15px; border-bottom: 1px dashed #cccccc;'></div>", unsafe_allow_html=True)
