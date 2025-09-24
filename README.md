# 나도 바나나 (Nano Banana) 🍌

AI 기반 이미지 생성 웹 서비스

## 📋 프로젝트 소개
여러 장의 이미지와 텍스트 프롬프트를 입력받아 새로운 이미지를 생성하는 Flask 기반 웹서비스입니다.

## 🚀 주요 기능
- 🎨 텍스트를 이미지로 변환 (Text-to-Image)
- 🖼️ 이미지 편집 및 변환 (Image-to-Image)
- 📤 드래그 앤 드롭 파일 업로드
- 💾 생성된 이미지 다운로드

## 🛠️ 기술 스택
- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript
- **AI API**: Nano-GPT API (이미지 생성)
- **이미지 처리**: Pillow

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/KennyB76/nano-banana-web.git
cd nano-banana-web
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 설정
`.env` 파일에 API 키 추가:
```
NANO_GPT_API_KEY = your_api_key_here
```

> **참고**: Nano-GPT API 키는 [https://nano-gpt.com](https://nano-gpt.com) 에서 발급받을 수 있습니다.

### 4. 서버 실행
```bash
python app.py
```

브라우저에서 http://localhost:5000 접속

## 📱 사용 방법
1. 웹 페이지에 접속
2. 이미지를 드래그 앤 드롭 또는 클릭하여 업로드 (선택사항)
3. 텍스트 프롬프트 입력 (필수)
4. "이미지 생성하기" 버튼 클릭
5. 생성된 이미지 확인 및 다운로드

## 🎨 지원 모델
- `hidream` - 기본 이미지 생성 모델
- `recraft-v3` - 고품질 이미지 생성
- `flux-kontext` - 이미지 편집 및 변환

## ⚠️ 현재 상태
- ✅ Nano-GPT API 통합 완료
- ⚠️ API 키가 필요합니다 (유료 서비스)
- 💡 Google Gemini API는 이미지 생성을 지원하지 않아 Nano-GPT로 대체

## 📁 프로젝트 구조
```
nano-banana-web/
├── app.py              # Flask 메인 애플리케이션
├── requirements.txt    # Python 패키지 목록
├── .env               # 환경변수 (API 키)
├── templates/         # HTML 템플릿
├── static/           # CSS, JS, 이미지
├── uploads/          # 임시 업로드 폴더
└── output/           # 생성된 이미지
```

## 🏷️ 라이선스
Created by Newton School

## 🔗 링크
- GitHub: https://github.com/KennyB76/nano-banana-web
- Nano-GPT API: https://docs.nano-gpt.com