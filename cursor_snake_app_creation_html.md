# 스네이크 게임 개발 요청
_Exported on 11/27/2025 at 12:18:05 GMT+9 from Cursor (2.1.36)_

---

**User**

HTML, CSS, JavaScript만을 사용하여 완전히 작동하는 스네이크 게임을 개발해줘.



단일 HTML 파일로 파일명은 snake.html로 생성해.



---

**Cursor**


기존 파일 구조 확인 중. 이후 스네이크 게임 계획을 제시합니다.



스네이크 게임 계획 수립 중.


---

**User**

Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

---

**Cursor**


스네이크 게임 구현을 시작합니다. `snake.html` 파일을 생성합니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            gameRunning = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            const key = e.key;
            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                if (index === 0) {
                    // 머리
                    ctx.fillStyle = '#4ecdc4';
                } else {
                    // 몸통
                    ctx.fillStyle = '#45b7aa';
                }
                
                ctx.fillRect(
                    segment.x * CELL_SIZE + 1,
                    segment.y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            });
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>

```


린터 오류 확인 중.



스네이크 게임 구현을 완료했습니다.

## 구현된 기능

1. **게임 구조**
   - HTML5 Canvas 기반 게임 보드 (400x400px, 20x20 그리드)
   - 점수 표시 패널 (현재 점수, 최고 점수)
   - 게임 오버 오버레이

2. **게임 로직**
   - 뱀 이동 (방향키로 제어)
   - 음식 생성 및 먹기
   - 벽 충돌 감지
   - 자기 자신과의 충돌 감지
   - 점수 증가 및 뱀 길이 증가

3. **추가 기능**
   - 최고 점수 저장 (localStorage)
   - 게임 재시작
   - 반응형 디자인

4. **UI/UX**
   - 그라데이션 배경 및 카드 스타일
   - 그리드 표시
   - 뱀 머리/몸통 색상 구분
   - 부드러운 애니메이션 효과

`snake.html` 파일을 브라우저에서 열면 바로 플레이할 수 있습니다. 방향키로 뱀을 조종하고 음식을 먹으며 점수를 올리세요.

---

**User**

일시정지 기능 추가해주고 뱀이 움직이는 모양을 좀더 현실감있게 눈이랑 혓바닥이나 비늘 같은 그래픽을 표현해줘

---

**Cursor**


일시정지 기능 추가와 뱀 그래픽 개선을 진행합니다. 현재 파일을 확인 중입니다.



일시정지 기능 추가와 뱀 그래픽 개선 중입니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            gameRunning = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            const key = e.key;
            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                if (index === 0) {
                    // 머리
                    ctx.fillStyle = '#4ecdc4';
                } else {
                    // 몸통
                    ctx.fillStyle = '#45b7aa';
                }
                
                ctx.fillRect(
                    segment.x * CELL_SIZE + 1,
                    segment.y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            });
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            gameRunning = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            const key = e.key;
            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                if (index === 0) {
                    // 머리
                    ctx.fillStyle = '#4ecdc4';
                } else {
                    // 몸통
                    ctx.fillStyle = '#45b7aa';
                }
                
                ctx.fillRect(
                    segment.x * CELL_SIZE + 1,
                    segment.y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            });
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            gameRunning = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            const key = e.key;
            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                if (index === 0) {
                    // 머리
                    ctx.fillStyle = '#4ecdc4';
                } else {
                    // 몸통
                    ctx.fillStyle = '#45b7aa';
                }
                
                ctx.fillRect(
                    segment.x * CELL_SIZE + 1,
                    segment.y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            });
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            gameRunning = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            const key = e.key;
            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                if (index === 0) {
                    // 머리
                    ctx.fillStyle = '#4ecdc4';
                } else {
                    // 몸통
                    ctx.fillStyle = '#45b7aa';
                }
                
                ctx.fillRect(
                    segment.x * CELL_SIZE + 1,
                    segment.y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            });
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            const key = e.key;
            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                if (index === 0) {
                    // 머리
                    ctx.fillStyle = '#4ecdc4';
                } else {
                    // 몸통
                    ctx.fillStyle = '#45b7aa';
                }
                
                ctx.fillRect(
                    segment.x * CELL_SIZE + 1,
                    segment.y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            });
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                if (index === 0) {
                    // 머리
                    ctx.fillStyle = '#4ecdc4';
                } else {
                    // 몸통
                    ctx.fillStyle = '#45b7aa';
                }
                
                ctx.fillRect(
                    segment.x * CELL_SIZE + 1,
                    segment.y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            });
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                if (index === 0) {
                    // 머리
                    ctx.fillStyle = '#4ecdc4';
                } else {
                    // 몸통
                    ctx.fillStyle = '#45b7aa';
                }
                
                ctx.fillRect(
                    segment.x * CELL_SIZE + 1,
                    segment.y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            });
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);
    </script>
</body>
</html>


```


