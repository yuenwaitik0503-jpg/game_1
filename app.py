import streamlit as st
import random

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字排序謎題", layout="centered")

# --- 2. 核心狀態安全初始化（確保所有變數在最開頭就 100% 存在） ---
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

if "selected_idx" not in st.session_state:
    st.session_state.selected_idx = None


# --- 3. 重置遊戲安全函數（確保每一次重開或換難度，所有變數都同步重置） ---
def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    base_numbers = [str(i) for i in range(1, difficulty_num + 1)]
    st.session_state.secret_sequence = random.sample(base_numbers, difficulty_num)
    st.session_state.player_sequence = list(st.session_state.secret_sequence)
    random.shuffle(st.session_state.player_sequence)
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False
    st.session_state.selected_idx = None  # 徹底重置暫存索引，防崩潰


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
        st.session_state.selected_idx = None  # 檢查後清空選擇狀態
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

# 【步驟 B】🖐️ 玩家操作區（點擊對調引擎，100% 告別紅色）
st.subheader("🖐️ 玩家操作區")

# 視覺提示：告訴玩家現在點到哪了
if st.session_state.selected_idx is not None:
    # 安全保護，防止索引越界
    if st.session_state.selected_idx < len(st.session_state.player_sequence):
        current_selected_num = st.session_state.player_sequence[st.session_state.selected_idx]
        st.info(f"💡 正在移動數字 `{current_selected_num}`，請點擊另一個數字來與它對調位置...")
    else:
        st.session_state.selected_idx = None
else:
    st.caption("👇 請用滑鼠「點擊」想要調換位置的任意兩個數字卡片：")

# 產生純淨的數字顯示清單（去文字、去顏色）
pill_options = [f" {num} " for num in st.session_state.player_sequence]

# 使用原生 st.pills，它會完美適應你的 Streamlit 主題色（灰色/深色），絕無紅色
selected_pill = st.pills(
    label="當前排列順序",
    options=pill_options,
    label_visibility="collapsed",
    key="native_num_pills_v3"
)

# 處理對調邏輯
if selected_pill:
    clicked_idx = pill_options.index(selected_pill)
    
    if st.session_state.selected_idx is None:
        # 第一次點擊：記錄選中的第一個數字位置
        st.session_state.selected_idx = clicked_idx
        st.rerun()
    else:
        # 第二次點擊：執行對調
        idx1 = st.session_state.selected_idx
        idx2 = clicked_idx
        
        # 只有當點擊不同卡片時才對調
        if idx1 != idx2 and idx1 < len(st.session_state.player_sequence) and idx2 < len(st.session_state.player_sequence):
            st.session_state.player_sequence[idx1], st.session_state.player_sequence[idx2] = (
                st.session_state.player_sequence[idx2],
                st.session_state.player_sequence[idx1]
            )
        
        # 對調完後清除暫存，準備下一次對調
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
