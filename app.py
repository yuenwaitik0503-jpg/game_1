import streamlit as st
import random
import streamlit.components.v1 as components
import json

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

    if st.button("👁️ 揭曉神秘箱答案", type="secondary", use_container_width=True):
        st.session_state.show_answer = True
        st.rerun()
        
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
st.write("請直接用滑鼠「左右拖曳」下方的數字卡片來調整順序，完成後點擊左側的檢查按鈕！")
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

# 【步驟 B】🖐️ 玩家操作區（HTML5 原生無損拖曳引擎，徹底除錯、去紅）
st.subheader("🖐️ 玩家操作區")
st.caption("👇 請直接用滑鼠點住數字「左右拖拉」調換順序：")

# 準備傳遞給前端 JavaScript 的當前數字列表
items_json = json.dumps(st.session_state.player_sequence)

# 嵌入高效能 HTML5 拖拽組件
# 這段代碼自帶乾淨的極簡灰色卡片樣式，且絕對不重複、不走位
html_code = f"""
<div id="drag-container" style="display: flex; gap: 12px; padding: 10px 0; font-family: sans-serif; user-select: none;"></div>

<script>
// 從 Streamlit 獲取當前的純數字列表
const items = {items_json};
const container = document.getElementById('drag-container');

// 動態渲染極簡數字卡片
items.forEach((num, index) => {{
    const el = document.createElement('div');
    el.innerText = num;
    el.draggable = true;
    el.dataset.index = index;
    
    // 設定高質感、防紅色的極簡外觀
    Object.assign(el.style, {{
        backgroundColor: '#2b303c',
        color: '#ffffff',
        border: '1px solid #434956',
        borderRadius: '8px',
        padding: '14px 28px',
        fontSize: '24px',
        fontWeight: 'bold',
        cursor: 'grab',
        textAlign: 'center',
        minWidth: '25px',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
    }});
    
    // 監聽 HTML5 拖拽事件
    el.addEventListener('dragstart', (e) => {{
        e.dataTransfer.setData('text/plain', index);
        el.style.opacity = '0.5';
    }});
    
    el.addEventListener('dragend', () => {{
        el.style.opacity = '1';
    }});
    
    el.addEventListener('dragover', (e) => {{
        e.preventDefault();
    }});
    
    el.addEventListener('drop', (e) => {{
        e.preventDefault();
        const fromIndex = parseInt(e.dataTransfer.getData('text/plain'));
        const toIndex = index;
        
        if (fromIndex !== toIndex) {{
            // 在前端精準交換位置，絕對不會產生重複數字
            const updatedItems = [...items];
            const [movedItem] = updatedItems.splice(fromIndex, 1);
            updatedItems.splice(toIndex, 0, movedItem);
            
            // 將完美排好的新陣列一次性安全回傳給 Python
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: updatedItems
            }}, '*');
        }}
    }});
    
    container.appendChild(el);
}});
</script>
"""

# 用於即時捕捉網頁端傳回來的最新正確排序資料
# 利用 key 快取機制將變數完全隔離開來，防範任何異步走位錯誤
response = components.html(html_code, height=90, key=f"html5_drag_engine_v1_{len(st.session_state.history)}")

# 當前端傳回完美的新陣列時，覆寫系統序列
if response is not None:
    st.session_state.player_sequence = [str(x) for x in response]
    st.rerun()

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
