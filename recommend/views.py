import random
import sqlite3
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import MovieData , TopMovie, RecUser, WorldCup
from django.contrib.auth.models import User
from django.db.models import Q
from .contentsRec import content_recommend, item_based_recommend
# Create your views here.

def worldcup(request):
    username = str(request.user) #세션으로부터 유저네임 가져오기
    if request.method == 'POST':
        bestmovie_id = int(request.POST.get('bestMovie'))
        try : #같은 유저거나 같은 무비면 변화한 값만 업데이트
            recU = RecUser.objects.get(userName=username)
            recU.bestMovie = bestmovie_id
            recU.save()
            check = 1
        except :
            U = User.objects.get(username=username) # 회원가입시 생성된 테이블에서 유저네임과 같은 레코드를 쿼리 : html에 id를 넣어주기 위해서!
            user = get_object_or_404(User, pk=U.id) # 위와 같음 : 한번 더 하는 이유는 저장할때 밀어넣어주기 위헤..
            bestmovie = RecUser(userId = user, userName=request.POST.get('userName'), bestMovie=bestmovie_id)
            bestmovie.save() #valid안하고 그냥 save # 저장하려는 모델이 외래키로 만들어져서 꼭 상위모델을 넣어줘야한다.
            check = 1
        if check == 1:
            try:
                M = WorldCup.objects.get(movieId=bestmovie_id)
                M.championCount += 1
                M.save()
            except:
                M = WorldCup(movieId = bestmovie_id, championCount = 1)
                M.save()
        return redirect('index') # 인덱스 홈페이지로 이동하기전에 함수처리시간보고 worldcup.html에서 시간을 끌어야할듯

    else :
        if username != 'AnonymousUser': #로그인했을
            U = User.objects.get(username=username)
            userId = U.id
            top_movie = list(TopMovie.objects.all())
            random.shuffle(top_movie)
            top_movie = top_movie[:32]
            context = {'top_movie' : top_movie, 'userName': username, 'userId' : userId} #같이 데이터를 던져줌
            return render(request, 'recommend/worldcup.html',context)
        return render(request, 'accounts/login.html') #로그인 안되어있다면 로그인페이지로 이동시키기


def index(request):
    #userID
    username = request.user
    if str(username) != 'AnonymousUser':
        try:
            recU = RecUser.objects.get(userName=username) #이상형 월드컵을 한적이 있는지 검사
            userId = recU.userId_id #userID
            best_movie_id = recU.bestMovie
            contents = content_recommend(best_movie_id)
            item_contents = item_based_recommend(best_movie_id)

            movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')
            worldcup_df = pd.DataFrame(list(WorldCup.objects.all().values())).sort_values('championCount',ascending=False)



            best_movie = movies_df.loc[best_movie_id]

            sim_genre_movie = movies_df.loc[contents['genre'].values].sort_values('vote_count',ascending=False)
            director_movie = movies_df.loc[contents['director_movie'].values].sort_values('vote_count',ascending=False)
            actor1_movie = movies_df.loc[contents['actor1_movie'].values].sort_values('vote_count',ascending=False)
            actor2_movie = movies_df.loc[contents['actor2_movie'].values].sort_values('vote_count',ascending=False)
            worldcup_df = movies_df.loc[worldcup_df['movieId'].values][:6]
            item_movie = movies_df.loc[item_contents['item_movie'].values].sort_values('vote_count',ascending=False)


            sim_genre_list = [i[1] for i in sim_genre_movie.iterrows()]
            director_list = [i[1] for i in director_movie.iterrows()]
            actor1_list = [i[1] for i in actor1_movie.iterrows()]
            actor2_list = [i[1] for i in actor2_movie.iterrows()]
            worldcup_list = [i[1] for i in worldcup_df.iterrows()]
            item_movie_list = [i[1] for i in item_movie.iterrows()]

            context = {
            'best_movie' : best_movie ,
            'sim_genre_list' : sim_genre_list ,
            'director_list' : director_list,
            'actor1' : contents['actor1'],
            'actor2' : contents['actor2'],
            'actor1_list' : actor1_list,
            'actor2_list' : actor2_list,
            'worldcup_list' : worldcup_list,
            'item_movie_list' : item_movie_list,
             }

            return render(request,'recommend/index.html',context)
        except : #없다면 이상형월드컵 강제로 보내버리기
            return redirect('recommend:worldcup')
    return render(request, 'recommend/AnonymousUser.html') #로그인 안한 유저라면 인덱스에서 뭘 보여줄지 구상하기


def rating(request):
    rating_movie = TopMovie.objects.all

    context = {
        'rating_movie' : rating_movie
    }
    return render(request,'recommend/rating.html',context)
