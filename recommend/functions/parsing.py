import requests

from user.models import User as UserModel
from place.models import (
    Place as PlaceModel,
    PlaceType as PlaceTypeModel,
    Duration as DurationModel
)
from place.serializers import PlaceAddSerializer

base_parsing_url = 'https://map.naver.com/v5/api/search?caller=pcweb&query='
base_route_url = 'https://map.naver.com/v5/api/transit/directions/point-to-point?start={}, {},placeid= {},name= {}&goal= {}, {},placeid= {},name={}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


# start에서 goal까지 걸리는 이동 시간
def duration_minute(start_index, start_word, goal_index, goal_word, places_info):
    start = parsing(start_index, start_word, places_info)
    goal = parsing(goal_index, goal_word, places_info)

    duration = DurationModel.objects.filter(start_id=start['id'], end_id=goal['id'])
    
    if len(duration) == 0:
        route_url = base_route_url.format(start['x'], start['y'], start['id'], start['name'],
                                          goal['x'], goal['y'], goal['id'], goal['name'])
        data = requests.get(route_url, headers=headers).json()
        if data['paths']:
            duration_time = data['paths'][0]['duration']
        else:
            duration_time = 1


        kinds = ['', '식당', '카페', '숙소']

        index = start_index
        word = start_word
        typename = kinds[index] if kinds[index] != '' else '여행장소'
        placetype = PlaceTypeModel.objects.get(typename=typename)
        start_place = PlaceModel.objects.filter(word=word, placetype=placetype).first()


        index = goal_index
        word = goal_word
        typename = kinds[index] if kinds[index] != '' else '여행장소'
        placetype = PlaceTypeModel.objects.get(typename=typename)
        goal_place = PlaceModel.objects.filter(word=word, placetype=placetype).first()

        duration_temp = {
            'start_id': start['id'],
            'end_id': goal['id'],
            'duration': duration_time
        }

        DurationModel.objects.create(start_place=start_place, end_place=goal_place, **duration_temp)
    else:
        duration_time = duration.first().duration

    return duration_time


# 장소 유형과 검색단어를 입력받아 관련 장소정보를 반환
# index - 0: 여행장소, 1: 식당, 2: 카페, 3: 숙소
# word - 검색단어
# places_info - 여행일정에 포함된 장소 데이터 리스트
# return : DB에 해당 정보 있으면 첫번째 데이터 반환
#          없으면 네이버지도에서 'word kinds[index]'으로 검색하여 상위 첫번째 장소 반환       
def parsing(index, word, places_info):
    kinds = ['', '식당', '카페', '숙소']
    typename = kinds[index] if kinds[index] != '' else '여행장소'

    # DB에서 입력 정보에 해당하는 데이터 검색
    placetype = PlaceTypeModel.objects.get(typename=typename)
    place = PlaceModel.objects.filter(word=word, placetype=placetype)
    if len(place) != 0:
        place = place.first()
        place_info = {
                'id': place._id,
                'name': place.name,
                'x': place.x,
                'y': place.y,
                'address': place.address,
                'word': word,
                'index': index,
            }
    # 없으면 네이버지도에서 입력 정보로 검색, DB에 저장
    else:
        parsing_url = base_parsing_url + word + ' ' + kinds[index]
        data = requests.get(parsing_url, headers=headers).json()
        place = data['result']['place']['list'][0]

        place_info = {
            '_id': place['id'],
            'name': place['name'],
            'x': place['x'],
            'y': place['y'],
            'address': place['address'],
            'word': word,
            'index': index,
        }

        user = UserModel.objects.get(username="admin")
        image = None

        placeadd_serializer = PlaceAddSerializer(data=place_info)

        if placeadd_serializer.is_valid():
            placeadd_serializer.save(user=user,placetype=placetype,image=image)

        place_info['id'] = place_info.pop('_id')

    if place_info not in places_info:
        places_info.append(place_info)

    return place_info


