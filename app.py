import streamlit as st
import random

# --- 1. 遊戲基礎設定 ---
st.set_page_config(page_title="數字排序謎題", layout="centered")

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
st.write("利用下方的操作區滑桿，直接左右拉動來調整當前數字的排列順序！")
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

# 【步驟 B】🖐️ 玩家操作區（純內建原生，絕無紅色、最聽話的滑動排序）
st.subheader("🖐️ 玩家操作區")
st.caption("🔍 當前順序如下，只有最純粹的獨立數字：")

# 1. 用超大字體、極簡美觀地呈現當前玩家排出來的獨立數字
current_display = " ".join([f"({num})" for num in st.session_state.player_sequence])
st.markdown(f"<h2 style='text-align: center; color: #2196F3; letter-spacing: 15px;'>{current_display}</h2>", unsafe_allow_html=True)

st.write("")
st.caption("👇 拉動各個位置的滑桿，即可自由調整該位置要擺放哪個數字：")

# 2. 為每個位置生成一個專屬的數字調整滑桿，左右拉動超流暢
cols = st.columns(st.session_state.difficulty)
new_sequence = list(st.session_state.player_sequence)

for idx in range(st.session_state.difficulty):
    with cols[idx]:
        st.markdown(f"<p style='text-align: center; margin-bottom: -10px;'>第 {idx+1} 位</p>", unsafe_allow_html=True)
        # 取得目前這個位置的數字
        current_val = st.session_state.player_sequence[idx]
        
        # 滑桿選項：可選範圍就是 1 ~ 難度上限的數字
        # 拉動滑桿，數字順序立刻聽話改變
        selected_num = st.select_slider(
            label=f"slider_{idx}",
            options=[str(i) for i in range(1, st.session_state.difficulty + 1)],
            value=current_val,
            label_visibility="collapsed",
            key=f"pos_slider_{idx}_r{len(st.session_state.history)}"
        )
        new_sequence[idx] = selected_num

# 只要玩家拉動任何一個滑桿，立刻更新排列
if new_sequence != st.session_state.player_sequence:
    st.session_state.player_sequence = new_sequence
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
        <span style='font-size: 22px; letter-spacing: 8px; font-family: monospace; color: #9E9E9E;'>{history_display}</span>  
        🎯 位置完全正確： `{record["correct"]}` / {st.session_state.difficulty} 個
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 15px; border-bottom: 1px dashed #cccccc;'></div>", unsafe_allow_html=True)
