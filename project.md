# 나도 바나나 (Nano Banana) 프로젝트

## 📋 프로젝트 개요
여러 장의 이미지와 텍스트 프롬프트를 입력받아 새로운 이미지를 생성하는 Flask 기반 웹서비스

- **서비스명**: 나도 바나나
- **메인 컬러**: #FFD548
- **로고**: logo.png
- **기술 스택**: Flask, Jinja2, Google Gemini API

## ✅ 할일 목록 (TODO)

### 1. 환경 설정
- [ ] requirements.txt 파일 생성
  - Flask
  - google-generativeai
  - Pillow
  - python-dotenv
  - Werkzeug
- [ ] 필요한 패키지 설치
- [ ] 프로젝트 폴더 구조 생성
  - [ ] templates/ 폴더
  - [ ] static/ 폴더 (css/, js/, images/)
  - [ ] uploads/ 폴더 (임시 업로드)
  - [ ] output/ 폴더 (생성된 이미지)

### 2. 백엔드 개발 (Flask)
- [ ] app.py 메인 파일 생성
- [ ] 라우트 설정
  - [ ] `/` - 메인 페이지
  - [ ] `/generate` - 이미지 생성 API
  - [ ] `/download/<filename>` - 이미지 다운로드
- [ ] 파일 업로드 처리 로직
  - [ ] 다중 파일 업로드 지원
  - [ ] 파일 유효성 검사 (이미지 파일만)
  - [ ] 안전한 파일명 생성
- [ ] Gemini API 연동
  - [ ] API 키 환경변수 로드
  - [ ] 이미지 + 텍스트 프롬프트 전송
  - [ ] 생성된 이미지 수신 및 저장
- [ ] 에러 처리
  - [ ] API 호출 실패
  - [ ] 파일 업로드 실패
  - [ ] 필수 입력값 검증

### 3. 프론트엔드 개발
- [ ] HTML 템플릿 (templates/)
  - [ ] base.html - 기본 레이아웃
  - [ ] index.html - 메인 페이지
  - [ ] result.html - 결과 페이지
- [ ] CSS 스타일링 (static/css/)
  - [ ] 메인 컬러 (#FFD548) 적용
  - [ ] 반응형 디자인
  - [ ] 드래그 앤 드롭 영역 스타일
- [ ] JavaScript 기능 (static/js/)
  - [ ] Drag & Drop 파일 업로드
  - [ ] 파일 미리보기
  - [ ] 업로드 진행 상태 표시
  - [ ] 폼 유효성 검사

### 4. UI/UX 구현
- [ ] 헤더 영역
  - [ ] 로고 배치
  - [ ] "Created by Newton School" 표시
- [ ] 파일 업로드 영역
  - [ ] Drag & Drop 영역 구현
  - [ ] 파일 선택 버튼 (대체 방법)
  - [ ] 업로드된 파일 목록 표시
- [ ] 텍스트 프롬프트 입력
  - [ ] 텍스트 영역 (필수 입력)
  - [ ] 입력 가이드 텍스트
- [ ] 이미지 생성 버튼
- [ ] 결과 표시
  - [ ] 생성된 이미지 표시
  - [ ] 다운로드 버튼

### 5. Gemini API 통합
- [ ] google-generativeai 패키지 설정
- [ ] 모델 설정 (gemini-2.0-flash-exp)
- [ ] 이미지 처리
  - [ ] PIL로 이미지 열기
  - [ ] BytesIO로 메모리 처리
  - [ ] Base64 인코딩 (필요시)
- [ ] API 호출 및 응답 처리
- [ ] 생성된 이미지 저장

### 6. 테스트 및 디버깅
- [ ] 단일 이미지 업로드 테스트
- [ ] 다중 이미지 업로드 테스트
- [ ] 다양한 이미지 포맷 테스트 (JPG, PNG, GIF)
- [ ] 대용량 파일 처리 테스트
- [ ] API 응답 시간 확인
- [ ] 에러 케이스 테스트

### 7. 배포 준비
- [ ] 프로덕션 설정
- [ ] 보안 설정
  - [ ] 파일 업로드 크기 제한
  - [ ] 허용 파일 확장자 제한
  - [ ] CSRF 보호
- [ ] 로깅 설정
- [ ] 배포 문서 작성

## 📁 프로젝트 구조
```
nano-banana-web/
├── app.py                 # Flask 메인 애플리케이션
├── requirements.txt       # Python 패키지 목록
├── .env                  # 환경변수 (API 키)
├── .gitignore           # Git 제외 파일
├── project.md           # 프로젝트 문서 (현재 파일)
├── logo.png             # 서비스 로고
├── templates/           # HTML 템플릿
│   ├── base.html       # 기본 레이아웃
│   ├── index.html      # 메인 페이지
│   └── result.html     # 결과 페이지
├── static/             # 정적 파일
│   ├── css/
│   │   └── style.css   # 스타일시트
│   ├── js/
│   │   └── main.js     # JavaScript
│   └── images/
│       └── logo.png    # 로고 복사본
├── uploads/            # 임시 업로드 폴더
└── output/            # 생성된 이미지 폴더
```

## 🔑 핵심 기능
1. **이미지 파일 불러오기**
   - 여러 개 파일 동시 업로드
   - Drag & Drop 지원
   - 선택적 입력

2. **텍스트 프롬프트**
   - 필수 입력
   - 이미지 생성 지시사항

3. **이미지 생성**
   - Gemini API 활용
   - gemini-2.0-flash-exp 모델 사용

4. **결과 저장 및 다운로드**
   - output 폴더 저장
   - 다운로드 기능 제공

## 📝 참고사항
- API Key는 .env 파일의 GOOGLE_API_KEY 사용
- example.py 파일 참고하여 Gemini API 구현
- 보안을 위해 .env 파일은 Git에서 제외됨

## 🚀 실행 방법
```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. Flask 서버 실행
python app.py

# 3. 브라우저에서 접속
http://localhost:5000
```

## 📅 진행 상태
- 프로젝트 시작일: 2025-01-23
- 현재 단계: ✅ 개발 완료
- Flask 서버 실행 중: http://localhost:5000

## ✅ 완료된 항목
- [x] requirements.txt 파일 생성
- [x] 프로젝트 폴더 구조 생성
- [x] Flask app.py 구현
- [x] HTML 템플릿 작성 (base, index, result)
- [x] CSS 스타일링 (#FFD548 메인 컬러 적용)
- [x] JavaScript Drag & Drop 기능 구현
- [x] 파일 업로드 및 미리보기 기능
- [x] 서버 실행 테스트 완료