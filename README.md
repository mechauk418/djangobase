# DjangoBase

## 목차

0. 개발 목적
1. 서비스 소개
2. 기술 스택
3. 기능
4. 개발 과정

### 0. 개발 목적

django rest framework로 웹페이지를 구축할때 기본이 되는 틀을 만들고 이를 Docker 등을 사용하여 배포하여 CI/CD 파이프라인 구축까지 연습을 한다.

### 1. 서비스 소개

기본적인 사용자 계정 관리와 하나의 게시판을 가진 웹페이지

### 2. 기술 스택

| Backend            | Database   | Release           | Cooperation |
| ------------------ | ---------- | ----------------- | ----------- |
| Python             | PostgreSQL | EC2, Docker, Github action  | GIT, GITHUB |
| Django Restful API | RDS        | 가비아(domain)    |             |

### 3. 기능

1. accounts
- 회원 가입
- 로그인, 로그아웃
- 소셜 로그인
- JWT

2. article
- 게시글 및 댓글 CRUD
- 이미지 첨부
- 조회수 및 추천 
- 검색 및 필터링

### 4. 개발 과정

[DRF를 활용하여 게시판 만들기]('https://velog.io/@mechauk418/series/FastAPI%EB%A1%9C-%EA%B2%8C%EC%8B%9C%ED%8C%90-%EB%A7%8C%EB%93%A4%EA%B8%B0)