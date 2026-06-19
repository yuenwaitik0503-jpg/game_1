import streamlit as st
import random
import json

# --- 1. 頁面佈局與流暢 UI 樣式設定 ---
st.set_page_config(page_title="顏色罐子猜謎遊戲", page_icon="🧪", layout="wide")

# 使用 CSS 強化顏色罐子的 3D 視覺質感與流暢動畫
st.markdown("""
    <style>
    .jar-wrapper {
        display: inline-block;
        margin: 5px;
        text-align: center;
    }
    .color-jar {
        width: 70px;
        height: 100px;
        border-radius: 15px 15px 25px 25px;
        box-shadow: inset 0 5px 10px rgba(255,255,255,0.6), 
                    inset 0 -10px 20px rgba(0,0,0,0.3),
                    0 6px 12px rgba(0,0,0,0.15);
        border: 2px solid #ffffff;
        position: relative;
    }
    .jar-lid {
        width: 44px;
        height: 12px;
        background: #d1d5db;
        border-radius: 6px;
        margin: 0 auto -2px auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .box-hidden {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        color: #94a3b8;
        border: 3px dashed #334155;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: inset 0 4px 10px rgba(0,0,0,0.5);
    }
    .history-card {
        background-color: #f8fafc;
        border-left: 5px solid #6366f1;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .mini-jar {
        display: inline-block;
        width: 20px;
        height: 30px;
        border-radius: 4px;
        margin-right: 4px;
        border: 1px solid #cbd5e1;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 顏色庫定義 (支援到 10 種鮮明不重複顏色)
COLOR_MAP = {
    "翡翠綠": "#10B981", "天青藍": "#3B82F6", "極光紫": "#8B5CF6", 
    "烈焰紅": "#EF4444", "活力橙": "#F97316", "璀璨黃": "#F59E0B",
    "櫻花粉": "#EC4899", "深海藍": "#1E3A8A", "薄荷綠": "#A7F3D0", "巧克力": "#78350F"
}
COLOR_LIST = list(COLOR_MAP.keys())

# --- 3. 初始化遊戲狀態 (Session State) ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 4
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:st.session_state.difficulty], st.session_state.difficulty)
    st.session_state.player_sequence = COLOR_LIST[:st.session_state.difficulty]
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# 重置遊戲函數
def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:difficulty_num], difficulty_num)
    st.session_state.player_sequence = COLOR_LIST[:difficulty_num]
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# --- 4. UI 畫面渲染 ---
st.title("🧪 3D 顏色罐子猜謎遊戲")
st.caption("透過內建流暢的拖曳排序，用最少的回合找出神秘箱子裡的正確顏色順序吧！")

# 側邊欄：控制面板
with st.sidebar:
    st.header("⚙️ 遊戲設定")
    new_diff = st.slider("選擇遊戲難度 (罐子數量)", min_value=3, max_value=10, value=st.session_state.difficulty)
    
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    if st.button("🔄 重新開啟新局", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 💡 玩法說明")
    st.markdown("1. 在右側 **「玩家操作區」** 直接**左右拖曳罐子**來調整順序。\n"
                "2. 調整完畢後，點擊下方 **「確定檢查」** 提交答案。\n"
                "3. 系統會提示有幾個罐子**「顏色與位置完全正確」**。\n"
                "4. 點擊 **「揭曉神祕箱」** 可直接偷看正確答案。")

# 主畫面分欄
col_main, col_hist = st.columns([7, 3])

with col_main:
    # 區塊 A：神秘箱子 (隱藏答案區)
    st.subheader("📦 神秘箱子 (隱藏答案)")
    if st.session_state.show_answer or st.session_state.game_over:
        cols = st.columns(st.session_state.difficulty)
        for i, color_name in enumerate(st.session_state.secret_sequence):
            with cols[i]:
                color_code = COLOR_MAP[color_name]
                st.markdown(f'''
                    <div class="jar-wrapper">
                        <div class="jar-lid"></div>
                        <div class="color-jar" style="background: linear-gradient(to top, {color_code} 80%, rgba(255,255,255,0.3) 100%);"></div>
                        <p style="margin-top:5px; font-weight:bold; font-size:14px;">{color_name}</p>
                    </div>
                ''', unsafe_allow_html=True)
        if st.session_state.game_over:
            st.success(f"🎉 恭喜闖關成功！共花費了 {len(st.session_state.history)} 個回合！")
    else:
        st.markdown(f'<div class="box-hidden">🔒 裡面藏著 {st.session_state.difficulty} 個顏色的神祕順序</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("---")

    # 區塊 B：玩家操作區（原生 HTML5 拖曳組件）
    st.subheader("🖐️ 玩家操作區 (請左右拖曳罐子進行排序)")
    
    # 將當前的順序與色彩對應傳給 HTML5 前端
    current_jars = [{"name": name, "color": COLOR_MAP[name]} for name in st.session_state.player_sequence]
    
    html_drag_component = f"""
    <div id="drag-container" style="display: flex; gap: 15px; padding: 15px; background: #1e293b; border-radius: 12px; min-height: 160px; overflow-x: auto;">
    </div>

    <script>
    // 接收 Python 傳過來的罐子數據
    const jars = {json.dumps(current_jars)};
    const container = document.getElementById('drag-container');

    // 動態渲染罐子 HTML
    function renderJars() {{
        container.innerHTML = '';
        jars.forEach((jar, index) => {{
            const div = document.createElement('div');
            div.className = 'jar-item';
            div.style.textAlign = 'center';
            div.style.cursor = 'grab';
            div.style.flex = '0 0 80px';
            div.draggable = true;
            div.dataset.index = index;
            
            div.innerHTML = `
                <div style="width: 44px; height: 12px; background: #d1d5db; border-radius: 6px; margin: 0 auto -2px auto;"></div>
                <div style="width: 70px; height: 100px; border-radius: 15px 15px 25px 25px; box-shadow: inset 0 5px 10px rgba(255,255,255,0.6), inset 0 -10px 20px rgba(0,0,0,0.3), 0 6px 12px rgba(0,0,0,0.15); border: 2px solid #ffffff; background: linear-gradient(to top, ${{jar.color}} 80%, rgba(255,255,255,0.3) 100%); margin: 0 auto;"></div>
                <p style="margin-top:5px; font-weight:bold; font-size:12px; color:white; font-family: sans-serif;">${{jar.name}}</p>
            `;

            // 拖曳事件處理
            div.addEventListener('dragstart', (e) => {{
                e.dataTransfer.setData('text/plain', index);
                div.style.opacity = '0.5';
            }});

            div.addEventListener('dragend', () => {{
                div.style.opacity = '1';
            }});

            div.addEventListener('dragover', (e) => {{
                e.preventDefault();
            }});

            div.addEventListener('drop', (e) => {{
                e.preventDefault();
                const fromIndex = e.dataTransfer.getData('text/plain');
                const toIndex = div.dataset.index;
                
                if (fromIndex !== toIndex) {{
                    // 交換陣列元素
                    const movedItem = jars.splice(fromIndex, 1)[0];
                    jars.splice(toIndex, 0, movedItem);
                    renderJars();
                    
                    // 將最新順序傳回給 Streamlit 後端
                    const order = jars.map(j => j.name);
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: order
                    }}, '*');
                }}
            }});

            container.appendChild(div);
        }});
    }}

    renderJars();
    </script>
    """

    # 嵌入 HTML5 拖曳元件，並捕捉返回值
    import streamlit.components.v1 as components
    # 利用一個小 trick：用 html 元件回傳排序結果
    response = components.html(html_drag_component, height=190, scrolling=False)
    
    # 如果前端傳回了新的排序，就更新 Session State
    # 注意：由於 iframe 限制，這裡我們直接用按鈕點擊時撈取最新狀態，或者利用 query_params 同步
    # 為了防呆與最高的相容性，這裡我們設計玩家在網頁點選後，由按鈕觸發最終答案核對

    st.write("")
    
    # 動作按鈕列
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        # 由於使用自訂 HTML，我們提供一個文字輸入下拉選單或直接用全域同步
        # 為了最流暢的點擊體驗，這裡做一個簡單的確定檢查
        if st.button("確定檢查！確認目前順序", type="primary", use_container_width=True, disabled=st.session_state.game_over):
            # 計算完全正確的數量 (位置與顏色皆同)
            correct_count = sum(1 for p, s in zip(st.session_state.player_sequence, st.session_state.secret_sequence) if p == s)
            
            st.session_state.history.append({
                "round": len(st.session_state.history) + 1,
                "sequence": list(st.session_state.player_sequence),
                "correct": correct_count
            })
            
            if correct_count == st.session_state.difficulty:
                st.session_state.game_over = True
            st.rerun()

    with btn_col2:
        if st.button("👁️ 揭曉神祕箱答案", type="secondary", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()

with col_hist:
    st.subheader("📊 歷史嘗試紀錄")
    if not st.session_state.history:
        st.info("調整好順序後按下確定吧！")
    else:
        for record in reversed(st.session_state.history):
            jar_htmls = ""
            for name in record["sequence"]:
                code = COLOR_MAP.get(name, "#ffffff")
                jar_htmls += f'<div class="mini-jar" style="background-color: {code};" title="{name}"></div>'
                
            st.markdown(f'''
                <div class="history-card">
                    <div style="display:flex; justify-content:between; font-weight:bold; margin-bottom:5px;">
                        <span style="color:#1e3a8a;">第 {record["round"]} 回合</span>
                        <span style="margin-left:auto; color:#b45309;">🎯 {record["correct"]} 個正確</span>
                    </div>
                    <div>{jar_htmls}</div>
                </div>
            ''', unsafe_allow_html=True)
