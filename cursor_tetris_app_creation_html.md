# 단일 HTML 파일로 테트리스 게임 구현
_Exported on 11/27/2025 at 12:17:35 GMT+9 from Cursor (2.1.36)_

---

**User**

HTML, CSS, JavaScript만을 사용하여 완전히 작동하는 테트리스 게임을 개발해줘.



단일 HTML 파일로 파일명은 tetris.html로 생성해



### 기술 요구사항

- 바닐라 JavaScript (프레임워크 없음)

- CSS Grid 또는 Canvas를 활용한 게임 보드

- 단일 HTML 파일로 구성 (인라인 CSS/JS 포함)



### 핵심 구성요소



#### 1. 데이터 모델

- 게임보드: 10x20 그리드 (2차원 배열)

- 테트로미노: 7가지 블록 타입 (I, O, T, S, Z, J, L)

- 플레이어 상태: 점수, 레벨, 라인 클리어 수

- 현재 블록: 위치(x, y), 회전 상태, 타입

- 다음 블록: 미리보기용



#### 2. 게임 로직

- 블록 생성: 랜덤 테트로미노 생성 및 다음 블록 큐

- 블록 이동: 좌/우 이동, 아래로 떨어뜨리기

- 회전: 시계방향/반시계방향 회전 (벽 킥 포함)

- 충돌 감지: 벽, 바닥, 기존 블록과의 충돌

- 라인 클리어: 완성된 라인 제거 및 점수 계산

- 게임 오버: 새 블록이 생성될 수 없을 때



#### 3. 컨트롤

- 화살표 키: 좌/우 이동, 아래로 빠르게 떨어뜨리기

- 스페이스바: 즉시 바닥까지 떨어뜨리기

- 위 화살표/Z키: 회전



#### 4. UI 구성

- 게임 보드 (10x20 그리드)

- 점수 표시

- 레벨 표시

- 다음 블록 미리보기

- 게임 오버/일시정지 상태 표시



#### 5. 게임 피처

- 레벨별 속도 증가

- 라인 클리어에 따른 점수 시스템

- 부드러운 애니메이션

- 반응형 디자인



### 구현 세부사항

- 게임 루프는 requestAnimationFrame 사용

- 모든 테트로미노 형태를 배열로 정의

- 충돌 감지 함수 구현

- 키보드 이벤트 리스너 설정

- 게임 상태 관리 (playing, paused, gameOver)



### 코드 구조

- HTML: 기본 구조 및 게임 컨테이너

- CSS: 게임 보드 스타일링 및 반응형 디자인

- JavaScript: 게임 로직, 이벤트 핸들링, 렌더링



완전히 작동하는 테트리스 게임을 단일 HTML 파일로 구현해줘.

모든 코드는 주석과 함께 제공하고, 즉시 브라우저에서 실행 가능하도록 작성해줘.

---

**Cursor**


