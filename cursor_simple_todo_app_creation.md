# Simple todo app creation
_Exported on 11/27/2025 at 12:17:20 GMT+9 from Cursor (2.1.36)_

---

**User**

HTML, CSS, JavaScript만 사용해서 간단한 TODO 앱을 만들어줘. 



단일 HTML 파일로 파일명은 todo.html로 생성해.



목표 기능은 다음과 같아: 

- TODO 항목 추가 

- 완료 체크 및 해제 

- TODO 삭제



조건: 

- 로그인 기능은 아주 간단하게 구현해줘 (예: 사용자 이름 입력 후 저장된 TODO만 보여주기) 

- 기능과 UI는 최대한 단순하게 구성해줘 

- 전체 프로젝트 구조 (HTML, CSS, JS 파일 구성)도 함께 알려줘

---

**Cursor**


단일 HTML 파일로 간단한 TODO 앱을 생성 중입니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>간단한 TODO 앱</title>
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

        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 500px;
            padding: 30px;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }

        .login-section {
            margin-bottom: 20px;
        }

        .login-section input {
            width: 70%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }

        .login-section button {
            width: 28%;
            padding: 10px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin-left: 2%;
        }

        .login-section button:hover {
            background: #5568d3;
        }

        .user-info {
            margin-bottom: 15px;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .user-info span {
            color: #333;
            font-weight: bold;
        }

        .user-info button {
            padding: 5px 15px;
            background: #e74c3c;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }

        .user-info button:hover {
            background: #c0392b;
        }

        .todo-form {
            display: flex;
            margin-bottom: 20px;
        }

        .todo-form input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }

        .todo-form input:focus {
            outline: none;
            border-color: #667eea;
        }

        .todo-form button {
            padding: 12px 20px;
            margin-left: 10px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }

        .todo-form button:hover {
            background: #5568d3;
        }

        .todo-list {
            list-style: none;
        }

        .todo-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 10px;
            background: #f9f9f9;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }

        .todo-item.completed {
            opacity: 0.6;
            border-left-color: #27ae60;
        }

        .todo-item.completed .todo-text {
            text-decoration: line-through;
            color: #999;
        }

        .todo-checkbox {
            margin-right: 12px;
            width: 20px;
            height: 20px;
            cursor: pointer;
        }

        .todo-text {
            flex: 1;
            color: #333;
            font-size: 14px;
        }

        .todo-delete {
            padding: 6px 12px;
            background: #e74c3c;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }

        .todo-delete:hover {
            background: #c0392b;
        }

        .empty-message {
            text-align: center;
            color: #999;
            padding: 40px;
            font-style: italic;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 TODO 앱</h1>
        
        <!-- 로그인 섹션 -->
        <div id="loginSection" class="login-section">
            <input type="text" id="usernameInput" placeholder="사용자 이름을 입력하세요" />
            <button onclick="login()">로그인</button>
        </div>

        <!-- 사용자 정보 및 로그아웃 -->
        <div id="userInfo" class="user-info hidden">
            <span>안녕하세요, <strong id="currentUser"></strong>님!</span>
            <button onclick="logout()">로그아웃</button>
        </div>

        <!-- TODO 입력 폼 -->
        <div id="todoSection" class="hidden">
            <div class="todo-form">
                <input type="text" id="todoInput" placeholder="새로운 TODO를 입력하세요" />
                <button onclick="addTodo()">추가</button>
            </div>

            <!-- TODO 리스트 -->
            <ul id="todoList" class="todo-list"></ul>
        </div>
    </div>

    <script>
        // 현재 사용자 정보
        let currentUser = localStorage.getItem('currentUser');

        // 페이지 로드 시 초기화
        window.onload = function() {
            if (currentUser) {
                showTodoSection(currentUser);
            } else {
                showLoginSection();
            }
        };

        // 로그인 함수
        function login() {
            const username = document.getElementById('usernameInput').value.trim();
            if (username === '') {
                alert('사용자 이름을 입력해주세요.');
                return;
            }
            currentUser = username;
            localStorage.setItem('currentUser', username);
            showTodoSection(username);
        }

        // 로그아웃 함수
        function logout() {
            currentUser = null;
            localStorage.removeItem('currentUser');
            document.getElementById('usernameInput').value = '';
            showLoginSection();
        }

        // 로그인 섹션 표시
        function showLoginSection() {
            document.getElementById('loginSection').classList.remove('hidden');
            document.getElementById('userInfo').classList.add('hidden');
            document.getElementById('todoSection').classList.add('hidden');
        }

        // TODO 섹션 표시
        function showTodoSection(username) {
            document.getElementById('loginSection').classList.add('hidden');
            document.getElementById('userInfo').classList.remove('hidden');
            document.getElementById('todoSection').classList.remove('hidden');
            document.getElementById('currentUser').textContent = username;
            loadTodos();
        }

        // TODO 추가 함수
        function addTodo() {
            const todoInput = document.getElementById('todoInput');
            const todoText = todoInput.value.trim();
            
            if (todoText === '') {
                alert('TODO 내용을 입력해주세요.');
                return;
            }

            const todos = getTodos();
            const newTodo = {
                id: Date.now(),
                text: todoText,
                completed: false
            };
            todos.push(newTodo);
            saveTodos(todos);
            todoInput.value = '';
            renderTodos();
        }

        // TODO 완료/미완료 토글
        function toggleTodo(id) {
            const todos = getTodos();
            const todo = todos.find(t => t.id === id);
            if (todo) {
                todo.completed = !todo.completed;
                saveTodos(todos);
                renderTodos();
            }
        }

        // TODO 삭제 함수
        function deleteTodo(id) {
            if (confirm('이 TODO를 삭제하시겠습니까?')) {
                const todos = getTodos();
                const filteredTodos = todos.filter(t => t.id !== id);
                saveTodos(filteredTodos);
                renderTodos();
            }
        }

        // 로컬 스토리지에서 TODO 가져오기
        function getTodos() {
            if (!currentUser) return [];
            const todosJson = localStorage.getItem(`todos_${currentUser}`);
            return todosJson ? JSON.parse(todosJson) : [];
        }

        // 로컬 스토리지에 TODO 저장
        function saveTodos(todos) {
            if (!currentUser) return;
            localStorage.setItem(`todos_${currentUser}`, JSON.stringify(todos));
        }

        // TODO 리스트 렌더링
        function renderTodos() {
            const todoList = document.getElementById('todoList');
            const todos = getTodos();

            if (todos.length === 0) {
                todoList.innerHTML = '<li class="empty-message">TODO가 없습니다. 새로운 TODO를 추가해보세요!</li>';
                return;
            }

            todoList.innerHTML = todos.map(todo => `
                <li class="todo-item ${todo.completed ? 'completed' : ''}">
                    <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''} 
                           onchange="toggleTodo(${todo.id})" />
                    <span class="todo-text">${escapeHtml(todo.text)}</span>
                    <button class="todo-delete" onclick="deleteTodo(${todo.id})">삭제</button>
                </li>
            `).join('');
        }

        // TODO 로드 함수
        function loadTodos() {
            renderTodos();
        }

        // HTML 이스케이프 함수 (XSS 방지)
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Enter 키로 TODO 추가
        document.addEventListener('DOMContentLoaded', function() {
            const todoInput = document.getElementById('todoInput');
            const usernameInput = document.getElementById('usernameInput');

            if (todoInput) {
                todoInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        addTodo();
                    }
                });
            }

            if (usernameInput) {
                usernameInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        login();
                    }
                });
            }
        });
    </script>