린터 오류 확인 중입니다.



일시정지 기능과 뱀 그래픽 개선을 완료했습니다.

## 추가된 기능

### 1. 일시정지 기능
- **Space** 또는 **P** 키로 일시정지/재개
- 일시정지 중 오버레이 표시
- 일시정지 중에는 게임 업데이트 중단

### 2. 뱀 그래픽 개선
- **눈**: 방향에 따라 위치 변경
  - 오른쪽: 오른쪽에 눈
  - 왼쪽: 왼쪽에 눈
  - 위: 위쪽에 눈
  - 아래: 아래쪽에 눈
- **혓바닥**: 머리 앞쪽에 빨간색 혓바닥 표시
- **비늘 패턴**: 몸통에 대각선 비늘 패턴 추가
- **그라데이션**: 머리와 몸통에 그라데이션 적용
- **윤곽선**: 각 세그먼트에 윤곽선 추가

게임을 실행하면 뱀이 더 현실적으로 보이고, Space 또는 P 키로 언제든 일시정지할 수 있습니다.

---

**User**

꼬리도 표현해주고 배경화면은 귀여운 뱀 애니메이션 넣어줘

---

**Cursor**


뱀 꼬리 표현 추가와 배경 귀여운 뱀 애니메이션 추가를 진행합니다. 현재 파일을 확인 중입니다.



