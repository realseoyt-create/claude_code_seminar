# 01. 앱 기동 확인

앱이 서버에서 실행 중인지 확인하는 방법을 설명합니다.

---

## 개념: 프로세스란 무엇인가

서버에서 앱을 실행하면 **프로세스**가 하나 생깁니다. 프로세스는 "지금 이 앱이 실행 중"이라는 증거입니다. 앱이 죽으면 프로세스가 사라집니다.

`ps` 명령어는 현재 서버에서 실행 중인 모든 프로세스 목록을 보여줍니다.

---

## Java 앱 확인

### 방법 1: ps 명령어로 확인

```bash
ps aux | grep java
```

**명령어 설명:**
- `ps aux`: 모든 프로세스 목록 출력
- `|`: 앞 명령어의 출력을 뒤 명령어로 넘김
- `grep java`: java가 포함된 줄만 필터링

**정상 출력 예시:**
```
appuser  12345  2.3  8.1 4823040 665432 ?  Sl   09:00   1:23 java -jar /app/myapp.jar
```

| 항목 | 의미 |
|------|------|
| `appuser` | 앱을 실행한 사용자 |
| `12345` | 프로세스 ID (PID) |
| `java -jar /app/myapp.jar` | 실행된 명령어 |

**비정상 출력 예시 (앱이 죽은 경우):**
```
appuser  99999  0.0  0.0  14432   952 pts/0  S+   10:01   0:00 grep --color=auto java
```
`grep java` 명령 자체만 보이고 실제 java 프로세스가 없으면 앱이 실행 중이 아닙니다.

### 방법 2: jps 명령어 (JDK 설치된 경우)

```bash
jps -l
```

`jps`는 Java 프로세스만 깔끔하게 보여줍니다.

**정상 출력 예시:**
```
12345 /app/myapp.jar
```

앱이 없으면 아무것도 출력되지 않습니다.

---

## Python 앱 확인

```bash
ps aux | grep python
```

또는 Python 3인 경우:

```bash
ps aux | grep python3
```

**정상 출력 예시:**
```
appuser  23456  0.5  1.2 245320 98764 ?  S   09:00   0:30 python3 /app/my_script.py
```

### 여러 Python 프로세스 구분하기

Python 앱이 여러 개 실행 중이라면, 실행 명령어의 **스크립트 파일명**으로 구분합니다.

```bash
ps aux | grep python3
```

```
appuser  23456  ... python3 /app/order_service.py    ← 주문 서비스
appuser  23789  ... python3 /app/payment_service.py  ← 결제 서비스
```

내가 담당하는 스크립트 파일명이 보이면 정상입니다.

---

## 포트(네트워크 소켓) 확인

앱이 프로세스로 떠 있더라도, 네트워크 연결을 받을 준비가 됐는지 포트를 확인해야 합니다.

```bash
ss -tlnp | grep <포트번호>
```

예시: 앱이 8080 포트를 사용하는 경우

```bash
ss -tlnp | grep 8080
```

**정상 출력 예시:**
```
LISTEN  0  128  0.0.0.0:8080  0.0.0.0:*  users:(("java",pid=12345,fd=42))
```

`LISTEN` 상태로 포트가 열려 있으면 정상입니다.

**구형 서버에서 netstat 사용:**
```bash
netstat -tlnp | grep 8080
```

---

## 로그 실시간 확인

앱이 정상 동작 중인지 로그를 통해 확인합니다.

```bash
tail -f /경로/app.log
```

**예시:**
```bash
tail -f /app/logs/myapp.log
```

- `tail -f`: 파일의 끝부분을 실시간으로 계속 보여줌
- 종료: `Ctrl + C`

**정상 로그 패턴 예시:**
```
2026-07-20 09:00:01 INFO  ApplicationStarted - App started successfully on port 8080
2026-07-20 09:00:05 INFO  MessageReceived - Received order message: ORDER-12345
```

**비정상 로그 패턴 예시:**
```
2026-07-20 09:00:01 ERROR ConnectionFailed - Failed to connect to RV daemon
2026-07-20 09:00:01 FATAL ApplicationExit - Exiting due to fatal error
```

`ERROR`, `FATAL`, `Exception` 키워드가 반복적으로 나오면 문제가 있는 상태입니다.

---

## systemd 서비스로 관리되는 경우

앱이 systemd 서비스로 등록되어 있다면 아래 명령어로 상태를 확인합니다.

```bash
systemctl status <서비스명>
```

**예시:**
```bash
systemctl status myapp.service
```

**정상 출력 예시:**
```
● myapp.service - My Application
   Loaded: loaded (/etc/systemd/system/myapp.service; enabled)
   Active: active (running) since Sun 2026-07-20 09:00:00 KST
```

- `active (running)`: 정상 실행 중
- `inactive (dead)`: 실행 중이 아님
- `failed`: 오류로 종료됨

---

## 빠른 확인 체크리스트

- [ ] `ps aux | grep java` (또는 `grep python3`) — 프로세스가 존재하는가?
- [ ] `ss -tlnp | grep <포트>` — 포트가 열려 있는가?
- [ ] `tail -f /경로/app.log` — 최근 로그에 ERROR/FATAL이 없는가?