단일 HTML 파일로 테트리스 게임 구현 중입니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let dropInterval = 1000;  // 밀리초 단위
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                dropInterval = Math.max(100, 1000 - (level - 1) * 100);
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            if (e.key === 'p' || e.key === 'P') {
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
    </script>
</body>
</html>
```


테트리스 게임을 단일 HTML 파일(`tetris.html`)로 구현했습니다. 린터 오류 확인 중입니다.



완료했습니다. `tetris.html` 파일을 생성했습니다.

## 구현된 기능

### 핵심 기능
- 7가지 테트로미노 (I, O, T, S, Z, J, L)
- 10x20 게임 보드 (Canvas 기반)
- 충돌 감지 (벽, 바닥, 기존 블록)
- 벽 킥 회전 시스템
- 라인 클리어 및 점수 계산
- 레벨 시스템 (10줄마다 레벨 증가, 속도 증가)
- 다음 블록 미리보기

### 조작법
- ← → : 좌우 이동
- ↓ : 빠르게 떨어뜨리기
- ↑ / Z : 시계방향 회전
- 스페이스바 : 즉시 바닥까지 떨어뜨리기
- P : 일시정지/재개

### 게임 시스템
- 점수: 라인 클리어 시 점수 획득 (1줄=100, 2줄=300, 3줄=500, 4줄=800) × 레벨
- 레벨: 10줄마다 레벨 증가, 속도 증가
- 보너스: 빠른 낙하(+1점), 하드 드롭(+2점)

### UI/UX
- 반응형 디자인
- 게임 오버 화면 및 재시작 버튼
- 일시정지 기능
- 실시간 점수/레벨/라인 표시

브라우저에서 `tetris.html`을 열면 바로 플레이할 수 있습니다. 모든 코드에 주석이 포함되어 있습니다.

---

**User**

일시정지 기능을 만들어주고 속도를 2배 3배 빠르게 하는 기능도 넣어줘

---

**Cursor**


일시정지 기능을 개선하고 속도 조절(2배/3배) 기능을 추가 중입니다.



일시정지 기능을 개선하고 속도 조절(2배/3배) 기능을 추가 중입니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let dropInterval = 1000;  // 밀리초 단위
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                dropInterval = Math.max(100, 1000 - (level - 1) * 100);
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            if (e.key === 'p' || e.key === 'P') {
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
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
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                    <li>1 / 2 / 3 : 속도 조절</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let dropInterval = 1000;  // 밀리초 단위
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                dropInterval = Math.max(100, 1000 - (level - 1) * 100);
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            if (e.key === 'p' || e.key === 'P') {
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
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
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                    <li>1 / 2 / 3 : 속도 조절</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let baseDropInterval = 1000;  // 기본 낙하 간격 (밀리초 단위)
        let dropInterval = 1000;  // 현재 낙하 간격 (속도 배율 적용)
        let speedMultiplier = 1;  // 속도 배율 (1x, 2x, 3x)
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                dropInterval = Math.max(100, 1000 - (level - 1) * 100);
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            if (e.key === 'p' || e.key === 'P') {
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
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
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                    <li>1 / 2 / 3 : 속도 조절</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let baseDropInterval = 1000;  // 기본 낙하 간격 (밀리초 단위)
        let dropInterval = 1000;  // 현재 낙하 간격 (속도 배율 적용)
        let speedMultiplier = 1;  // 속도 배율 (1x, 2x, 3x)
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                dropInterval = Math.max(100, 1000 - (level - 1) * 100);
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
            document.getElementById('speed').textContent = speedMultiplier + 'x';
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            if (e.key === 'p' || e.key === 'P') {
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
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
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                    <li>1 / 2 / 3 : 속도 조절</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let baseDropInterval = 1000;  // 기본 낙하 간격 (밀리초 단위)
        let dropInterval = 1000;  // 현재 낙하 간격 (속도 배율 적용)
        let speedMultiplier = 1;  // 속도 배율 (1x, 2x, 3x)
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                baseDropInterval = Math.max(100, 1000 - (level - 1) * 100);
                dropInterval = baseDropInterval / speedMultiplier;
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
            document.getElementById('speed').textContent = speedMultiplier + 'x';
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            if (e.key === 'p' || e.key === 'P') {
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
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
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                    <li>1 / 2 / 3 : 속도 조절</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let baseDropInterval = 1000;  // 기본 낙하 간격 (밀리초 단위)
        let dropInterval = 1000;  // 현재 낙하 간격 (속도 배율 적용)
        let speedMultiplier = 1;  // 속도 배율 (1x, 2x, 3x)
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                baseDropInterval = Math.max(100, 1000 - (level - 1) * 100);
                dropInterval = baseDropInterval / speedMultiplier;
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
            document.getElementById('speed').textContent = speedMultiplier + 'x';
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 속도 조절 함수
        // ============================================
        function setSpeed(multiplier) {
            speedMultiplier = multiplier;
            dropInterval = baseDropInterval / speedMultiplier;
            updateUI();
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            // 일시정지 토글
            if (e.key === 'p' || e.key === 'P') {
                e.preventDefault();
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            // 속도 조절 (1x, 2x, 3x)
            if (e.key === '1' || e.key === '2' || e.key === '3') {
                const multiplier = parseInt(e.key);
                setSpeed(multiplier);
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
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
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                    <li>1 / 2 / 3 : 속도 조절</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let baseDropInterval = 1000;  // 기본 낙하 간격 (밀리초 단위)
        let dropInterval = 1000;  // 현재 낙하 간격 (속도 배율 적용)
        let speedMultiplier = 1;  // 속도 배율 (1x, 2x, 3x)
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                baseDropInterval = Math.max(100, 1000 - (level - 1) * 100);
                dropInterval = baseDropInterval / speedMultiplier;
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
            document.getElementById('speed').textContent = speedMultiplier + 'x';
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 속도 조절 함수
        // ============================================
        function setSpeed(multiplier) {
            speedMultiplier = multiplier;
            dropInterval = baseDropInterval / speedMultiplier;
            updateUI();
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            // 일시정지 토글
            if (e.key === 'p' || e.key === 'P') {
                e.preventDefault();
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            // 속도 조절 (1x, 2x, 3x)
            if (e.key === '1' || e.key === '2' || e.key === '3') {
                const multiplier = parseInt(e.key);
                setSpeed(multiplier);
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            speedMultiplier = 1;
            baseDropInterval = 1000;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
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
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
                <p style="margin-top: 10px; font-size: 14px; opacity: 0.8;">속도: <span id="pauseSpeed">1x</span></p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                    <li>1 / 2 / 3 : 속도 조절</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let baseDropInterval = 1000;  // 기본 낙하 간격 (밀리초 단위)
        let dropInterval = 1000;  // 현재 낙하 간격 (속도 배율 적용)
        let speedMultiplier = 1;  // 속도 배율 (1x, 2x, 3x)
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                baseDropInterval = Math.max(100, 1000 - (level - 1) * 100);
                dropInterval = baseDropInterval / speedMultiplier;
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
            document.getElementById('speed').textContent = speedMultiplier + 'x';
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 속도 조절 함수
        // ============================================
        function setSpeed(multiplier) {
            speedMultiplier = multiplier;
            dropInterval = baseDropInterval / speedMultiplier;
            updateUI();
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            // 일시정지 토글
            if (e.key === 'p' || e.key === 'P') {
                e.preventDefault();
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            // 속도 조절 (1x, 2x, 3x)
            if (e.key === '1' || e.key === '2' || e.key === '3') {
                const multiplier = parseInt(e.key);
                setSpeed(multiplier);
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            speedMultiplier = 1;
            baseDropInterval = 1000;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
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
    <title>테트리스 게임</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .game-container {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .game-board-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        canvas {
            border: 3px solid #333;
            background: #000;
            display: block;
        }

        .info-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 200px;
        }

        .info-box {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .info-box h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 18px;
        }

        .info-box p {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .next-block {
            width: 120px;
            height: 120px;
            background: #000;
            border: 2px solid #333;
            border-radius: 5px;
        }

        .controls {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #333;
        }

        .controls h3 {
            margin-bottom: 10px;
            color: #333;
        }

        .controls ul {
            list-style: none;
            font-size: 14px;
            line-height: 1.8;
        }

        .controls li {
            color: #555;
        }

        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }

        .game-over.show {
            display: block;
        }

        .game-over h2 {
            margin-bottom: 20px;
            font-size: 32px;
        }

        .game-over button {
            padding: 12px 30px;
            font-size: 18px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }

        .game-over button:hover {
            background: #764ba2;
        }

        .pause-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .pause-overlay.show {
            display: block;
        }

        @media (max-width: 768px) {
            .game-container {
                flex-direction: column;
            }

            canvas {
                width: 100%;
                max-width: 300px;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-board-container">
            <canvas id="gameBoard" width="300" height="600"></canvas>
            <div class="game-over" id="gameOver">
                <h2>게임 오버!</h2>
                <p>최종 점수: <span id="finalScore">0</span></p>
                <button onclick="restartGame()">다시 시작</button>
            </div>
            <div class="pause-overlay" id="pauseOverlay">
                <h2>일시정지</h2>
                <p>P 키를 눌러 계속</p>
                <p style="margin-top: 10px; font-size: 14px; opacity: 0.8;">속도: <span id="pauseSpeed">1x</span></p>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>점수</h3>
                <p id="score">0</p>
            </div>
            
            <div class="info-box">
                <h3>레벨</h3>
                <p id="level">1</p>
            </div>
            
            <div class="info-box">
                <h3>라인 클리어</h3>
                <p id="lines">0</p>
            </div>
            
            <div class="info-box">
                <h3>속도</h3>
                <p id="speed">1x</p>
            </div>
            
            <div class="info-box">
                <h3>다음 블록</h3>
                <canvas class="next-block" id="nextBlock" width="120" height="120"></canvas>
            </div>
            
            <div class="controls">
                <h3>조작법</h3>
                <ul>
                    <li>← → : 이동</li>
                    <li>↓ : 빠르게 떨어뜨리기</li>
                    <li>↑ / Z : 회전</li>
                    <li>스페이스바 : 즉시 낙하</li>
                    <li>P : 일시정지</li>
                    <li>1 / 2 / 3 : 속도 조절</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // ============================================
        // 게임 상수 및 설정
        // ============================================
        const COLS = 10;  // 게임 보드 열 수
        const ROWS = 20;  // 게임 보드 행 수
        const BLOCK_SIZE = 30;  // 블록 크기 (픽셀)
        const COLORS = [
            null,
            '#00f0f0',  // I - 청록색
            '#f0f000',  // O - 노란색
            '#a000f0',  // T - 보라색
            '#00f000',  // S - 초록색
            '#f00000',  // Z - 빨간색
            '#0000f0',  // J - 파란색
            '#f0a000'   // L - 주황색
        ];

        // ============================================
        // 테트로미노 정의 (각 블록의 회전 상태)
        // ============================================
        const SHAPES = {
            I: [
                [[0,0,0,0],
                 [1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0]],
                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
            ],
            O: [
                [[1,1],
                 [1,1]]
            ],
            T: [
                [[0,1,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,1,0]],
                [[0,1,0],
                 [1,1,0],
                 [0,1,0]]
            ],
            S: [
                [[0,1,1],
                 [1,1,0],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,1],
                 [0,0,1]]
            ],
            Z: [
                [[1,1,0],
                 [0,1,1],
                 [0,0,0]],
                [[0,0,1],
                 [0,1,1],
                 [0,1,0]]
            ],
            J: [
                [[1,0,0],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,1],
                 [0,1,0],
                 [0,1,0]],
                [[0,0,0],
                 [1,1,1],
                 [0,0,1]],
                [[0,1,0],
                 [0,1,0],
                 [1,1,0]]
            ],
            L: [
                [[0,0,1],
                 [1,1,1],
                 [0,0,0]],
                [[0,1,0],
                 [0,1,0],
                 [0,1,1]],
                [[0,0,0],
                 [1,1,1],
                 [1,0,0]],
                [[1,1,0],
                 [0,1,0],
                 [0,1,0]]
            ]
        };

        // ============================================
        // 게임 상태 변수
        // ============================================
        let board = [];  // 게임 보드 (2차원 배열)
        let currentPiece = null;  // 현재 블록
        let nextPiece = null;  // 다음 블록
        let score = 0;
        let level = 1;
        let lines = 0;
        let dropCounter = 0;
        let baseDropInterval = 1000;  // 기본 낙하 간격 (밀리초 단위)
        let dropInterval = 1000;  // 현재 낙하 간격 (속도 배율 적용)
        let speedMultiplier = 1;  // 속도 배율 (1x, 2x, 3x)
        let lastTime = 0;
        let gameState = 'playing';  // 'playing', 'paused', 'gameOver'
        
        // Canvas 요소
        const canvas = document.getElementById('gameBoard');
        const ctx = canvas.getContext('2d');
        const nextCanvas = document.getElementById('nextBlock');
        const nextCtx = nextCanvas.getContext('2d');

        // ============================================
        // 게임 보드 초기화
        // ============================================
        function initBoard() {
            board = Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
        }

        // ============================================
        // 블록 생성 함수
        // ============================================
        function createPiece(type) {
            const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
            const randomType = type || types[Math.floor(Math.random() * types.length)];
            const shape = SHAPES[randomType];
            
            return {
                type: randomType,
                shape: shape[0],
                rotation: 0,
                x: Math.floor(COLS / 2) - Math.floor(shape[0][0].length / 2),
                y: 0,
                color: COLORS[types.indexOf(randomType) + 1]
            };
        }

        // ============================================
        // 블록 그리기 함수
        // ============================================
        function drawBlock(ctx, x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        // ============================================
        // 게임 보드 그리기
        // ============================================
        function drawBoard() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 보드의 블록들 그리기
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    if (board[y][x]) {
                        drawBlock(ctx, x, y, COLORS[board[y][x]]);
                    }
                }
            }
            
            // 현재 블록 그리기
            if (currentPiece) {
                const shape = currentPiece.shape;
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            drawBlock(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                        }
                    }
                }
            }
        }

        // ============================================
        // 다음 블록 미리보기 그리기
        // ============================================
        function drawNextBlock() {
            nextCtx.fillStyle = '#000';
            nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
            
            if (nextPiece) {
                const shape = nextPiece.shape;
                const blockSize = 20;
                const offsetX = (nextCanvas.width - shape[0].length * blockSize) / 2;
                const offsetY = (nextCanvas.height - shape.length * blockSize) / 2;
                
                for (let y = 0; y < shape.length; y++) {
                    for (let x = 0; x < shape[y].length; x++) {
                        if (shape[y][x]) {
                            nextCtx.fillStyle = nextPiece.color;
                            nextCtx.fillRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                            nextCtx.strokeStyle = '#fff';
                            nextCtx.lineWidth = 1;
                            nextCtx.strokeRect(
                                offsetX + x * blockSize,
                                offsetY + y * blockSize,
                                blockSize,
                                blockSize
                            );
                        }
                    }
                }
            }
        }

        // ============================================
        // 충돌 감지 함수
        // ============================================
        function collide(piece, dx = 0, dy = 0, rotation = null) {
            const shape = rotation !== null ? SHAPES[piece.type][rotation] : piece.shape;
            const newX = piece.x + dx;
            const newY = piece.y + dy;
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardX = newX + x;
                        const boardY = newY + y;
                        
                        // 벽 충돌 체크
                        if (boardX < 0 || boardX >= COLS || boardY >= ROWS) {
                            return true;
                        }
                        
                        // 바닥 충돌 체크
                        if (boardY < 0) {
                            continue;
                        }
                        
                        // 기존 블록과 충돌 체크
                        if (board[boardY][boardX]) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        // ============================================
        // 블록 회전 함수
        // ============================================
        function rotatePiece(piece, direction = 1) {
            const rotations = SHAPES[piece.type];
            if (rotations.length === 1) return piece;  // O 블록은 회전 불가
            
            let newRotation = (piece.rotation + direction + rotations.length) % rotations.length;
            const newShape = rotations[newRotation];
            
            // 벽 킥: 회전 후 벽에 닿으면 위치 조정
            let offsetX = 0;
            let offsetY = 0;
            
            // 왼쪽 벽에 닿으면 오른쪽으로 이동
            if (collide({...piece, shape: newShape, rotation: newRotation}, 0, 0)) {
                if (!collide({...piece, shape: newShape, rotation: newRotation}, 1, 0)) {
                    offsetX = 1;
                } else if (!collide({...piece, shape: newShape, rotation: newRotation}, -1, 0)) {
                    offsetX = -1;
                } else {
                    return piece;  // 회전 불가
                }
            }
            
            return {
                ...piece,
                shape: newShape,
                rotation: newRotation,
                x: piece.x + offsetX
            };
        }

        // ============================================
        // 블록을 보드에 고정
        // ============================================
        function mergePiece() {
            const shape = currentPiece.shape;
            const colorIndex = COLORS.indexOf(currentPiece.color);
            
            for (let y = 0; y < shape.length; y++) {
                for (let x = 0; x < shape[y].length; x++) {
                    if (shape[y][x]) {
                        const boardY = currentPiece.y + y;
                        const boardX = currentPiece.x + x;
                        if (boardY >= 0) {
                            board[boardY][boardX] = colorIndex;
                        }
                    }
                }
            }
        }

        // ============================================
        // 완성된 라인 제거 및 점수 계산
        // ============================================
        function clearLines() {
            let linesCleared = 0;
            
            for (let y = ROWS - 1; y >= 0; y--) {
                if (board[y].every(cell => cell !== 0)) {
                    board.splice(y, 1);
                    board.unshift(Array(COLS).fill(0));
                    linesCleared++;
                    y++;  // 같은 행을 다시 체크
                }
            }
            
            if (linesCleared > 0) {
                lines += linesCleared;
                // 점수 계산: 1줄=100, 2줄=300, 3줄=500, 4줄=800
                const points = [0, 100, 300, 500, 800];
                score += points[linesCleared] * level;
                
                // 레벨 업 (10줄마다)
                level = Math.floor(lines / 10) + 1;
                baseDropInterval = Math.max(100, 1000 - (level - 1) * 100);
                dropInterval = baseDropInterval / speedMultiplier;
                
                updateUI();
            }
        }

        // ============================================
        // UI 업데이트
        // ============================================
        function updateUI() {
            document.getElementById('score').textContent = score;
            document.getElementById('level').textContent = level;
            document.getElementById('lines').textContent = lines;
            document.getElementById('speed').textContent = speedMultiplier + 'x';
        }

        // ============================================
        // 게임 오버 체크
        // ============================================
        function checkGameOver() {
            if (collide(currentPiece)) {
                gameState = 'gameOver';
                document.getElementById('finalScore').textContent = score;
                document.getElementById('gameOver').classList.add('show');
                return true;
            }
            return false;
        }

        // ============================================
        // 블록 낙하
        // ============================================
        function dropPiece() {
            if (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
            } else {
                mergePiece();
                clearLines();
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                if (checkGameOver()) {
                    return;
                }
            }
        }

        // ============================================
        // 즉시 바닥까지 떨어뜨리기
        // ============================================
        function hardDrop() {
            while (!collide(currentPiece, 0, 1)) {
                currentPiece.y++;
                score += 2;  // 하드 드롭 보너스
            }
            mergePiece();
            clearLines();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            updateUI();
            
            if (checkGameOver()) {
                return;
            }
        }

        // ============================================
        // 속도 조절 함수
        // ============================================
        function setSpeed(multiplier) {
            speedMultiplier = multiplier;
            dropInterval = baseDropInterval / speedMultiplier;
            updateUI();
        }

        // ============================================
        // 키보드 이벤트 처리
        // ============================================
        document.addEventListener('keydown', (e) => {
            if (gameState === 'gameOver') return;
            
            // 일시정지 토글
            if (e.key === 'p' || e.key === 'P') {
                e.preventDefault();
                if (gameState === 'playing') {
                    gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.add('show');
                    document.getElementById('pauseSpeed').textContent = speedMultiplier + 'x';
                } else if (gameState === 'paused') {
                    gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.remove('show');
                    lastTime = performance.now();
                }
                return;
            }
            
            // 속도 조절 (1x, 2x, 3x)
            if (e.key === '1' || e.key === '2' || e.key === '3') {
                const multiplier = parseInt(e.key);
                setSpeed(multiplier);
                return;
            }
            
            if (gameState === 'paused') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    if (!collide(currentPiece, -1, 0)) {
                        currentPiece.x--;
                    }
                    break;
                case 'ArrowRight':
                    if (!collide(currentPiece, 1, 0)) {
                        currentPiece.x++;
                    }
                    break;
                case 'ArrowDown':
                    dropPiece();
                    score += 1;  // 빠른 낙하 보너스
                    updateUI();
                    dropCounter = dropInterval;  // 타이머 리셋
                    break;
                case 'ArrowUp':
                case 'z':
                case 'Z':
                    currentPiece = rotatePiece(currentPiece, 1);
                    break;
                case ' ':
                    e.preventDefault();
                    hardDrop();
                    break;
            }
        });

        // ============================================
        // 게임 루프
        // ============================================
        function gameLoop(time = 0) {
            if (gameState === 'playing') {
                const deltaTime = time - lastTime;
                dropCounter += deltaTime;
                
                if (dropCounter > dropInterval) {
                    dropPiece();
                    dropCounter = 0;
                }
                
                lastTime = time;
            }
            
            drawBoard();
            drawNextBlock();
            requestAnimationFrame(gameLoop);
        }

        // ============================================
        // 게임 재시작
        // ============================================
        function restartGame() {
            initBoard();
            score = 0;
            level = 1;
            lines = 0;
            dropCounter = 0;
            speedMultiplier = 1;
            baseDropInterval = 1000;
            dropInterval = 1000;
            gameState = 'playing';
            currentPiece = createPiece();
            nextPiece = createPiece();
            document.getElementById('gameOver').classList.remove('show');
            document.getElementById('pauseOverlay').classList.remove('show');
            updateUI();
            lastTime = performance.now();
        }

        // ============================================
        // 게임 시작
        // ============================================
        function startGame() {
            initBoard();
            currentPiece = createPiece();
            nextPiece = createPiece();
            updateUI();
            lastTime = performance.now();
            gameLoop();
        }

        // 게임 시작
        startGame();
    </script>
</body>
</html>

```


린터 오류 확인 중입니다.



일시정지 기능을 개선하고 속도 조절 기능을 추가했습니다.

## 추가된 기능

### 1. 속도 조절 기능
- 1키: 기본 속도 (1배)
- 2키: 2배 속도
- 3키: 3배 속도
- 속도 배율은 UI에 표시됩니다
- 레벨 업 시에도 선택한 속도 배율이 유지됩니다

### 2. 일시정지 기능 개선
- P 키로 일시정지/재개
- 일시정지 화면에 현재 속도 표시
- 게임 오버 상태에서는 일시정지 불가

### 3. UI 개선
- 속도 표시 박스 추가 (1x, 2x, 3x)
- 조작법에 속도 조절 키 안내 추가

## 사용 방법

- P: 일시정지/재개
- 1: 기본 속도 (1배)
- 2: 2배 속도
- 3: 3배 속도

속도 조절은 게임 중 언제든지 가능하며, 일시정지 중에도 변경할 수 있습니다. 변경된 속도는 게임 재개 시 적용됩니다.

