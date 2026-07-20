# 02. 크론탭(Crontab) 관리

크론탭이 무엇인지, 내 앱이 등록되어 있는지 확인하는 방법을 설명합니다.

---

## 개념: 크론이란 무엇인가

**크론(Cron)**은 리눅스의 자동 스케줄러입니다. "매일 오전 9시에 이 스크립트를 실행해라", "10분마다 이 프로그램을 실행해라"와 같은 일정을 등록해두면 자동으로 실행합니다.

**크론탭(Crontab)**은 크론의 **설정 파일**입니다. 어떤 명령을 언제 실행할지 목록이 담겨 있습니다.

크론은 사용자별로 분리되어 있습니다. `appuser`의 크론탭과 `root`의 크론탭은 별개입니다.

---

## 크론탭 확인

### 현재 사용자의 크론탭 보기

```bash
crontab -l
```

**등록된 작업이 있는 경우:**
```
# 매일 오전 9시에 주문 처리 스크립트 실행
0 9 * * * /usr/bin/python3 /app/order_process.py >> /app/logs/order.log 2>&1

# 서버 재부팅 시 앱 자동 시작
@reboot /usr/bin/java -jar /app/myapp.jar >> /app/logs/myapp.log 2>&1
```

**아무것도 없는 경우:**
```
no crontab for appuser
```

### 다른 사용자의 크론탭 보기 (sudo 권한 필요)

```bash
sudo crontab -l -u <사용자명>
```

예시:
```bash
sudo crontab -l -u appuser
```

### 시스템 크론 위치 확인

사용자 크론탭 외에 시스템 전체에 영향을 주는 크론 설정 위치입니다.

```bash
# 시스템 크론탭 파일
cat /etc/crontab

# 시스템 크론 디렉토리 목록
ls /etc/cron.d/
```

---

## 크론 표현식 읽는 법

크론탭의 각 줄은 아래 형식입니다.

```
분  시  일  월  요일  실행할명령어
```

```
*   *   *   *    *    /usr/bin/python3 /app/script.py
│   │   │   │    │
│   │   │   │    └── 요일 (0=일요일, 1=월요일 ... 6=토요일)
│   │   │   └─────── 월 (1~12)
│   │   └─────────── 일 (1~31)
│   └─────────────── 시 (0~23)
└─────────────────── 분 (0~59)
```

**`*` 의미**: "모든 값에 해당" (제한 없음)

### 자주 쓰는 예시

| 표현식 | 의미 |
|--------|------|
| `0 9 * * *` | 매일 오전 9시 정각 |
| `30 8 * * 1-5` | 평일(월~금) 오전 8시 30분 |
| `*/10 * * * *` | 10분마다 |
| `0 0 1 * *` | 매월 1일 자정 |
| `@reboot` | 서버 재부팅 시 한 번 |

---

## 크론 실행 로그 확인

크론이 실제로 실행됐는지, 오류가 있는지 로그로 확인합니다.

### Ubuntu / Debian 계열

```bash
grep CRON /var/log/syslog | tail -20
```

### RHEL / CentOS / Rocky Linux 계열

```bash
grep CRON /var/log/cron | tail -20
```

### systemd 기반 (최신 배포판)

```bash
journalctl -u cron --since "today"
```

**정상 실행 로그 예시:**
```
Jul 20 09:00:01 myserver CRON[45678]: (appuser) CMD (/usr/bin/python3 /app/script.py)
```

**오류 로그 예시:**
```
Jul 20 09:00:01 myserver CRON[45678]: (appuser) CMD (/usr/bin/python3 /app/script.py)
Jul 20 09:00:02 myserver CRON[45678]: (CRON) error (grandchild #45679 failed with exit status 1)
```

`exit status 1`과 같은 오류가 보이면 스크립트 실행이 실패한 것입니다. 앱 담당자에게 알려주세요.

---

## 크론탭 주의사항

### 1. 절대 경로를 사용해야 합니다

크론은 일반 터미널과 달리 **환경변수가 거의 없습니다**. 따라서 명령어의 전체 경로를 써야 합니다.

```bash
# 잘못된 예 (크론에서 실패할 수 있음)
python3 /app/script.py

# 올바른 예 (전체 경로 사용)
/usr/bin/python3 /app/script.py
```

`python3`의 실제 경로 확인:
```bash
which python3
# 출력: /usr/bin/python3
```

### 2. 로그 저장 설정

크론 작업의 출력을 파일로 저장해두면 나중에 실행 결과를 확인할 수 있습니다.

```bash
# 표준 출력과 오류 출력 모두 파일에 저장
0 9 * * * /usr/bin/python3 /app/script.py >> /app/logs/cron.log 2>&1
```

- `>>`: 기존 파일에 이어쓰기 (덮어쓰지 않음)
- `2>&1`: 오류 출력도 같은 파일에 저장

---

## 빠른 확인 체크리스트

- [ ] `crontab -l` — 내 크론탭에 앱이 등록되어 있는가?
- [ ] 크론 표현식이 의도한 시간과 맞는가?
- [ ] 명령어 경로가 절대 경로로 되어 있는가?
- [ ] 로그 파일 경로가 설정되어 있는가?
- [ ] 최근 크론 실행 로그에 오류가 없는가?
