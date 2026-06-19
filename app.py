import streamlit as st
import random

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字排序謎題", layout="centered")

# --- 2. 初始化遊戲狀態 ---
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
    # 用於紀錄點擊對調的暫存索引
    st.session_state.selected_idx = None

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
    st.session_state.selected_idx = None

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
st.write("請使用下方的數字卡片，點擊任意兩個數字即可直接交換它們的位置！")
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

# 【步驟 B】🖐️ 玩家操作區（告別紅色、最流暢穩定的對調引擎）
st.subheader("🖐️ 玩家操作區")

if st.session_state.selected_idx is not None:
    st.info(f"💡 正在移動數字 `{st.session_state.player_sequence[st.session_state.selected_idx]}`，請點擊另一個數字來與它對調位置...")
else:
    st.caption("👇 請用滑鼠「點擊」想要調換位置的任意兩個數字卡片：")

# 將當前的數組轉換為帶有位置序號的獨立顯示文字，徹底與紅色分離
pill_options = [f" {num} " for num in st.session_state.player_sequence]

# 使用原生 st.pills，它渲染出來會是完美的深色/灰色主題卡片，絕不帶任何多餘文字與紅色
selected_pill = st.pills(
    label="當前排列順序",
    options=pill_options,
    label_visibility="collapsed",
    key="native_num_pills"
)

# 對調的核心驅動邏輯
if selected_pill:
    # 找出玩家點擊的是第幾個位置的卡片
    clicked_idx = pill_options.index(selected_pill)
    
    if st.session_state.selected_idx is None:
        # 如果是第一次點擊，紀錄起點位置
        st.session_state.selected_idx = clicked_idx
        st.rerun()
    else:
        # 如果是第二次點擊，將兩個位置的數字對調
        idx1 = st.session_state.selected_idx
        idx2 = clicked_idx
        
        # 位置對調
        st.session_state.player_sequence[idx1], st.session_state.player_sequence[idx2] = (
            st.session_state.player_sequence[idx2],
            st.session_state.player_sequence[idx1]
        )
        # 對調完成後清除狀態
        st.session_state.selected_idx = None
        st.rerun()

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