뱀 꼬리 표현 추가와 배경 귀여운 뱀 애니메이션 추가 중입니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <div class="background-snakes" id="backgroundSnakes"></div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <div class="background-snakes" id="backgroundSnakes"></div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else if (index === snake.length - 1) {
                    // 꼬리 그리기
                    drawSnakeTail(x, y, index);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <div class="background-snakes" id="backgroundSnakes"></div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else if (index === snake.length - 1) {
                    // 꼬리 그리기
                    drawSnakeTail(x, y, index);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 뱀 꼬리 그리기
        function drawSnakeTail(x, y, index) {
            const centerX = x + CELL_SIZE / 2;
            const centerY = y + CELL_SIZE / 2;
            
            // 꼬리 방향 계산 (이전 세그먼트로부터)
            const prevSegment = snake[index - 1];
            const tailDirection = {
                x: prevSegment.x - snake[index].x,
                y: prevSegment.y - snake[index].y
            };

            // 꼬리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 윤곽선
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 끝 부분 (뾰족하게)
            ctx.fillStyle = '#3a9d8f';
            ctx.beginPath();
            
            if (tailDirection.x === 1) { // 왼쪽으로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.x === -1) { // 오른쪽으로 향하는 꼬리
                ctx.moveTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.y === 1) { // 위로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            } else if (tailDirection.y === -1) { // 아래로 향하는 꼬리
                ctx.moveTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            }
            
            ctx.fill();
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <div class="background-snakes" id="backgroundSnakes"></div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            createBackgroundSnakes();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 배경 귀여운 뱀 생성
        function createBackgroundSnakes() {
            const container = document.getElementById('backgroundSnakes');
            const snakeCount = 5;
            
            for (let i = 0; i < snakeCount; i++) {
                const snake = document.createElement('div');
                snake.className = 'cute-snake';
                snake.innerHTML = createCuteSnakeSVG();
                container.appendChild(snake);
            }
        }

        // 귀여운 뱀 SVG 생성
        function createCuteSnakeSVG() {
            return `
                <svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
                    <!-- 뱀 몸통 -->
                    <ellipse cx="30" cy="30" rx="25" ry="12" fill="#4ecdc4" opacity="0.8"/>
                    <!-- 뱀 머리 -->
                    <circle cx="45" cy="30" r="10" fill="#2ecc71" opacity="0.9"/>
                    <!-- 눈 -->
                    <circle cx="48" cy="27" r="2" fill="#fff"/>
                    <circle cx="48" cy="33" r="2" fill="#fff"/>
                    <circle cx="49" cy="27" r="1" fill="#000"/>
                    <circle cx="49" cy="33" r="1" fill="#000"/>
                    <!-- 혓바닥 -->
                    <path d="M 55 30 L 60 28 L 60 32 Z" fill="#e74c3c" opacity="0.8"/>
                    <!-- 비늘 패턴 -->
                    <path d="M 20 30 L 25 25 L 30 30 L 25 35 Z" fill="#45b7aa" opacity="0.6"/>
                    <path d="M 15 30 L 20 25 L 25 30 L 20 35 Z" fill="#45b7aa" opacity="0.6"/>
                </svg>
            `;
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else if (index === snake.length - 1) {
                    // 꼬리 그리기
                    drawSnakeTail(x, y, index);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 뱀 꼬리 그리기
        function drawSnakeTail(x, y, index) {
            const centerX = x + CELL_SIZE / 2;
            const centerY = y + CELL_SIZE / 2;
            
            // 꼬리 방향 계산 (이전 세그먼트로부터)
            const prevSegment = snake[index - 1];
            const tailDirection = {
                x: prevSegment.x - snake[index].x,
                y: prevSegment.y - snake[index].y
            };

            // 꼬리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 윤곽선
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 끝 부분 (뾰족하게)
            ctx.fillStyle = '#3a9d8f';
            ctx.beginPath();
            
            if (tailDirection.x === 1) { // 왼쪽으로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.x === -1) { // 오른쪽으로 향하는 꼬리
                ctx.moveTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.y === 1) { // 위로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            } else if (tailDirection.y === -1) { // 아래로 향하는 꼬리
                ctx.moveTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            }
            
            ctx.fill();
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```


린터 오류 확인 중입니다.



뱀 꼬리 표현과 배경 귀여운 뱀 애니메이션을 추가했습니다.

## 추가된 기능

### 1. 뱀 꼬리 표현
- 마지막 세그먼트를 꼬리로 그리기
- 이전 세그먼트 방향에 따라 꼬리 끝이 뾰족하게 표시
- 방향별 꼬리 모양 적용 (왼쪽/오른쪽/위/아래)

### 2. 배경 귀여운 뱀 애니메이션
- 배경에 5마리의 귀여운 뱀 추가
- 좌우로 부드럽게 이동하는 애니메이션
- 위아래로 살짝 흔들리는 효과
- SVG로 구현 (눈, 혓바닥, 비늘 패턴 포함)
- 각 뱀마다 다른 속도와 시작 시간으로 자연스러운 움직임

배경의 귀여운 뱀들이 계속 움직이며, 게임 내 뱀도 꼬리가 표현됩니다.

---

**User**

뱀이 먹는 먹이를 사과모양으로 빨갛게표현해주고 배경색은 보라색 말고 다른 색으로 해줘

---

**Cursor**


먹이를 빨간 사과 모양으로 변경하고 배경색을 보라색이 아닌 색으로 변경 중입니다.



먹이를 빨간 사과 모양으로 변경하고 배경색을 보라색이 아닌 색으로 변경 중입니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <div class="background-snakes" id="backgroundSnakes"></div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            createBackgroundSnakes();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 배경 귀여운 뱀 생성
        function createBackgroundSnakes() {
            const container = document.getElementById('backgroundSnakes');
            const snakeCount = 5;
            
            for (let i = 0; i < snakeCount; i++) {
                const snake = document.createElement('div');
                snake.className = 'cute-snake';
                snake.innerHTML = createCuteSnakeSVG();
                container.appendChild(snake);
            }
        }

        // 귀여운 뱀 SVG 생성
        function createCuteSnakeSVG() {
            return `
                <svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
                    <!-- 뱀 몸통 -->
                    <ellipse cx="30" cy="30" rx="25" ry="12" fill="#4ecdc4" opacity="0.8"/>
                    <!-- 뱀 머리 -->
                    <circle cx="45" cy="30" r="10" fill="#2ecc71" opacity="0.9"/>
                    <!-- 눈 -->
                    <circle cx="48" cy="27" r="2" fill="#fff"/>
                    <circle cx="48" cy="33" r="2" fill="#fff"/>
                    <circle cx="49" cy="27" r="1" fill="#000"/>
                    <circle cx="49" cy="33" r="1" fill="#000"/>
                    <!-- 혓바닥 -->
                    <path d="M 55 30 L 60 28 L 60 32 Z" fill="#e74c3c" opacity="0.8"/>
                    <!-- 비늘 패턴 -->
                    <path d="M 20 30 L 25 25 L 30 30 L 25 35 Z" fill="#45b7aa" opacity="0.6"/>
                    <path d="M 15 30 L 20 25 L 25 30 L 20 35 Z" fill="#45b7aa" opacity="0.6"/>
                </svg>
            `;
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 음식 그리기
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else if (index === snake.length - 1) {
                    // 꼬리 그리기
                    drawSnakeTail(x, y, index);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 뱀 꼬리 그리기
        function drawSnakeTail(x, y, index) {
            const centerX = x + CELL_SIZE / 2;
            const centerY = y + CELL_SIZE / 2;
            
            // 꼬리 방향 계산 (이전 세그먼트로부터)
            const prevSegment = snake[index - 1];
            const tailDirection = {
                x: prevSegment.x - snake[index].x,
                y: prevSegment.y - snake[index].y
            };

            // 꼬리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 윤곽선
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 끝 부분 (뾰족하게)
            ctx.fillStyle = '#3a9d8f';
            ctx.beginPath();
            
            if (tailDirection.x === 1) { // 왼쪽으로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.x === -1) { // 오른쪽으로 향하는 꼬리
                ctx.moveTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.y === 1) { // 위로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            } else if (tailDirection.y === -1) { // 아래로 향하는 꼬리
                ctx.moveTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            }
            
            ctx.fill();
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <div class="background-snakes" id="backgroundSnakes"></div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            createBackgroundSnakes();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 배경 귀여운 뱀 생성
        function createBackgroundSnakes() {
            const container = document.getElementById('backgroundSnakes');
            const snakeCount = 5;
            
            for (let i = 0; i < snakeCount; i++) {
                const snake = document.createElement('div');
                snake.className = 'cute-snake';
                snake.innerHTML = createCuteSnakeSVG();
                container.appendChild(snake);
            }
        }

        // 귀여운 뱀 SVG 생성
        function createCuteSnakeSVG() {
            return `
                <svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
                    <!-- 뱀 몸통 -->
                    <ellipse cx="30" cy="30" rx="25" ry="12" fill="#4ecdc4" opacity="0.8"/>
                    <!-- 뱀 머리 -->
                    <circle cx="45" cy="30" r="10" fill="#2ecc71" opacity="0.9"/>
                    <!-- 눈 -->
                    <circle cx="48" cy="27" r="2" fill="#fff"/>
                    <circle cx="48" cy="33" r="2" fill="#fff"/>
                    <circle cx="49" cy="27" r="1" fill="#000"/>
                    <circle cx="49" cy="33" r="1" fill="#000"/>
                    <!-- 혓바닥 -->
                    <path d="M 55 30 L 60 28 L 60 32 Z" fill="#e74c3c" opacity="0.8"/>
                    <!-- 비늘 패턴 -->
                    <path d="M 20 30 L 25 25 L 30 30 L 25 35 Z" fill="#45b7aa" opacity="0.6"/>
                    <path d="M 15 30 L 20 25 L 25 30 L 20 35 Z" fill="#45b7aa" opacity="0.6"/>
                </svg>
            `;
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 사과 그리기
            drawApple(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2
            );

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else if (index === snake.length - 1) {
                    // 꼬리 그리기
                    drawSnakeTail(x, y, index);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 뱀 꼬리 그리기
        function drawSnakeTail(x, y, index) {
            const centerX = x + CELL_SIZE / 2;
            const centerY = y + CELL_SIZE / 2;
            
            // 꼬리 방향 계산 (이전 세그먼트로부터)
            const prevSegment = snake[index - 1];
            const tailDirection = {
                x: prevSegment.x - snake[index].x,
                y: prevSegment.y - snake[index].y
            };

            // 꼬리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 윤곽선
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 끝 부분 (뾰족하게)
            ctx.fillStyle = '#3a9d8f';
            ctx.beginPath();
            
            if (tailDirection.x === 1) { // 왼쪽으로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.x === -1) { // 오른쪽으로 향하는 꼬리
                ctx.moveTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.y === 1) { // 위로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            } else if (tailDirection.y === -1) { // 아래로 향하는 꼬리
                ctx.moveTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            }
            
            ctx.fill();
            ctx.stroke();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```


사과 그리기 함수 추가 중입니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스네이크 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .background-snakes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cute-snake {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
            animation: floatSnake 20s infinite linear;
        }

        .cute-snake:nth-child(1) {
            top: 10%;
            animation-delay: 0s;
            animation-duration: 25s;
        }

        .cute-snake:nth-child(2) {
            top: 30%;
            animation-delay: -5s;
            animation-duration: 30s;
        }

        .cute-snake:nth-child(3) {
            top: 50%;
            animation-delay: -10s;
            animation-duration: 20s;
        }

        .cute-snake:nth-child(4) {
            top: 70%;
            animation-delay: -15s;
            animation-duration: 35s;
        }

        .cute-snake:nth-child(5) {
            top: 20%;
            animation-delay: -8s;
            animation-duration: 28s;
        }

        @keyframes floatSnake {
            0% {
                left: -100px;
                transform: translateY(0) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) rotate(5deg);
            }
            50% {
                transform: translateY(0) rotate(0deg);
            }
            75% {
                transform: translateY(30px) rotate(-5deg);
            }
            100% {
                left: calc(100% + 100px);
                transform: translateY(0) rotate(0deg);
            }
        }

        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        .score-panel {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            gap: 20px;
        }

        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            min-width: 120px;
        }

        .score-box h3 {
            font-size: 0.9em;
            margin-bottom: 5px;
            opacity: 0.9;
        }

        .score-box p {
            font-size: 1.8em;
            font-weight: bold;
        }

        .game-board-container {
            position: relative;
            display: inline-block;
        }

        #gameBoard {
            border: 3px solid #333;
            border-radius: 5px;
            background: #f0f0f0;
            display: block;
        }

        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .game-over.show {
            display: flex;
        }

        .pause-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
        }

        .pause-overlay.show {
            display: flex;
        }

        .pause-overlay h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .pause-overlay p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ff6b6b;
        }

        .game-over p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .game-over button {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .game-over button:hover {
            transform: scale(1.05);
        }

        .game-over button:active {
            transform: scale(0.95);
        }

        .instructions {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }

        .instructions p {
            margin: 5px 0;
        }

        @media (max-width: 500px) {
            .game-container {
                padding: 15px;
            }

            h1 {
                font-size: 1.8em;
            }

            .score-panel {
                flex-direction: column;
                gap: 10px;
            }

            #gameBoard {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🐍 스네이크 게임</h1>
        
        <div class="score-panel">
            <div class="score-box">
                <h3>현재 점수</h3>
                <p id="currentScore">0</p>
            </div>
            <div class="score-box">
                <h3>최고 점수</h3>
                <p id="highScore">0</p>
            </div>
        </div>

        <div class="game-board-container">
            <canvas id="gameBoard" width="400" height="400"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>Space 또는 P 키를 눌러 계속</p>
            </div>
        </div>

        <div class="instructions">
            <p>방향키(↑ ↓ ← →)를 사용하여 뱀을 조종하세요</p>
            <p>음식을 먹으면 점수가 올라가고 뱀이 길어집니다</p>
            <p>Space 또는 P 키로 일시정지할 수 있습니다</p>
        </div>
    </div>

    <div class="background-snakes" id="backgroundSnakes"></div>

    <script>
        // 게임 설정
        const GRID_SIZE = 20;
        const CELL_SIZE = 20;
        const BOARD_WIDTH = 400;
        const BOARD_HEIGHT = 400;
        const GRID_WIDTH = BOARD_WIDTH / CELL_SIZE;
        const GRID_HEIGHT = BOARD_HEIGHT / CELL_SIZE;

        // 게임 상태
        let canvas;
        let ctx;
        let snake = [];
        let direction = { x: 1, y: 0 };
        let nextDirection = { x: 1, y: 0 };
        let food = { x: 0, y: 0 };
        let score = 0;
        let gameRunning = false;
        let isPaused = false;
        let gameLoop = null;

        // DOM 요소
        const currentScoreEl = document.getElementById('currentScore');
        const highScoreEl = document.getElementById('highScore');
        const gameOverEl = document.getElementById('gameOver');
        const finalScoreEl = document.getElementById('finalScore');
        const pauseOverlayEl = document.getElementById('pauseOverlay');

        // 초기화
        function init() {
            canvas = document.getElementById('gameBoard');
            ctx = canvas.getContext('2d');
            
            // 최고 점수 불러오기
            const savedHighScore = localStorage.getItem('snakeHighScore');
            if (savedHighScore) {
                highScoreEl.textContent = savedHighScore;
            }

            resetGame();
            generateFood();
            draw();
            createBackgroundSnakes();
            
            // 키보드 이벤트 리스너
            document.addEventListener('keydown', handleKeyPress);
        }

        // 배경 귀여운 뱀 생성
        function createBackgroundSnakes() {
            const container = document.getElementById('backgroundSnakes');
            const snakeCount = 5;
            
            for (let i = 0; i < snakeCount; i++) {
                const snake = document.createElement('div');
                snake.className = 'cute-snake';
                snake.innerHTML = createCuteSnakeSVG();
                container.appendChild(snake);
            }
        }

        // 귀여운 뱀 SVG 생성
        function createCuteSnakeSVG() {
            return `
                <svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
                    <!-- 뱀 몸통 -->
                    <ellipse cx="30" cy="30" rx="25" ry="12" fill="#4ecdc4" opacity="0.8"/>
                    <!-- 뱀 머리 -->
                    <circle cx="45" cy="30" r="10" fill="#2ecc71" opacity="0.9"/>
                    <!-- 눈 -->
                    <circle cx="48" cy="27" r="2" fill="#fff"/>
                    <circle cx="48" cy="33" r="2" fill="#fff"/>
                    <circle cx="49" cy="27" r="1" fill="#000"/>
                    <circle cx="49" cy="33" r="1" fill="#000"/>
                    <!-- 혓바닥 -->
                    <path d="M 55 30 L 60 28 L 60 32 Z" fill="#e74c3c" opacity="0.8"/>
                    <!-- 비늘 패턴 -->
                    <path d="M 20 30 L 25 25 L 30 30 L 25 35 Z" fill="#45b7aa" opacity="0.6"/>
                    <path d="M 15 30 L 20 25 L 25 30 L 20 35 Z" fill="#45b7aa" opacity="0.6"/>
                </svg>
            `;
        }

        // 게임 리셋
        function resetGame() {
            snake = [
                { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
                { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
            ];
            direction = { x: 1, y: 0 };
            nextDirection = { x: 1, y: 0 };
            score = 0;
            currentScoreEl.textContent = score;
            gameOverEl.classList.remove('show');
            pauseOverlayEl.classList.remove('show');
            gameRunning = false;
            isPaused = false;
            
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
        }

        // 음식 생성
        function generateFood() {
            let newFood;
            do {
                newFood = {
                    x: Math.floor(Math.random() * GRID_WIDTH),
                    y: Math.floor(Math.random() * GRID_HEIGHT)
                };
            } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
            
            food = newFood;
        }

        // 키 입력 처리
        function handleKeyPress(e) {
            const key = e.key;

            // 일시정지 토글 (Space 또는 P)
            if ((key === ' ' || key === 'p' || key === 'P') && gameRunning) {
                togglePause();
                return;
            }

            // 일시정지 중이면 방향키 무시
            if (isPaused) return;

            if (!gameRunning && e.key.startsWith('Arrow')) {
                gameRunning = true;
                startGame();
            }

            if (key === 'ArrowUp' && direction.y === 0) {
                nextDirection = { x: 0, y: -1 };
            } else if (key === 'ArrowDown' && direction.y === 0) {
                nextDirection = { x: 0, y: 1 };
            } else if (key === 'ArrowLeft' && direction.x === 0) {
                nextDirection = { x: -1, y: 0 };
            } else if (key === 'ArrowRight' && direction.x === 0) {
                nextDirection = { x: 1, y: 0 };
            }
        }

        // 일시정지 토글
        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlayEl.classList.add('show');
            } else {
                pauseOverlayEl.classList.remove('show');
            }
        }

        // 게임 시작
        function startGame() {
            if (gameLoop) return;
            
            gameLoop = setInterval(() => {
                update();
                draw();
            }, 150);
        }

        // 게임 업데이트
        function update() {
            if (!gameRunning || isPaused) return;

            // 방향 업데이트
            direction = { ...nextDirection };

            // 뱀 머리 이동
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };

            // 벽 충돌 검사
            if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
                gameOver();
                return;
            }

            // 자기 자신과 충돌 검사
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }

            snake.unshift(head);

            // 음식 먹기 검사
            if (head.x === food.x && head.y === food.y) {
                score++;
                currentScoreEl.textContent = score;
                
                // 최고 점수 업데이트
                const currentHighScore = parseInt(highScoreEl.textContent) || 0;
                if (score > currentHighScore) {
                    highScoreEl.textContent = score;
                    localStorage.setItem('snakeHighScore', score);
                }
                
                generateFood();
            } else {
                snake.pop();
            }
        }

        // 게임 오버
        function gameOver() {
            gameRunning = false;
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            finalScoreEl.textContent = score;
            gameOverEl.classList.add('show');
        }

        // 재시작
        function restartGame() {
            resetGame();
            generateFood();
            draw();
        }

        // 그리기
        function draw() {
            // 배경 지우기
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, BOARD_WIDTH, BOARD_HEIGHT);

            // 그리드 그리기
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            for (let i = 0; i <= GRID_WIDTH; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, BOARD_HEIGHT);
                ctx.stroke();
            }
            for (let i = 0; i <= GRID_HEIGHT; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(BOARD_WIDTH, i * CELL_SIZE);
                ctx.stroke();
            }

            // 사과 그리기
            drawApple(
                food.x * CELL_SIZE + CELL_SIZE / 2,
                food.y * CELL_SIZE + CELL_SIZE / 2
            );

            // 뱀 그리기
            snake.forEach((segment, index) => {
                const x = segment.x * CELL_SIZE;
                const y = segment.y * CELL_SIZE;
                const centerX = x + CELL_SIZE / 2;
                const centerY = y + CELL_SIZE / 2;

                if (index === 0) {
                    // 머리 그리기
                    drawSnakeHead(x, y, centerX, centerY);
                } else if (index === snake.length - 1) {
                    // 꼬리 그리기
                    drawSnakeTail(x, y, index);
                } else {
                    // 몸통 그리기 (비늘 패턴)
                    drawSnakeBody(x, y, index);
                }
            });
        }

        // 뱀 머리 그리기
        function drawSnakeHead(x, y, centerX, centerY) {
            // 머리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#2ecc71');
            gradient.addColorStop(1, '#27ae60');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 머리 윤곽선
            ctx.strokeStyle = '#1e8449';
            ctx.lineWidth = 2;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 눈 그리기 (방향에 따라 위치 변경)
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 4;

            if (direction.x === 1) { // 오른쪽
                // 오른쪽 눈
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) { // 왼쪽
                // 왼쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) { // 위
                // 위쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) { // 아래
                // 아래쪽 눈
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset, eyeSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // 눈동자
            ctx.fillStyle = '#000';
            if (direction.x === 1) {
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset + 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.x === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY - eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset - 1, centerY + eyeOffset, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === -1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY - eyeOffset - 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            } else if (direction.y === 1) {
                ctx.beginPath();
                ctx.arc(centerX - eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(centerX + eyeOffset, centerY + eyeOffset + 1, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            // 혓바닥 그리기 (머리 앞쪽)
            ctx.fillStyle = '#e74c3c';
            const tongueLength = 6;
            const tongueX = centerX + direction.x * (CELL_SIZE / 2 + tongueLength);
            const tongueY = centerY + direction.y * (CELL_SIZE / 2 + tongueLength);
            
            ctx.beginPath();
            ctx.moveTo(centerX + direction.x * CELL_SIZE / 2, centerY + direction.y * CELL_SIZE / 2);
            ctx.lineTo(tongueX - 2, tongueY);
            ctx.lineTo(tongueX, tongueY - 1);
            ctx.lineTo(tongueX + 2, tongueY);
            ctx.closePath();
            ctx.fill();
        }

        // 뱀 몸통 그리기 (비늘 패턴)
        function drawSnakeBody(x, y, index) {
            // 몸통 배경
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 비늘 패턴 그리기
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            
            // 비늘 윤곽선
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            
            // 비늘 내부 패턴
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 0.5;
            
            // 대각선 비늘 패턴
            const offset = (index % 2) * 2;
            ctx.beginPath();
            ctx.moveTo(x + 2 + offset, y + CELL_SIZE - 2);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2 - offset, y + 2);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 2, y + 2 + offset);
            ctx.lineTo(x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            ctx.lineTo(x + CELL_SIZE - 2, y + CELL_SIZE - 2 - offset);
            ctx.stroke();
        }

        // 뱀 꼬리 그리기
        function drawSnakeTail(x, y, index) {
            const centerX = x + CELL_SIZE / 2;
            const centerY = y + CELL_SIZE / 2;
            
            // 꼬리 방향 계산 (이전 세그먼트로부터)
            const prevSegment = snake[index - 1];
            const tailDirection = {
                x: prevSegment.x - snake[index].x,
                y: prevSegment.y - snake[index].y
            };

            // 꼬리 배경 (그라데이션)
            const gradient = ctx.createLinearGradient(x, y, x + CELL_SIZE, y + CELL_SIZE);
            gradient.addColorStop(0, '#45b7aa');
            gradient.addColorStop(1, '#3a9d8f');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 윤곽선
            ctx.strokeStyle = '#2d7d6f';
            ctx.lineWidth = 1;
            ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // 꼬리 끝 부분 (뾰족하게)
            ctx.fillStyle = '#3a9d8f';
            ctx.beginPath();
            
            if (tailDirection.x === 1) { // 왼쪽으로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.x === -1) { // 오른쪽으로 향하는 꼬리
                ctx.moveTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE / 2, centerY);
                ctx.closePath();
            } else if (tailDirection.y === 1) { // 위로 향하는 꼬리
                ctx.moveTo(x + 1, y + 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            } else if (tailDirection.y === -1) { // 아래로 향하는 꼬리
                ctx.moveTo(x + 1, y + CELL_SIZE - 1);
                ctx.lineTo(x + CELL_SIZE - 1, y + CELL_SIZE - 1);
                ctx.lineTo(centerX, y + CELL_SIZE / 2);
                ctx.closePath();
            }
            
            ctx.fill();
            ctx.stroke();
        }

        // 사과 그리기
        function drawApple(centerX, centerY) {
            const radius = CELL_SIZE / 2 - 2;
            
            // 사과 본체 (빨간색)
            const gradient = ctx.createRadialGradient(
                centerX - radius * 0.3,
                centerY - radius * 0.3,
                0,
                centerX,
                centerY,
                radius
            );
            gradient.addColorStop(0, '#ff4757');
            gradient.addColorStop(0.7, '#ee5a6f');
            gradient.addColorStop(1, '#c44569');
            
            ctx.fillStyle = gradient;
            ctx.beginPath();
            // 사과 모양 (위쪽이 약간 들어간 형태)
            ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
            ctx.fill();
            
            // 사과 하단 부분 (약간 들어간 부분)
            ctx.fillStyle = '#c44569';
            ctx.beginPath();
            ctx.arc(centerX, centerY + radius * 0.3, radius * 0.4, 0, Math.PI, true);
            ctx.fill();
            
            // 사과 윤곽선
            ctx.strokeStyle = '#a8324f';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
            ctx.stroke();
            
            // 사과 줄기 (위쪽)
            ctx.fillStyle = '#8b4513';
            ctx.beginPath();
            ctx.moveTo(centerX, centerY - radius);
            ctx.lineTo(centerX - 2, centerY - radius - 3);
            ctx.lineTo(centerX + 2, centerY - radius - 3);
            ctx.closePath();
            ctx.fill();
            
            // 사과 잎 (줄기 옆)
            ctx.fillStyle = '#2ed573';
            ctx.beginPath();
            ctx.ellipse(centerX - 3, centerY - radius - 2, 3, 2, -0.5, 0, Math.PI * 2);
            ctx.fill();
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', init);

        
    </script>
</body>
</html>


```


린터 오류 확인 중입니다.



완료했습니다.

## 변경 사항

### 1. 배경색 변경
- 보라색 그라데이션 → 초록색 그라데이션으로 변경
- `#11998e`(청록)에서 `#38ef7d`(밝은 초록)로 그라데이션 적용

### 2. 먹이를 사과 모양으로 변경
- 빨간색 원형 → 빨간 사과 모양으로 변경
- 사과 특징:
  - 빨간색 그라데이션 (밝은 빨강 → 진한 빨강)
  - 하단 약간 들어간 형태
  - 위쪽 갈색 줄기
  - 줄기 옆 초록색 잎
  - 윤곽선으로 형태 강조

게임에서 먹이가 빨간 사과로 표시되고, 배경은 초록색 계열로 변경되었습니다.

---

**User**

된거야?

---

**Cursor**


파일을 확인해 변경 사항이 제대로 적용되었는지 확인 중입니다.



네, 적용되었습니다.

확인 결과:

1. **배경색 변경**: 보라색 → 초록색 그라데이션 (`#11998e` → `#38ef7d`)

2. **사과 그리기 함수 추가**: `drawApple()` 함수가 구현되어 있고, 게임에서 호출됩니다.

3. **사과 특징**:
   - 빨간색 그라데이션 본체
   - 하단 약간 들어간 형태
   - 갈색 줄기
   - 초록색 잎

`snake.html` 파일을 브라우저에서 열면 배경이 초록색이고, 먹이가 빨간 사과 모양으로 표시됩니다.

---

**User**

/git-custome 

--- Cursor Command: git-custome.md ---
# git-custome

git add .

git commit -m "git commit"

git push origin main
This command will be available in chat with /git-custome

--- End Command ---

---

**Cursor**


`/git-custome` 커맨드를 실행할까요? 이 커맨드는 다음을 수행합니다:
1. `git add .` - 모든 변경사항 스테이징
2. `git commit -m "git commit"` - 커밋
3. `git push origin main` - 원격 저장소에 푸시

실행할까요?

---

**User**

go

---

**Cursor**


git 커맨드 실행 중입니다.



완료했습니다.

다음 git 작업을 실행했습니다:

1. `git add .` - 모든 변경사항 스테이징 완료
2. `git commit -m "git commit"` - 커밋 완료 (커밋 해시: 94502f4)
3. `git push origin main` - 원격 저장소에 푸시 완료

변경사항이 원격 저장소에 반영되었습니다.

