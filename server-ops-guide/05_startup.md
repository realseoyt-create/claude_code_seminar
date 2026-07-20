# 05. 앱 기동 방법 선택

앱을 서버에서 어떻게 띄워야 하는지, 방법별 차이와 권장 방식을 설명합니다.

---

## 앱 기동 방법 4가지 비교

| 방법 | 설명 | 장점 | 단점 | 권장 상황 |
|------|------|------|------|-----------|
| **수동 실행** | SSH 접속 후 직접 명령 실행 | 가장 단순 | 서버 재시작 시 앱이 사라짐 | 개발·테스트·임시 실행 |
| **크론탭 `@reboot`** | 재부팅 시 크론으로 자동 실행 | 설정이 간단 | 재시작 관리·상태 모니터링 어려움 | 간단한 배치 스크립트 |
| **systemd 서비스** | OS 서비스로 등록 | 재시작 자동화·로그 통합·상태 관리 | 설정 파일 작성 필요 | **운영 환경 권장** |
| **Supervisor** | Python 프로세스 관리 도구 | 설정 쉬움·재시작 자동화 | 별도 설치 필요 | Python 앱 운영 |

---

## 방법 1: 수동 실행

SSH 접속 후 터미널에서 직접 앱을 실행합니다.

**문제점:** 터미널을 닫거나 SSH 접속이 끊기면 앱도 같이 종료됩니다.

이를 방지하려면 `nohup`과 `&`를 사용합니다.

### Java 앱 수동 실행

```bash
nohup java -jar /app/myapp.jar > /app/logs/myapp.log 2>&1 &
```

### Python 앱 수동 실행

```bash
nohup python3 /app/my_script.py > /app/logs/script.log 2>&1 &
```

**명령어 설명:**
- `nohup`: 터미널이 닫혀도 프로세스가 종료되지 않도록 함
- `> /app/logs/myapp.log 2>&1`: 출력과 오류를 파일에 저장
- `&`: 백그라운드에서 실행

**실행 후 PID 확인:**
```bash
echo $!    # 방금 실행한 프로세스의 PID 출력
```

> **주의:** 서버가 재시작되면 앱이 사라집니다. 임시 목적이 아니라면 아래 방법을 사용하세요.

---

## 방법 2: 크론탭 `@reboot`

서버 재부팅 시 자동으로 앱을 실행합니다.

```bash
crontab -e
```

편집기가 열리면 아래를 추가합니다.

### Java 앱

```
@reboot /usr/bin/java -jar /app/myapp.jar >> /app/logs/myapp.log 2>&1
```

### Python 앱

```
@reboot /usr/bin/python3 /app/my_script.py >> /app/logs/script.log 2>&1
```

**`@reboot`의 한계:**
- 앱이 죽어도 자동으로 재시작하지 않습니다 (재부팅 시에만 실행됨)
- 앱 상태를 OS 레벨에서 모니터링하기 어렵습니다
- 배치성 스크립트나 단순한 시작 목적에 적합합니다

---

## 방법 3: systemd 서비스 (운영 환경 권장)

운영 환경에서 권장하는 방식입니다. OS가 앱의 생명주기를 관리하며, 앱이 죽으면 자동으로 재시작합니다.

### 서비스 파일 작성

`/etc/systemd/system/myapp.service` 파일을 생성합니다. (sudo 권한 필요)

**Java 앱 서비스 파일 예시:**

```ini
[Unit]
Description=My Java Application
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/app
ExecStart=/usr/bin/java -jar /app/myapp.jar
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Python 앱 서비스 파일 예시:**

```ini
[Unit]
Description=My Python Application
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/app
ExecStart=/usr/bin/python3 /app/my_script.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 서비스 등록 및 시작

```bash
# systemd 설정 다시 읽기
sudo systemctl daemon-reload

# 서비스 활성화 (부팅 시 자동 시작)
sudo systemctl enable myapp.service

# 서비스 시작
sudo systemctl start myapp.service

# 서비스 상태 확인
sudo systemctl status myapp.service
```

### systemd 앱 로그 확인

```bash
journalctl -u myapp.service -f
```

### systemd의 장점

- **자동 재시작:** 앱이 죽으면 `RestartSec` 후 자동으로 재시작
- **부팅 시 자동 시작:** `systemctl enable` 설정 후 서버 재시작 시 자동으로 기동
- **로그 통합:** `journalctl`로 앱 로그와 시스템 로그를 통합 조회 가능
- **상태 관리:** `systemctl status`로 현재 상태, 최근 로그 한눈에 확인

---

## 방법 4: Supervisor (Python 앱)

Supervisor는 Python 앱을 관리하기 위한 전용 프로세스 관리 도구입니다.

```bash
# Supervisor 설치 (Ubuntu/Debian)
sudo apt-get install supervisor

# 설치 확인
supervisorctl status
```

**Supervisor 설정 파일 예시 (`/etc/supervisor/conf.d/myapp.conf`):**

```ini
[program:myapp]
command=/usr/bin/python3 /app/my_script.py
directory=/app
user=appuser
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/app/logs/supervisor.log
```

```bash
# 설정 다시 읽기 및 앱 시작
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start myapp
```

---

## 결론: 크론으로 앱을 띄워야 하는가?

| 상황 | 권장 방법 |
|------|-----------|
| 운영 환경 Java/Python 앱 | **systemd 서비스** |
| 간단한 배치 스크립트 (주기적 실행) | **크론탭** (주기 실행용) |
| 재부팅 시 간단히 띄우고 싶음 | 크론탭 `@reboot` (단, 재시작 관리 불가) |
| Python 앱이고 Supervisor가 설치되어 있음 | **Supervisor** |
| 테스트/임시 실행 | **수동 실행** |

크론탭 `@reboot`은 가능하지만, **앱이 죽었을 때 자동으로 재시작되지 않는다**는 한계가 있습니다. 운영 환경에서는 `systemd`를 사용하는 것을 권장합니다.

---

## 빠른 참고: 앱 상태 관리 명령어

| 목적 | systemd | Supervisor |
|------|---------|------------|
| 시작 | `systemctl start myapp` | `supervisorctl start myapp` |
| 중지 | `systemctl stop myapp` | `supervisorctl stop myapp` |
| 재시작 | `systemctl restart myapp` | `supervisorctl restart myapp` |
| 상태 확인 | `systemctl status myapp` | `supervisorctl status myapp` |
| 로그 확인 | `journalctl -u myapp -f` | `tail -f /app/logs/supervisor.log` |
