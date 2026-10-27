# 포트폴리오 관리

## 콘텐츠 수정

| 파일 | 내용 |
| --- | --- |
| `src/data/profile.json` | 소개, 이메일, 학력, 활동, 수상, 기술 |
| `src/data/projects.json` | 대표 프로젝트의 역할, 구현, 평가, 제한과 링크 |
| `src/data/archive.json` | 추가 개발 기록과 학습 저장소 |
| `public/images/` | 기존 실제 시연 이미지와 시스템 구성도 |
| `src/styles/site.css` | 제공된 무채색 HTML 템플릿의 기본 디자인 |
| `src/styles/enhancements.css` | 프로젝트·이력서·상세 페이지와 반응형 스타일 |
| `src/site.js` | 메뉴, 필터, 상세 dialog, 이메일 복사, 인쇄 |
| `scripts/build.py` | 공통 HTML 구성과 모든 정적 페이지 생성 |

프로젝트 날짜·검증 수치는 근거가 확인된 경우에만 갱신한다. `profile.updated`는 디자인 수정일이 아닌 자료 기준일이다. 비공개 Notion이나 개인 자료 링크는 공개하지 않는다.

## 검증 및 배포

`npm run verify`는 JavaScript 문법, HTML 생성, 메타데이터·내부 링크·이미지·프로젝트 기록 보존을 확인한다. npm 패키지 설치는 필요 없다. Node.js와 Python 3 표준 라이브러리만 사용한다.

`main`에 반영하면 GitHub Actions가 `dist/`를 GitHub Pages에 배포한다. 기존 `/projects/<slug>/`, `/about/`, `/resume/` 주소를 유지한다. 변경을 취소할 때는 Git 기록에서 해당 커밋을 revert하고 재배포한다.

`dist/index.html`은 홈페이지이며 스타일·스크립트를 포함한다. 이미지가 포함된 단일 파일 `dist/portfolio.html`도 생성된다. 이 파일의 별도 상세 페이지·이력서 링크는 운영 중인 GitHub Pages 주소로 연결된다.

## 이력서

`/resume/`의 인쇄 / PDF 저장 버튼을 사용한다. 인쇄 시 메뉴와 버튼을 숨기고 A4 형식으로 출력한다.

## 구현 특성

추가 서버·계정·분석 추적 도구 없이 동작한다. 이메일 복사 권한이 없으면 주소 선택과 직접 복사 안내로 대체한다. JavaScript를 사용할 수 없는 환경에서도 프로젝트 전체 페이지 링크와 주요 콘텐츠를 볼 수 있다.
