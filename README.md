# WeatherBot API 
---
## Quickstart 
가상환경 또는 컨테이너를 사용해 실행합니다.
### container (build and start containers)
```sh
docker-compose up -d --build
```
### venv (setup environments and run server)
```sh
1. pip install pip-tools
2. pip-sync requirements/dev.txt
3. sh run_server.sh
```
---
## Health check
서버 상태를 체크합니다.
```sh
curl -X GET http://localhost:8000/livez
```
---
## Unittest
가상환경 또는 컨테이너를 사용해 테스트합니다.
### container
```sh
docker exec -it web bash -c "pytest -vv tests"
```
### venv
```sh
pytest -vv tests
```
---
## Coinfig
앱의 config를 관리합니다.
- app.conf.log: 로그 설정 config를 관리합니다.
- app.conf.config.service: 전체적인 서비스와 관련된 config를 관리합니다.
