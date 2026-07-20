# 03. TIBCO RV(Rendezvous) 설정 확인

TIBCO Rendezvous(RV)란 무엇인지, 서버에서 설정이 올바른지 확인하는 방법을 설명합니다.

---

## 개념: TIBCO Rendezvous(RV)란

**TIBCO Rendezvous(RV)**는 시스템 간에 **메시지를 주고받는 미들웨어**입니다.

예를 들어, 주문 시스템과 결제 시스템이 서로 통신할 때 직접 연결하는 대신 RV를 통해 메시지를 주고받습니다. 마치 **우체국**처럼, 보내는 쪽과 받는 쪽이 직접 연결되지 않아도 메시지가 전달됩니다.

```
[주문 시스템] → RV 메시지 → [RV 데몬(rvd)] → RV 메시지 → [결제 시스템]
```

### RV 데몬(rvd)이란
**rvd**는 RV의 핵심 프로세스로, 메시지 중계 역할을 합니다. 앱들이 RV로 통신하려면 **서버에 rvd가 반드시 실행 중**이어야 합니다.

### 주요 RV 파라미터

| 파라미터 | 의미 | 기본값 |
|----------|------|--------|
| `service` | RV 서비스 포트 번호 | 7500 |
| `network` | 네트워크 인터페이스 또는 멀티캐스트 주소 | (빈값=자동) |
| `daemon` | rvd 접속 주소 | localhost:7500 |

---

## RV 데몬 기동 확인

### rvd 프로세스 확인

```bash
ps aux | grep rvd
```

**정상 출력 예시:**
```
tibco    1234  0.0  0.2  45678  1234 ?  Ss   09:00   0:01 /opt/tibco/tibrv/bin/rvd -service 7500
```

**비정상 출력 (rvd가 없는 경우):**
```
appuser  99999  0.0  0.0  14432  952 pts/0  S+   10:01   0:00 grep --color=auto rvd
```
`grep rvd` 명령 자체만 보이고 실제 rvd 프로세스가 없으면 RV 데몬이 꺼진 상태입니다.

### TIBCO 관련 전체 프로세스 확인

```bash
ps aux | grep tib
```

rvd 외에 다른 TIBCO 프로세스(rvroad, tibems 등)도 함께 확인할 수 있습니다.

---

## RV 포트 확인

rvd의 기본 포트는 **7500**입니다. 포트가 열려 있는지 확인합니다.

```bash
ss -tlnp | grep 7500
```

**정상 출력 예시:**
```
LISTEN  0  128  0.0.0.0:7500  0.0.0.0:*  users:(("rvd",pid=1234,fd=5))
```

포트가 열려 있으면 RV 데몬이 정상적으로 수신 대기 중입니다.

---

## RV 설정 파일 확인

### 일반적인 설정 파일 위치

RV 설정은 앱마다 다를 수 있습니다. 아래 위치를 순서대로 확인하세요.

```bash
# TIBCO 설치 기본 위치
ls /opt/tibco/

# 앱 디렉토리 내 설정 파일 검색
find /app -name "*.properties" -o -name "*.conf" -o -name "*.xml" | xargs grep -l "tibco\|rv\|rendezvous" 2>/dev/null
```

### 설정 파일에서 확인할 항목

설정 파일에서 아래 항목을 찾습니다.

```properties
# Java 앱의 경우 (예: application.properties)
rv.service=7500
rv.network=
rv.daemon=localhost:7500

# Python 앱의 경우 (예: config.yaml)
rv:
  service: "7500"
  network: ""
  daemon: "localhost:7500"
```

**확인 포인트:**
- `service`: 포트 번호가 rvd 기동 파라미터와 일치하는가?
- `daemon`: rvd가 실행 중인 서버 주소가 맞는가? (같은 서버면 `localhost`)

---

## 앱 로그에서 RV 연결 상태 확인

앱이 RV에 정상 연결됐는지 로그에서 확인합니다.

```bash
tail -f /경로/app.log | grep -i "rv\|rendezvous\|tibco"
```

### 정상 연결 로그 예시

```
INFO  RVConnection - Connected to TIBCO RV daemon at localhost:7500
INFO  RVListener  - Subscribed to subject: ORDER.CREATED
```

### 비정상 오류 로그 패턴

| 오류 메시지 | 의미 | 조치 |
|------------|------|------|
| `No such service` | 지정한 포트에 rvd가 없음 | rvd 기동 여부 확인 |
| `Daemon not running` | rvd 프로세스가 꺼져 있음 | rvd 재시작 요청 |
| `Connection refused` | 포트에 연결 불가 | 방화벽 또는 rvd 확인 |
| `Failed to create transport` | RV 트랜스포트 생성 실패 | service/network/daemon 파라미터 확인 |

---

## RV 관련 주의사항

### 페일오버 시 RV 데몬 재시작 필요

페일오버로 Standby 서버가 Active가 되면, **해당 서버의 rvd가 실행 중인지 반드시 확인**해야 합니다.

rvd가 꺼져 있으면 앱이 RV 통신을 못 하므로 메시지를 주고받지 못합니다. 자세한 내용은 [04_failover.md](04_failover.md)를 참고하세요.

---

## 빠른 확인 체크리스트

- [ ] `ps aux | grep rvd` — rvd 프로세스가 실행 중인가?
- [ ] `ss -tlnp | grep 7500` — 7500 포트가 열려 있는가?
- [ ] 앱 설정 파일의 `service`, `daemon` 파라미터가 올바른가?
- [ ] 앱 로그에 RV 연결 오류가 없는가?
