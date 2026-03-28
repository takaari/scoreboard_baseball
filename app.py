import streamlit as st
import random
import base64

def play_sound_autoplay(file_path):
    import uuid

    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

    unique_id = uuid.uuid4()

    audio_html = f"""
    <audio autoplay id="{unique_id}">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """

    st.markdown(audio_html, unsafe_allow_html=True)
"""
def play_bgm_loop(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

    audio_html = f"""
    <audio autoplay loop id="bgm">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
"""


st.set_page_config(
    page_title="スコアボード⚾ベースボール",
    layout="wide"   # ← これが重要
)


st.markdown("<h2 style='text-align:center;'>スコアボード⚾ベースボール</h2>", unsafe_allow_html=True)




    
st.markdown("""
<style>

/* ===== 背景（最重要） ===== */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0b3d2e !important;  /* 深緑 */
}

/* サイドバーも同色に */
[data-testid="stSidebar"] {
    background-color: #0b3d2e;
}

/* ===== 全テキスト ===== */
* {
    color: white !important;
}

/* ===== 見出し ===== */
h1, h2, h3, h4 {
    color: white !important;
}

/* ===== スコアボード ===== */
table {
    width: 100%;
    border-collapse: collapse;
    text-align: center;
    color: white;
}

th, td {
    border: 2px solid white !important;
    padding: 6px 10px;
}

th {
    background-color: rgba(255,255,255,0.2);
}

/* ===== ボタン ===== */
button[kind="primary"], button {
    background-color: #145a32 !important;
    color: white !important;
    border: 2px solid white !important;
}

button:hover {
    background-color: #1e8449 !important;
}

</style>
""", unsafe_allow_html=True)



# -------------------------
# セッション初期化
# -------------------------
if "inning" not in st.session_state:
    st.session_state.inning = 1
if "top" not in st.session_state:
    st.session_state.top = True
if "scores_top" not in st.session_state:
    st.session_state.scores_top = [None] * 9
if "scores_bottom" not in st.session_state:
    st.session_state.scores_bottom = [None] * 9
if "finished" not in st.session_state:
    st.session_state.finished = False
if "ready" not in st.session_state:
    st.session_state.ready = False
if "play_hit_sound" not in st.session_state:
    st.session_state.play_hit_sound = False
#if "bgm_started" not in st.session_state:
#    st.session_state.bgm_started = False
#if "bgm_playing" not in st.session_state:
#    st.session_state.bgm_playing = False
#if "bgm_restart" not in st.session_state:
#    st.session_state.bgm_restart = False

# -------------------------
# チーム名入力
# -------------------------
if not st.session_state.ready:
    st.subheader("チーム名を入力してください")

    team_top = st.text_input("先攻チーム名（表）", value="チームA")
    team_bottom = st.text_input("後攻チーム名（裏）", value="チームB")

    if st.button("▶ ゲーム開始"):
        st.session_state.team_top = team_top
        st.session_state.team_bottom = team_bottom
        st.session_state.ready = True

        # 👇 BGMスタート
#        st.session_state.bgm_playing = True

#        st.rerun()

    st.stop()  # ← ここで以降の表示を止める
    
team_top = st.session_state.team_top
team_bottom = st.session_state.team_bottom

# -------------------------
# BGM（試合中ずっと）
# -------------------------
#if st.session_state.get("bgm_playing") and not st.session_state.get("bgm_started"):
#    play_bgm_loop("sounds/cheering_pep_squad.mp3")
#    st.session_state.bgm_started = True

# -------------------------
# 効果音（カキーン）
# -------------------------
if st.session_state.get("play_hit_sound"):
    play_sound_autoplay("sounds/batto.mp3")
    st.session_state.play_hit_sound = False
# -------------------------
# BGM再開トリガー
# -------------------------
#if st.session_state.get("bgm_restart"):
#    st.session_state.bgm_playing = True
#    st.session_state.bgm_restart = False

# -------------------------
# 現在の回表示
# -------------------------
col1, col2 = st.columns([3, 2])

with col1:
    if not st.session_state.finished:
        half = "表" if st.session_state.top else "裏"
        st.subheader(f"{st.session_state.inning}回 {half}")

with col2:
    if not st.session_state.finished:
        if st.button("▶ 次の結果を表示"):

            score = random.choices(
                [0, 1, 2, 3, 4, 5],
                weights=[0.65, 0.14, 0.10, 0.07, 0.03, 0.01],
                k=1
            )[0]

            # 👇 ここ追加（先にフラグ立てる）
            if score > 0:
                st.session_state.play_hit_sound = True
                
                st.session_state.bgm_playing = False
                st.session_state.bgm_restart = True

            if st.session_state.top:
                # 表の攻撃
                st.session_state.scores_top[st.session_state.inning - 1] = score
                st.session_state.top = False

                # ★ 9回表終了時の特別判定
                if st.session_state.inning == 9:
                    top_total = sum(
                        s for s in st.session_state.scores_top if isinstance(s, int)
                    )
                    bottom_total = sum(
                        s for s in st.session_state.scores_bottom if isinstance(s, int)
                    )

                    if bottom_total > top_total:
                        st.session_state.scores_bottom[8] = "X"
                        st.session_state.finished = True
                        st.rerun()

            else:
                # 裏の攻撃
                st.session_state.scores_bottom[st.session_state.inning - 1] = score
                st.session_state.top = True
                st.session_state.inning += 1

                if st.session_state.inning > 9:
                    st.session_state.finished = True

            st.rerun()



# -------------------------
# スコアボード表示
# -------------------------
st.markdown("### スコアボード")

html = "<table style='width:100%; border-collapse:collapse; text-align:center;'>"
html += "<tr><th></th>" + "".join(f"<th>{i}</th>" for i in range(1,10)) + "<th>R</th></tr>"

top_total = sum(s for s in st.session_state.scores_top if isinstance(s, int))
bottom_total = sum(s for s in st.session_state.scores_bottom if isinstance(s, int))


html += f"<tr><td>{team_top}</td>"
for s in st.session_state.scores_top:
    html += f"<td>{'' if s is None else s}</td>"
html += f"<td><b>{top_total}</b></td></tr>"

html += f"<tr><td>{team_bottom}</td>"
for s in st.session_state.scores_bottom:
    html += f"<td>{'' if s is None else s}</td>"
html += f"<td><b>{bottom_total}</b></td></tr>"

html += "</table>"

st.markdown(html, unsafe_allow_html=True)


    
# -------------------------
# 勝敗判定
# -------------------------
if st.session_state.finished:
    st.divider()
    if top_total > bottom_total:
        st.success(f"🏆 勝利：{team_top}")
    elif bottom_total > top_total:
        st.success(f"🏆 勝利：{team_bottom}")
    else:
        st.info("🤝 引き分け")
