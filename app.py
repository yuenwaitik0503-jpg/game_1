import streamlit as st
import random
import json

# --- 1. 頁面佈局與 iOS 玻璃風格核心樣式設定 ---
st.set_page_config(page_title="iOS 顏色罐子謎題", page_icon="🧪", layout="wide", initial_sidebar_state="collapsed")

# 核心 CSS：注入 iOS 系統風格與強大的毛玻璃特效
st.markdown("""
    <style>
    /* 全局背景：深色星空暗藍，最能襯托出 iOS 玻璃流光質感 */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1e2f 100%);
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* iOS 標題與副標題樣式 */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* iOS 擬真玻璃卡片基底 (Glassmorphism) */
    .ios-glass-card {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 24px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 20px;
    }
    
    /* 📦 神秘箱子：iOS 簡約暗黑卡片風格 */
    .box-hidden-ios {
        background: rgba(15, 23, 42, 0.6);
        border: 1px dashed rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 45px 20px;
        text-align: center;
        font-size: 20px;
        font-weight: 500;
        color: #94a3b8;
        letter-spacing: -0.3px;
        box-shadow: inset 0 4px 12px rgba(0,0,0,0.4);
    }
    
    /* 📊 iOS 歷史紀錄小卡 (細緻磨砂玻璃) */
    .ios-history-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px;
        border-radius: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .mini-jar-ios {
        display: inline-block;
        width: 16px;
        height: 24px;
        border-radius: 6px;
        margin-right: 5px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* 覆蓋 Streamlit 原生按鈕，改成 iOS 圓潤高質感膠囊按鈕 */
    .stButton>button {
        border-radius: 14px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        letter-spacing: -0.2px !important;
        transition: all 0.2s ease !important;
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

def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:difficulty_num], difficulty_num)
    st.session_state.player_sequence = COLOR_LIST[:difficulty_num]
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# --- 4. UI 畫面渲染 ---
st.title("🧪 顏色罐子謎題")
st.caption("👈 點擊左上角「▶」可展開 iPhone 風格控制面板")

# iOS 側邊欄控制台
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
    st.markdown("1. 在 **「玩家操作區」** 直接**左右拖曳罐子**調整順序。\n"
                "2. 調整完畢後，點擊下方 **「確定檢查」** 提交答案。\n"
                "3. 系統會提示有幾個罐子**「顏色與位置完全正確」**。\n"
                "4. 點擊 **「揭曉神秘箱」** 可直接偷看正確答案。")

# 主畫面配置：滿版大區域 [8, 2]
col_main, col_hist = st.columns([8, 2])

with col_main:
    # 區塊 A：神秘箱子區
    st.markdown('<div class="ios-glass-card">', unsafe_allow_html=True)
    st.subheader("📦 神秘箱子")
    
    if st.session_state.show_answer or st.session_state.game_over:
        cols = st.columns(st.session_state.difficulty)
        for i, color_name in enumerate(st.session_state.secret_sequence):
            with cols[i]:
                color_code = COLOR_MAP[color_name]
                st.markdown(f'''
                    <div style="text-align: center; width:100%;">
                        <div style="width: 50%; height: 10px; background: rgba(255,255,255,0.4); border-radius: 5px; margin: 0 auto -2px auto; max-width: 36px;"></div>
                        <div style="width: 85%; height: 90px; border-radius: 16px; box-shadow: inset 0 4px 8px rgba(255,255,255,0.3), 0 8px 16px rgba(0,0,0,0.3); border: 1.5px solid rgba(255,255,255,0.6); background: linear-gradient(to top, {color_code} 85%, rgba(255,255,255,0.2) 100%); margin: 0 auto; max-width: 60px;"></div>
                        <p style="margin-top:6px; font-weight:500; font-size:12px; color:#e2e8f0; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">{color_name}</p>
                    </div>
                ''', unsafe_allow_html=True)
        if st.session_state.game_over:
            st.success(f"🎉 恭喜闖關成功！共花費了 {len(st.session_state.history)} 個回合！")
    else:
        st.markdown(f'<div class="box-hidden-ios">🔒 箱內藏有 {st.session_state.difficulty} 個顏色的隱藏順序</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 區塊 B：玩家操作區（極致 iOS 玻璃拖曳引擎）
    st.markdown('<div class="ios-glass-card">', unsafe_allow_html=True)
    st.subheader("🖐️ 玩家操作區")
    st.caption("左右拖曳下方的罐子來排列你認為正確的順序：")
    
    current_jars = [{"name": name, "color": COLOR_MAP[name]} for name in st.session_state.player_sequence]
    
    # 內嵌 HTML5 程式碼優化：全面套用 iOS 玻璃微光、大圓角、禁止向外擠壓
    html_drag_component = f"""
    <div id="drag-container" style="display: flex; width: 100%; box-sizing: border-box; gap: 10px; padding: 15px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 18px; min-height: 150px; overflow: hidden;">
    </div>

    <script>
    const jars = {json.dumps(current_jars)};
    const container = document.getElementById('drag-container');

    function renderJars() {{
        container.innerHTML = '';
        jars.forEach((jar, index) => {{
            const div = document.createElement('div');
            div.className = 'jar-item';
            div.style.textAlign = 'center';
            div.style.cursor = 'grab';
            div.style.flex = '1 1 0%';
            div.style.minWidth = '0';
            div.draggable = true;
            div.dataset.index = index;
            
            // 罐子設計：半透明磨砂上蓋 + 高透光 3D 液體瓶身
            div.innerHTML = `
                <div style="width: 50%; height: 10px; background: rgba(255, 255, 255, 0.4); border-radius: 5px; margin: 0 auto -2px auto; max-width: 36px;"></div>
                <div style="width: 85%; height: 90px; border-radius: 16px; box-shadow: inset 0 4px 8px rgba(255,255,255,0.4), 0 8px 20px rgba(0,0,0,0.4); border: 1.5px solid rgba(255,255,255,0.7); background: linear-gradient(to top, ${{jar.color}} 85%, rgba(255,255,255,0.2) 100%); margin: 0 auto; max-width: 60px; transition: transform 0.2s ease;"></div>
                <p style="margin-top:6px; font-weight:500; font-size:12px; color:#cbd5e1; font-family: -apple-system, sans-serif; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; padding: 0 2px;">${{jar.name}}</p>
            `;

            // 拖曳動效
            div.addEventListener('dragstart', (e) => {{
                e.dataTransfer.setData('text/plain', index);
                div.style.opacity = '0.3';
                div.style.transform = 'scale(0.95)';
            }});

            div.addEventListener('dragend', () => {{
                div.style.opacity = '1';
                div.style.transform = 'scale(1)';
            }});

            div.addEventListener('dragover', (e) => {{
                e.preventDefault();
            }});

            div.addEventListener('drop', (e) => {{
                e.preventDefault();
                const fromIndex = e.dataTransfer.getData('text/plain');
                const toIndex = div.dataset.index;
                
                if (fromIndex !== toIndex) {{
                    const movedItem = jars.splice(fromIndex, 1)[0];
                    jars.splice(toIndex, 0, movedItem);
                    renderJars();
                    
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

    import streamlit.components.v1 as components
    response = components.html(html_drag_component, height=170, scrolling=False)
    
    st.write("")
    
    # iOS 按鈕列
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("􀃳 確定檢查！", type="primary", use_container_width=True, disabled=st.session_state.game_over):
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
        if st.button("􀄧 揭曉神秘箱答案", type="secondary", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_hist:
    # 右側 iOS 歷史紀錄
    st.subheader("📊 歷史紀錄")
    if not st.session_state.history:
        st.info("暫無紀錄")
    else:
        for record in reversed(st.session_state.history):
            jar_htmls = ""
            for name in record["sequence"]:
                code = COLOR_MAP.get(name, "#ffffff")
                jar_htmls += f'<div class="mini-jar-ios" style="background-color: {code};" title="{name}"></div>'
                
            st.markdown(f'''
                <div class="ios-history-card">
                    <div style="font-weight:600; font-size:12px; margin-bottom:5px; display:flex; justify-content:space-between; color:#94a3b8;">
                        <span>第 {record["round"]} 回合</span>
                        <span style="color:#3b82f6;">🎯 {record["correct"]} 對</span>
                    </div>
                    <div style="display:flex; flex-wrap:nowrap; overflow:hidden;">{jar_htmls}</div>
                </div>
            ''', unsafe_allow_html=True)
