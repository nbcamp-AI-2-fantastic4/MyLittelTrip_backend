# 🛫 MyLittelTrip

여행일정 추천받기  
https://mylittletrip-4416.web.app

<br />

# 📃 프로젝트 정보

### 1. 제작기간

> 2022.07.07 ~ 09.02

### 2. 참여 인원

> |                    Name                    |  Position   |
> | :----------------------------------------: | :---------: |
> | [김동우](https://github.com/kimphysicsman) | Back, Front |
> |   [김진수](https://github.com/creamone)    |    Back     |
> |     [박진우](https://github.com/J1NU2)     |    Back     |
> |    [최민기](https://github.com/mankic)     |    Back     |

### 3. 역할 분담

> - 김동우 : 유저 기능 / 여행일정 추천 기능 + Front 구성
> - 김진수 : 여행장소 기능 + server 배포
> - 박진우 : 댓글, 좋아요 기능 + server 배포
> - 최민기 : 리뷰 기능 + server 배포

<br />

# 📚 기술 스택

### 1. Back-end

> python3  
> Django  
> Django-rest-framwork

### 2. Front-end

> React.js  
> Node.js

<br />

# 📊 ERD & Structure

<details>
<summary>ERD</summary>
<div markdown="1" style="padding-left: 15px;">
<img src="https://user-images.githubusercontent.com/68724828/186067947-f255f9a4-d92d-45cd-ab7c-419ec92943f8.png" width="800px"/>
</div>
</details>

<br />

<details>
<summary>Structure</summary>
<div markdown="1" style="padding-left: 15px;">
<img src="https://user-images.githubusercontent.com/68724828/186079270-28793ba1-466e-421f-baf2-563b890c926f.png" />
</div>
</details>

<br />

# 🔑 핵심기능

### 1. 여행장소 검색

> 사용자가 여행장소를 검색하면 DB에서 여행장소를 검색하고  
> DB에 없는 장소이면 네이버지도에서 검색하여 최상단의 장소의 정보를 가져오고 DB에 저장합니다.  
> [코드 보러가기](https://github.com/nbcamp-AI-2-fantastic4/MyLittelTrip_backend/blob/d9eba0efc4567cbaef9ec19eea76e76495190a69/recommend/functions/parsing.py#L70)

### 2. 최단 여행경로 찾기 & 여행일정 만들기

> 사용자가 입력한 여행장소들을 바탕으로 여행일정을 만듭니다.  
> [코드 보러가기](https://github.com/nbcamp-AI-2-fantastic4/MyLittelTrip_backend/blob/d9eba0efc4567cbaef9ec19eea76e76495190a69/recommend/functions/schedule.py#L14)

<br />

# 📕 기타 자료

### 1. 기획문서

> [MyLittleTrip - Notion](https://www.notion.so/kimphysicsman/MLT-My-Little-Trip-716433a2fc8940d9870bd83b63570646?v=0c42e849923d4449aade69046bf597d1)

### 2. 여행추천 알고리즘

> [Travel_recommedation - Github](https://github.com/kimphysicsman/Travel_recommedation)

### 3. 발표영상

<table>
  <tbody>
    <tr>
      <td>
        <p align="center"> 22.08.05 발표 </p>
        <a href="https://www.youtube.com/watch?v=6B0DSjvsqj0&t=1s" title="MyLittleTrip 중간발표">
          <img align="center" src="https://user-images.githubusercontent.com/68724828/186087151-e0f0ebed-08c1-4a99-9af0-a8c48c536205.png" width="300" >
        </a>
      </td>
      <td>
        <p align="center"> 22.08.16 발표 </p>
        <a href="https://youtu.be/9eoYpRqTZUU" title="MyLittleTrip 최종발표">
          <img align="center" src="https://user-images.githubusercontent.com/68724828/186087151-e0f0ebed-08c1-4a99-9af0-a8c48c536205.png" width="300" >
        </a>
      </td>
    </tr>
  </tbody>
</table>
