# 무비렌즈 데이터를 이용한 추천 시스템(recommendation system)

>###  사용한 언어&프레임워크
> * Python
>  * DjangoDB
>  * HTML
>  * CSS
>  * javascripts

-----

넷플릭스, 왓챠 등 추천시스템을 활용하는 업체들을 표본해서 이상형 월드컵을 이용하여 [필터버블][1]을 최소화하고, 접근성을 높였다.

추천시스템에는 크게 [콘텐츠 기반 추천][2]과 [최 이웃 기반 추천][2], [잠재요인 추천][2][^잠재요인]이 있다.

---
먼저, [무비렌즈][3]데이터를 가지고 가공하여 이용할 데이터를 추렸다. 이후, 각 컨텐츠 기반 추천시스템을 구현하고, 함수화를 진행했다. 그 다음, DjangoDB로 넘어와 웹상에서 구현할 수 있게 진행했다.

HTML과 CSS를 주로 사용했으며, javascripts에 대한 이해가 낮아 많이 사용하지는 못했다.




[1]:(https://terms.naver.com/entry.nhn?docId=5807275&cid=59277&categoryId=65525)
[2]:(https://john-analyst.medium.com/%EC%B6%94%EC%B2%9C-%EC%8B%9C%EC%8A%A4%ED%85%9C-recommendation-system-%EC%9D%B4%EB%9E%80-111e315f8256)

[^잠재요인]: 가장 정확도가 높았지만, 적용과 이해가 어려워 코드 사용만 하고 실제로 구현에 쓰지는 못했다.
