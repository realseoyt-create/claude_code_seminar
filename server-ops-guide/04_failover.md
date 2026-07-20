# 04. 페일오버 테스트

페일오버 테스트 시 무엇을, 어떤 순서로 확인해야 하는지 안내합니다.

---

## 개념: 페일오버(Failover)란

**페일오버**는 주 서버(Active)에 장애가 발생했을 때, 대기 서버(Standby)가 **자동으로 역할을 이어받는 것**입니다.

```
평상시:
  [Active 서버] ← 모든 트래픽  /  [Standby 서버] 대기 중

장애 발생:
  [Active 서버] ✗  →  [Standby 서버] ← 이제 Active로 전환
```

페일오버 테스트는 이 전환이 **제대로 일어나는지, 앱이 정상적으로 다시 뜨는지** 확인하는 테스트입니다.

### Active / Standby 구조

| 구분 | 역할 | 평소 상태 |
|------|------|-----------|
| Active 서버 | 실제 서비스 처리 | 앱·RV 실행 중 |
| Standby 서버 | 장애 대비 대기 | 앱 대기 중 (또는 꺼져 있음) |

---

## 테스트 전 준비 체크리스트

페일오버 테스트를 시작하기 전 아래를 모두 확인하세요.

### Active 서버 상태 확인

- [ ] 앱 프로세스가 실행 중인가? → [01_app_check.md](01_app_check.md) 참조
  ```bash
  ps aux | grep java       # Java 앱
  ps aux | grep python3    # Python 앱
  ```

- [ ] 앱 포트가 열려 있는가?
  ```bash
  ss -tlnp | grep <앱포트번호>
  ```

- [ ] RV 데몬이 실행 중인가? → [03_rv_config.md](03_rv_config.md) 참조
  ```bash
  ps aux | grep rvd
  ss -tlnp | grep 7500
  ```

- [ ] 앱 로그에 이상 없는가?
  ```bash
  tail -20 /경로/app.log
  ```

### Standby 서버 사전 확인

- [ ] Standby 서버에 SSH 접속 가능한가?
  ```bash
  ssh 사용자명@standby서버IP
  ```

- [ ] Standby 서버에서 앱 바이너리/스크립트가 존재하는가?
  ```bash
  ls -la /app/
  ```

### 테스트 공지

- [ ] 관련 담당자(앱 담당자, 인프라 담당자)에게 테스트 시작 시각 공지
- [ ] 테스트 중 영향받는 서비스 파악 및 사전 안내

---

## 페일오버 발생 직후 확인 포인트

Standby 서버가 Active로 전환된 직후 **신규 Active 서버**에서 아래를 순서대로 확인합니다.

### 1단계: 앱 프로세스 확인

```bash
ps aux | grep java
# 또는
ps aux | grep python3
```

앱 프로세스가 보이면 앱이 올라온 것입니다. 보이지 않으면 아직 기동 중이거나 기동에 실패한 것입니다.

> **잠깐 기다려야 하는 경우:** 페일오버 직후 앱이 완전히 뜨기까지 수십 초~수 분이 걸릴 수 있습니다. 프로세스가 보일 때까지 30초~1분 간격으로 반복 확인하세요.

### 2단계: 포트 응답 확인

```bash
ss -tlnp | grep <앱포트번호>
```

`LISTEN` 상태가 확인되면 앱이 네트워크 연결을 받을 준비가 된 것입니다.

### 3단계: RV 데몬 재기동 확인

```bash
ps aux | grep rvd
ss -tlnp | grep 7500
```

rvd가 실행 중이어야 합니다. **만약 rvd가 꺼져 있다면** 앱은 떠 있어도 RV 메시지를 주고받지 못합니다. 인프라 담당자에게 rvd 기동을 요청하세요.

### 4단계: 앱 로그 확인

```bash
tail -f /경로/app.log
```

확인할 항목:
- 시작 성공 메시지가 있는가? (`Started`, `Initialized`, `Ready` 등)
- RV 연결 성공 메시지가 있는가?
- ERROR, FATAL, Exception이 반복적으로 나오지 않는가?

**정상 기동 로그 예시:**
```
2026-07-20 10:05:01 INFO  Application    - Starting MyApp...
2026-07-20 10:05:03 INFO  RVConnection   - Connected to TIBCO RV daemon at localhost:7500
2026-07-20 10:05:03 INFO  RVListener     - Subscribed to subject: ORDER.CREATED
2026-07-20 10:05:03 INFO  Application    - MyApp started successfully on port 8080
```

### 5단계: 크론탭 확인

페일오버 후 크론 작업이 **올바른 서버(신규 Active)**에서 실행되는지 확인합니다.

```bash
crontab -l
```

크론이 등록되어 있어야 할 항목이 없다면, 크론탭이 이관되지 않은 것입니다. 인프라 담당자에게 확인을 요청하세요.

---

## 페일오버 확인 요약표

| 순서 | 확인 항목 | 명령어 | 정상 기준 |
|------|-----------|--------|-----------|
| 1 | 앱 프로세스 | `ps aux \| grep java` | 프로세스 존재 |
| 2 | 앱 포트 | `ss -tlnp \| grep <포트>` | LISTEN 상태 |
| 3 | RV 데몬 | `ps aux \| grep rvd` | rvd 프로세스 존재 |
| 4 | RV 포트 | `ss -tlnp \| grep 7500` | LISTEN 상태 |
| 5 | 앱 로그 | `tail -f /경로/app.log` | ERROR/FATAL 없음 |
| 6 | 크론탭 | `crontab -l` | 예상 작업 등록됨 |

---

## 테스트 후 확인사항

원래 Active 서버가 복구된 후:

- [ ] 원래 Active 서버 복구 확인 (역할 복귀 여부 확인)
- [ ] 메시지 유실 여부 확인: 테스트 중 처리되지 않은 메시지가 있는지 앱 로그 비교
- [ ] 양쪽 서버 로그 타임스탬프 기준으로 페일오버 시각 기록
- [ ] 테스트 결과 담당자에게 보고

---

## 자주 발생하는 문제

| 증상 | 가능한 원인 | 조치 |
|------|------------|------|
| 프로세스가 안 뜸 | 기동 스크립트 미이관, 설정 파일 없음 | 인프라 담당자에게 문의 |
| 포트가 안 열림 | 앱이 기동 실패 상태 | 앱 로그의 ERROR 확인 |
| RV 연결 실패 | rvd가 꺼져 있음 | rvd 기동 요청 |
| 크론이 없음 | 크론탭 미이관 | 인프라 담당자에게 크론탭 이관 요청 |
