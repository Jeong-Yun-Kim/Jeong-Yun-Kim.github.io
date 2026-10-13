# 구현·검증 결과

기준일: 2026-10-13

## 공개 배포

- 사이트: https://jeong-yun-kim.github.io/
- 저장소: https://github.com/Jeong-Yun-Kim/Jeong-Yun-Kim.github.io
- 공개 저장소 생성, 소스 반영, Pages의 GitHub Actions 배포와 HTTPS 강제 적용 완료.
- 확인한 배포 실행: https://github.com/Jeong-Yun-Kim/Jeong-Yun-Kim.github.io/actions/runs/38404997000
- 위 실행의 소스: `aa885ce81ee429cc021c183fdca3ad6f039a6fe5`. 빌드·배포 모두 성공.
- Node.js 24·Ubuntu 24.04와 Node 24 기반 공식 Pages Actions 사용.
- 저장소 생성 직후의 기본 Jekyll 배포가 늦게 완료되어 첫 Astro 배포를 덮은 문제를 확인했다. 기본 실행 종료 후 Astro를 재배포하여 해결하고 공개 경로를 다시 검사했다.
- 다른 프로젝트 저장소는 수정하지 않음.

## 구현

- Astro 7.3.8·TypeScript 기반 정적 사이트.
- 홈·소개·대표 프로젝트 4개 상세·AI Rescue Box 아카이브 상세·전체 프로젝트·이력서·404, 총 10개 HTML.
- 데스크톱·태블릿·모바일용 CSS, 키보드 포커스·본문 건너뛰기·시맨틱 구조·이미지 alt.
- 인쇄용 A4 CSS와 인쇄/PDF 저장 버튼.
- canonical·Open Graph·favicon·robots·sitemap, 기본 경로 `/`와 디렉터리별 HTML 출력.
- 프로젝트 데이터와 프로필 데이터 분리. 수정 절차는 README 참조.
- 전체 정적 산출물 377,812 bytes(약 378 KB). 애플리케이션 JavaScript는 이력서 인쇄 이벤트에만 사용.

## 자동 검사와 공개 HTTP 검증

- `npm run check`: 오류 0·경고 0·힌트 0.
- `npm run build`: 정적 HTML 10개 생성 성공.
- `npm run validate`: 내부 링크 213개·자산 참조 53개 통과.
- 외부 링크 20개: HTTP GET 200 확인. YouTube 실제 재생 여부까지 검증한 것은 아님.
- 재배포 후 공개 주소 25건 검사 통과: HTML·CSS·이미지·favicon·robots·sitemap, 상세/이력서의 슬래시 없는 경로, 임의 없는 경로, HTTP→HTTPS.
- 배포된 HTML·자산의 본문이 로컬 빌드 결과와 바이트 단위로 일치함을 확인.
- 없는 경로는 HTTP 404와 사용자 정의 404 본문 반환. `/404.html` 직접 접근은 HTTP 200.
- `.nojekyll`은 배포 제어 파일로 공개 자산 검사 대상에서 제외.
- 개인정보·임시 문구 검사. 비공개 원본 코드와 Notion 전문은 공개 소스에 포함하지 않음.

## 실제 브라우저에서 확인

- Chrome 데스크톱에서 홈, CausalRoboQC와 CARLA 상세, 전체 프로젝트 아카이브, 이력서, 사용자 정의 404 표시 확인.
- 상세 URL 직접 접속·새로고침, 슬래시 없는 상세 URL의 정규 경로 이동 확인.
- CausalRoboQC 사진·화면의 지연 로딩과 CARLA 구성도 표시 확인.
- 홈·상세 화면의 가로 넘침 없음.
- 키보드 Enter로 본문 건너뛰기 링크를 실행하여 `main` 포커스 이동 확인.

## 검증 한계

- 모바일·태블릿용 반응형 CSS는 구현했지만 실제 기기와 모바일 뷰포트 렌더링은 검증하지 못했다.
- Firefox·Safari 실브라우저, 전체 키보드 이동, 실제 인쇄/PDF 페이지 분할, Lighthouse 점수는 측정하지 않았다.
- 현재 환경의 Sites 스킬은 지정된 browser control 스킬이 없으면 로컬 preview 서버와 다른 브라우저 제어 경로를 사용하지 않도록 명시한다. 해당 스킬이 제공되지 않아 로컬 브라우저 QA는 실행하지 않았다. 공개 배포 후 지원되는 Chrome 브라우저에서 위 범위를 직접 확인했다.
- 프로젝트 자체의 테스트 수·성능 수치는 원본 개발 기록이며, 사이트 구축 과정에서 로봇·시뮬레이션 시험을 재실행한 결과가 아니다.
