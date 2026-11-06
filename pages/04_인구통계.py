# ... existing code ...
# 4. 사이드바 - 메인 메뉴 및 필터
st.sidebar.header("🧭 대시보드 메뉴")
menu = st.sidebar.radio(
    "분석 항목 선택",
    [
        "📈 연도별 남녀 연령별 인구 비교", 
        "🏆 연령대별 자치구 순위 막대그래프", 
        "🌟 [추가] 자치구별 고령화율(노령화 지표) 분석",
        "🎮 [미니게임] 나이 먹는 코인 캐처!"
    ]
)

# 공통 연령대 목록
# ... existing code ...

# ==========================================
# MENU 3: [추가] 자치구별 고령화율(노령화 지표) 분석
# ==========================================
elif menu == "🌟 [추가] 자치구별 고령화율(노령화 지표) 분석":
    st.title("🌟 [AI 추천 추가 기능] 자치구별 고령 인구 비율 분석")
    st.write("지속적인 저출산·고령화 사회에 맞춰, 각 자치구별 **60세 이상 고령 인구의 비율(총인구 대비)**을 비교하여 어느 지역이 고령화가 진행되었는지 한눈에 보여줍니다.")

    years = [str(y) for y in range(2020, 2026)]
    selected_year = st.sidebar.selectbox("기준 연도 선택", years, index=len(years) - 1)

    gu_df = df[df['지역명'] != '서울특별시'].copy()

    # 60세 이상 인구 합산 계산
    old_age_cols = [f'{selected_year}년_거주자_60~69세', f'{selected_year}년_거주자_70~79세', 
                    f'{selected_year}년_거주자_80~89세', f'{selected_year}년_거주자_90~99세', f'{selected_year}년_거주자_100세 이상']
    
    total_col = f'{selected_year}년_거주자_총인구수'

    gu_df['60세이상_인구합계'] = gu_df[old_age_cols].sum(axis=1)
    gu_df['고령인구비율(%)'] = (gu_df['60세이상_인구합계'] / gu_df[total_col]) * 100

    # 비율 높은 순으로 정렬
    gu_df_aged = gu_df.sort_values(by='고령인구비율(%)', ascending=False)

    fig = px.bar(
        gu_df_aged,
        x='고령인구비율(%)',
        y='지역명',
        orientation='h',
        title=f"<b>{selected_year}년</b> 서울시 자치구별 60세 이상 고령 인구 비율 (%)",
        text='고령인구비율(%)',
        color='고령인구비율(%)',
        color_continuous_scale='Reds'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=650)
    
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MENU 4: 🎮 [미니게임] 나이 먹는 코인 캐처!
# ==========================================
elif menu == "🎮 [미니게임] 나이 먹는 코인 캐처!":
    st.title("🎮 [미니게임] 나이 먹는 코인 캐처 (Age-Up Coin Game)")
    st.caption("떨어지는 코인을 먹고 100세까지 건강하게 나이를 먹어보세요!")

    # HTML/JS 기반 미니게임 임베딩
    game_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
            body { font-family: 'Jua', sans-serif; user-select: none; background: #0f172a; color: white; }
            #game-canvas { background: linear-gradient(to bottom, #1e293b, #334155); border-radius: 12px; }
        </style>
    </head>
    <body class="p-2 flex flex-col items-center justify-center min-h-screen">
        <div class="w-full max-w-lg bg-slate-800 p-4 rounded-2xl border-2 border-slate-700 shadow-2xl relative">
            <div class="flex justify-between items-center mb-2 px-1">
                <span id="ui-age" class="text-xl font-black text-amber-400">🎂 10세</span>
                <span id="ui-score" class="text-lg text-emerald-400">⭐ 0점</span>
                <span id="ui-life" class="text-lg text-rose-400">❤️❤️❤️</span>
            </div>
            
            <div class="relative w-full aspect-[4/5] max-h-[460px]">
                <canvas id="game-canvas" class="w-full h-full block"></canvas>
                <div id="overlay" class="absolute inset-0 bg-slate-950/90 rounded-xl flex flex-col items-center justify-center p-6 text-center">
                    <div id="overlay-icon" class="text-6xl mb-2">👦</div>
                    <h2 id="overlay-title" class="text-2xl font-bold text-amber-300 mb-2">나이 먹는 코인 받기!</h2>
                    <p class="text-xs text-slate-300 mb-4">
                        💰 <b>황금 코인</b>: +1세 / +100점<br>
                        ⭐ <b>황금 별</b>: +5세 / +500점<br>
                        🧪 <b>젊음의 묘약</b>: -3세 / 체력 회복<br>
                        💣 <b>해골 폭탄</b>: -1개 목숨 / 손상
                    </p>
                    <button id="start-btn" class="w-full py-3 bg-amber-500 hover:bg-amber-400 text-slate-900 font-black rounded-xl text-lg shadow-lg active:scale-95 transition">
                        시작하기 🚀
                    </button>
                </div>
            </div>

            <!-- 모바일/화면 조작 버튼 -->
            <div class="grid grid-cols-2 gap-2 mt-3 sm:hidden">
                <button id="btn-left" class="py-3 bg-slate-700 active:bg-amber-600 rounded-xl text-xl font-bold">👈 왼쪽</button>
                <button id="btn-right" class="py-3 bg-slate-700 active:bg-amber-600 rounded-xl text-xl font-bold">오른쪽 👉</button>
            </div>
        </div>

        <script>
            // Web Audio API 사운드 효과
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            function playSound(type) {
                if (audioCtx.state === 'suspended') audioCtx.resume();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);

                if (type === 'coin') {
                    osc.frequency.setValueAtTime(987.77, audioCtx.currentTime);
                    osc.frequency.setValueAtTime(1318.51, audioCtx.currentTime + 0.08);
                    gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.2);
                } else if (type === 'hit') {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(150, audioCtx.currentTime);
                    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.2);
                } else if (type === 'potion') {
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(300, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(600, audioCtx.currentTime + 0.25);
                    gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.25);
                }
            }

            const canvas = document.getElementById('game-canvas');
            const ctx = canvas.getContext('2d');
            function resize() { canvas.width = canvas.clientWidth; canvas.height = canvas.clientHeight; }
            resize(); window.addEventListener('resize', resize);

            let gameState = 'START';
            let age = 10, score = 0, life = 3;
            let items = [], spawnTimer = 0;
            const keys = { left: false, right: false };

            const player = { x: 0, y: 0, w: 40, h: 50, speed: 6 };

            window.addEventListener('keydown', e => {
                if (e.key === 'ArrowLeft' || e.key === 'a') keys.left = true;
                if (e.key === 'ArrowRight' || e.key === 'd') keys.right = true;
            });
            window.addEventListener('keyup', e => {
                if (e.key === 'ArrowLeft' || e.key === 'a') keys.left = false;
                if (e.key === 'ArrowRight' || e.key === 'd') keys.right = false;
            });

            document.getElementById('btn-left').onmousedown = document.getElementById('btn-left').ontouchstart = () => keys.left = true;
            document.getElementById('btn-left').onmouseup = document.getElementById('btn-left').ontouchend = () => keys.left = false;
            document.getElementById('btn-right').onmousedown = document.getElementById('btn-right').ontouchstart = () => keys.right = true;
            document.getElementById('btn-right').onmouseup = document.getElementById('btn-right').ontouchend = () => keys.right = false;

            function getEmoji() {
                if (age < 20) return '👦';
                if (age < 40) return '👨';
                if (age < 60) return '👨‍💼';
                if (age < 80) return '👴';
                return '🧙‍♂️';
            }

            function startGame() {
                age = 10; score = 0; life = 3; items = [];
                player.x = canvas.width / 2 - 20;
                player.y = canvas.height - 60;
                document.getElementById('overlay').classList.add('hidden');
                gameState = 'PLAYING';
                updateUI();
            }

            function updateUI() {
                document.getElementById('ui-age').innerText = `🎂 ${age}세`;
                document.getElementById('ui-score').innerText = `⭐ ${score}점`;
                document.getElementById('ui-life').innerText = '❤️'.repeat(life) + '🖤'.repeat(3 - life);
            }

            function gameOver() {
                gameState = 'GAMEOVER';
                document.getElementById('overlay-icon').innerText = age >= 100 ? '👑👴' : '🪦';
                document.getElementById('overlay-title').innerText = age >= 100 ? '100세 만수무강 달성!' : '게임 오버!';
                document.getElementById('start-btn').innerText = '다시 하기 🔄';
                document.getElementById('overlay').classList.remove('hidden');
            }

            document.getElementById('start-btn').onclick = startGame;

            function loop() {
                if (gameState === 'PLAYING') {
                    if (keys.left) player.x = Math.max(0, player.x - player.speed);
                    if (keys.right) player.x = Math.min(canvas.width - player.w, player.x + player.speed);

                    spawnTimer++;
                    if (spawnTimer > 40) {
                        spawnTimer = 0;
                        const r = Math.random();
                        let type = 'COIN', emoji = '💰';
                        if (r < 0.6) { type = 'COIN'; emoji = '💰'; }
                        else if (r < 0.75) { type = 'STAR'; emoji = '⭐'; }
                        else if (r < 0.88) { type = 'POTION'; emoji = '🧪'; }
                        else { type = 'BOMB'; emoji = '💣'; }
                        items.push({ x: Math.random() * (canvas.width - 30), y: -30, type, emoji, speed: Math.random() * 2 + 3 });
                    }

                    for (let i = items.length - 1; i >= 0; i--) {
                        const item = items[i];
                        item.y += item.speed;

                        // Collision
                        if (item.x < player.x + player.w && item.x + 30 > player.x &&
                            item.y < player.y + player.h && item.y + 30 > player.y) {
                            
                            if (item.type === 'COIN') { age += 1; score += 100; playSound('coin'); }
                            else if (item.type === 'STAR') { age += 5; score += 500; playSound('coin'); }
                            else if (item.type === 'POTION') { age = Math.max(10, age - 3); if (life < 3) life++; playSound('potion'); }
                            else if (item.type === 'BOMB') { life -= 1; playSound('hit'); }

                            updateUI();
                            items.splice(i, 1);

                            if (life <= 0 || age >= 100) gameOver();
                            continue;
                        }
                        if (item.y > canvas.height) items.splice(i, 1);
                    }
                }

                // Render
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.font = '24px serif';
                items.forEach(it => ctx.fillText(it.emoji, it.x, it.y + 24));

                ctx.font = '36px serif';
                ctx.fillText(getEmoji(), player.x, player.y + 36);

                requestAnimationFrame(loop);
            }
            loop();
        </script>
    </body>
    </html>
    """
    st.components.v1.html(game_html, height=620, scrolling=False)
