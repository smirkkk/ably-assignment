# ably-assignment

이 프로젝트는 Django REST framework로 개발되었습니다.

## 사용 기술
- Python Django, DRF
- MySQL
- Docker-compose


## 실행 방법
`docker-compose up -d`

## 구현 내용
### 1. API
[Postman Document](https://documenter.getpostman.com/view/14542884/UVkvKY6v)

- 회원 가입 API
  * 하기 API를 통해 전화번호를 인증하면 전화번호를 세션에 저장합니다.
  * 세션에 저장된 전화번호를 통해 회원가입을 진행합니다.
  * 회원가입이 완료되면 세션의 전화번호를 지웁니다.
- 로그인 API
  * 이메일, 전화번호, 아이디로 로그인이 가능합니다.
  * 위 요소들은 중복되어 요청할 수 없습니다.
- 내 정보 보기 API
  * 로그인, 회원가입 시 반환되는 JWT를 통해 인증합니다.
  * `Authorization: jwt {{token}}`
- 비밀번호 재설정 API
  * 회원가입과 동일하게 전화번호를 먼저 인증해야 합니다.
  * 가입되지 않은 전화번호로 인증을 진행하는 경우를 막기 위해 인증 시 `unique_only` 값을 `false`로 해야합니다.
- 인증번호 발송 & 전화번호 인증 API
  * 실제 전송, 인증을 하지 않습니다.
  * `unique_only`값이 `true`인 경우 중복된 전화번호는 거부합니다.
  * `unique_only`값이 `false`인 경우 이미 가입된 전화번호만 허용합니다.
  * `unique_only`의 기본값은 `true`입니다. 

### 2. 그 외
- 환경 변화로 인한 문제가 생기지 않도록 `docker compose`를 사용했습니다.
- `python manage.py test`로 테스트를 진행할 수 있습니다. DB 컨테이너가 실행중이어야 합니다.
- 디버그, 배포 모드 분리와 asgi를 통한 배포는 제외하였습니다.


---

## 후기

요구사항을 처음 읽었을 때 센스가 필요한 문제로 판단하였습니다.

제 경험을 토대로 생각해보면 입력값에 대한 `validation`이 가장 센스가 필요했던 것 같습니다. 

데이터의 형식은 정해져있는데 반해 유저의 입력은 자유로우니까요. 

이것은 UI/UX만으로 100% 통제할 수 없는 영역입니다.

DRF의 `Serializer`가 이 부분에 도움을 줘 쉽게 해결할 수 있었던 것 같습니다.