</body>
</html>

```


단일 HTML 파일로 TODO 앱을 생성했습니다.

## 생성된 파일

- **todo.html** - HTML, CSS, JavaScript가 모두 포함된 단일 파일

## 프로젝트 구조

```
vul_checker/
└── todo.html  (단일 파일 - HTML, CSS, JavaScript 모두 포함)
```

## 주요 기능

1. 로그인: 사용자 이름 입력 후 해당 사용자의 TODO만 표시
2. TODO 추가: 입력 후 추가 버튼 또는 Enter로 추가
3. 완료 체크: 체크박스로 완료/미완료 토글
4. TODO 삭제: 삭제 버튼으로 항목 삭제
5. 로그아웃: 다른 사용자로 전환 가능

## 기술적 특징

- 로컬 스토리지 사용: 사용자별 TODO를 브라우저에 저장
- XSS 방지: HTML 이스케이프 처리
- 반응형 디자인: 모바일과 데스크톱에서 동작
- Enter 키 지원: 입력 필드에서 Enter로 추가/로그인

## 사용 방법

1. `todo.html` 파일을 브라우저에서 열기
2. 사용자 이름 입력 후 로그인
3. TODO 항목 추가, 완료 체크, 삭제 사용

브라우저에서 `todo.html`을 열어 바로 사용할 수 있습니다.

```plaintext
vul_checker/
└── todo.html  (단일 파일 - HTML, CSS, JavaScript 모두 포함)
```

---

**User**

배경색을 보라색 말고 스위스의 산 사진으로 해줄래

---

**Cursor**


배경을 스위스 산 이미지로 변경 중입니다.



배경을 스위스 산 이미지로 변경 중입니다.


```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>간단한 TODO 앱</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80') center center / cover no-repeat fixed;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 500px;
            padding: 30px;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }

        .login-section {
            margin-bottom: 20px;
        }

        .login-section input {
            width: 70%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }

        .login-section button {
            width: 28%;
            padding: 10px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin-left: 2%;
        }

        .login-section button:hover {
            background: #5568d3;
        }

        .user-info {
            margin-bottom: 15px;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .user-info span {
            color: #333;
            font-weight: bold;
        }

        .user-info button {
            padding: 5px 15px;
            background: #e74c3c;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }

        .user-info button:hover {
            background: #c0392b;
        }

        .todo-form {
            display: flex;
            margin-bottom: 20px;
        }

        .todo-form input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }

        .todo-form input:focus {
            outline: none;
            border-color: #667eea;
        }

        .todo-form button {
            padding: 12px 20px;
            margin-left: 10px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }

        .todo-form button:hover {
            background: #5568d3;
        }

        .todo-list {
            list-style: none;
        }

        .todo-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 10px;
            background: #f9f9f9;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }

        .todo-item.completed {
            opacity: 0.6;
            border-left-color: #27ae60;
        }

        .todo-item.completed .todo-text {
            text-decoration: line-through;
            color: #999;
        }

        .todo-checkbox {
            margin-right: 12px;
            width: 20px;
            height: 20px;
            cursor: pointer;
        }

        .todo-text {
            flex: 1;
            color: #333;
            font-size: 14px;
        }

        .todo-delete {
            padding: 6px 12px;
            background: #e74c3c;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }

        .todo-delete:hover {
            background: #c0392b;
        }

        .empty-message {
            text-align: center;
            color: #999;
            padding: 40px;
            font-style: italic;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 TODO 앱</h1>
        
        <!-- 로그인 섹션 -->
        <div id="loginSection" class="login-section">
            <input type="text" id="usernameInput" placeholder="사용자 이름을 입력하세요" />
            <button onclick="login()">로그인</button>
        </div>

        <!-- 사용자 정보 및 로그아웃 -->
        <div id="userInfo" class="user-info hidden">
            <span>안녕하세요, <strong id="currentUser"></strong>님!</span>
            <button onclick="logout()">로그아웃</button>
        </div>

        <!-- TODO 입력 폼 -->
        <div id="todoSection" class="hidden">
            <div class="todo-form">
                <input type="text" id="todoInput" placeholder="새로운 TODO를 입력하세요" />
                <button onclick="addTodo()">추가</button>
            </div>

            <!-- TODO 리스트 -->
            <ul id="todoList" class="todo-list"></ul>
        </div>
    </div>

    <script>
        // 현재 사용자 정보
        let currentUser = localStorage.getItem('currentUser');

        // 페이지 로드 시 초기화
        window.onload = function() {
            if (currentUser) {
                showTodoSection(currentUser);
            } else {
                showLoginSection();
            }
        };

        // 로그인 함수
        function login() {
            const username = document.getElementById('usernameInput').value.trim();
            if (username === '') {
                alert('사용자 이름을 입력해주세요.');
                return;
            }
            currentUser = username;
            localStorage.setItem('currentUser', username);
            showTodoSection(username);
        }

        // 로그아웃 함수
        function logout() {
            currentUser = null;
            localStorage.removeItem('currentUser');
            document.getElementById('usernameInput').value = '';
            showLoginSection();
        }

        // 로그인 섹션 표시
        function showLoginSection() {
            document.getElementById('loginSection').classList.remove('hidden');
            document.getElementById('userInfo').classList.add('hidden');
            document.getElementById('todoSection').classList.add('hidden');
        }

        // TODO 섹션 표시
        function showTodoSection(username) {
            document.getElementById('loginSection').classList.add('hidden');
            document.getElementById('userInfo').classList.remove('hidden');
            document.getElementById('todoSection').classList.remove('hidden');
            document.getElementById('currentUser').textContent = username;
            loadTodos();
        }

        // TODO 추가 함수
        function addTodo() {
            const todoInput = document.getElementById('todoInput');
            const todoText = todoInput.value.trim();
            
            if (todoText === '') {
                alert('TODO 내용을 입력해주세요.');
                return;
            }

            const todos = getTodos();
            const newTodo = {
                id: Date.now(),
                text: todoText,
                completed: false
            };
            todos.push(newTodo);
            saveTodos(todos);
            todoInput.value = '';
            renderTodos();
        }

        // TODO 완료/미완료 토글
        function toggleTodo(id) {
            const todos = getTodos();
            const todo = todos.find(t => t.id === id);
            if (todo) {
                todo.completed = !todo.completed;
                saveTodos(todos);
                renderTodos();
            }
        }

        // TODO 삭제 함수
        function deleteTodo(id) {
            if (confirm('이 TODO를 삭제하시겠습니까?')) {
                const todos = getTodos();
                const filteredTodos = todos.filter(t => t.id !== id);
                saveTodos(filteredTodos);
                renderTodos();
            }
        }

        // 로컬 스토리지에서 TODO 가져오기
        function getTodos() {
            if (!currentUser) return [];
            const todosJson = localStorage.getItem(`todos_${currentUser}`);
            return todosJson ? JSON.parse(todosJson) : [];
        }

        // 로컬 스토리지에 TODO 저장
        function saveTodos(todos) {
            if (!currentUser) return;
            localStorage.setItem(`todos_${currentUser}`, JSON.stringify(todos));
        }

        // TODO 리스트 렌더링
        function renderTodos() {
            const todoList = document.getElementById('todoList');
            const todos = getTodos();

            if (todos.length === 0) {
                todoList.innerHTML = '<li class="empty-message">TODO가 없습니다. 새로운 TODO를 추가해보세요!</li>';
                return;
            }

            todoList.innerHTML = todos.map(todo => `
                <li class="todo-item ${todo.completed ? 'completed' : ''}">
                    <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''} 
                           onchange="toggleTodo(${todo.id})" />
                    <span class="todo-text">${escapeHtml(todo.text)}</span>
                    <button class="todo-delete" onclick="deleteTodo(${todo.id})">삭제</button>
                </li>
            `).join('');
        }

        // TODO 로드 함수
        function loadTodos() {
            renderTodos();
        }

        // HTML 이스케이프 함수 (XSS 방지)
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Enter 키로 TODO 추가
        document.addEventListener('DOMContentLoaded', function() {
            const todoInput = document.getElementById('todoInput');
            const usernameInput = document.getElementById('usernameInput');

            if (todoInput) {
                todoInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        addTodo();
                    }
                });
            }

            if (usernameInput) {
                usernameInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        login();
                    }
                });
            }
        });
    </script>
</body>
</html>


```


배경을 스위스 산 이미지로 변경했습니다.

변경 사항:
- 보라색 그라데이션 배경을 스위스 알프스 산 이미지로 교체
- 이미지는 화면 전체를 덮도록 설정 (`cover`, `fixed`)

브라우저에서 `todo.html`을 열면 스위스 산 배경이 표시됩니다.

