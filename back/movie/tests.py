# 아이디 : user1, 2, 3, 4 ...
# 비번 : 잉글릭스123
import json
# from django.contrib.auth.hashers import make_password
from datetime import datetime
import random

# 비밀번호 해시 생성 (실제 Django에서 사용하는 것과 동일한 방식)
# hashed_password = "pbkdf2_sha256$600000$hYITuBcHxHuBejSL$t3IlO0NEt0/kNPFJ3dAaCFEQKv9z6CcC+8I3RK6z1r4=" # dldrmfflrtm123의 해시값
hashed_password = "pbkdf2_sha256$600000$65bRy55NocFFoZPk9j0kSZ$RfgRj2YpsnzsTrwx0gilwBBbHjEY4whMizvWFe1veVA="

# 닉네임 생성을 위한 리스트
adjectives = ['즐거운', '행복한', '신나는', '슬기로운', '똑똑한', '열정적인', '활기찬', '든든한',
              '귀여운', '멋진', '무서운', '발랄한', '졸린', '슬픈', '화가난', '정의로운', '잘생긴', '못생긴', '아기']
nouns = ['사자', '호랑이', '토끼', '거북이', '코끼리', '팬더', '고양이', '강아지',
         '여우', '늑대', '얼룩말', '문어', '상어', '고래', '비둘기', '까치', '독수리', '돼지']

last_name = ['김', '이', '박', '최', '정', '강', '조',
             '윤', '장', '임', '오', '한', '서', '신', '권']
first_name = [
    '민수', '영희', '철수', '지혜', '현우', '수민', '하준', '서연', '도윤', '서현',
    '유진', '지훈', '채원', '민재', '다은', '승민', '예진', '준혁', '해준', '소연',
    '도현', '시우', '아라', '지호', '하율', '은서', '태윤', '가영', '우진', '다연'
]

users = []
current_id = 1

# Bronze tier (40명): 0-9 points
for i in range(40):
    users.append({
        "model": "accounts.user",
        "pk": current_id,
        "fields": {
            "password": hashed_password,
            "last_login": None,
            "is_superuser": False,
            "username": f"user{current_id}",
            "first_name": random.choice(first_name),
            "last_name": random.choice(last_name),
            "email": "",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-01-01T00:00:00Z",
            "level": "Beginner",
            "goal": "SAT",
            "prefer_genre": "Action",
            "points": random.randint(0, 9),  # 0-9 points
            "tier": "Bronze",
            "nickname": f"{adjectives[i % 10]}{nouns[i % 10]}{random.randint(1, 9999)}",
            "bio": "영어 공부 열심히 하겠습니다!"
        }
    })
    current_id += 1

# Silver tier (30명): 10-49 points
for i in range(30):
    users.append({
        "model": "accounts.user",
        "pk": current_id,
        "fields": {
            "password": hashed_password,
            "last_login": None,
            "is_superuser": False,
            "username": f"user{current_id}",
            "first_name": random.choice(first_name),
            "last_name": random.choice(last_name),
            "email": "",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-01-01T00:00:00Z",
            "level": "Beginner",
            "goal": "SAT",
            "prefer_genre": "Action",
            "points": random.randint(10, 49),  # 10-49 points
            "tier": "Silver",
            "nickname": f"{adjectives[(i+3) % 10]}{nouns[(i+5) % 10]}{random.randint(1, 9999)}",
            "bio": "영어 공부 열심히 하겠습니다!"
        }
    })
    current_id += 1

# Gold tier (15명): 50-100 points
for i in range(15):
    users.append({
        "model": "accounts.user",
        "pk": current_id,
        "fields": {
            "password": hashed_password,
            "last_login": None,
            "is_superuser": False,
            "username": f"user{current_id}",
            "first_name": random.choice(first_name),
            "last_name": random.choice(last_name),
            "email": "",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-01-01T00:00:00Z",
            "level": "Beginner",
            "goal": "SAT",
            "prefer_genre": "Action",
            "points": random.randint(50, 99),  # 50-99 points
            "tier": "Gold",
            "nickname": f"{adjectives[(i+6) % 10]}{nouns[(i+2) % 10]}{random.randint(1, 9999)}",
            "bio": "영어 공부 열심히 하겠습니다!"
        }
    })
    current_id += 1

# Platinum tier (8명): 100-299 points
for i in range(8):
    users.append({
        "model": "accounts.user",
        "pk": current_id,
        "fields": {
            "password": hashed_password,
            "last_login": None,
            "is_superuser": False,
            "username": f"user{current_id}",
            "first_name": random.choice(first_name),
            "last_name": random.choice(last_name),
            "email": "",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-01-01T00:00:00Z",
            "level": "Beginner",
            "goal": "SAT",
            "prefer_genre": "Action",
            "points": random.randint(100, 299),  # 100-299 points
            "tier": "Platinum",
            "nickname": f"{adjectives[(i+1) % 10]}{nouns[(i+7) % 10]}{random.randint(1, 9999)}",
            "bio": "영어 공부 열심히 하겠습니다!"
        }
    })
    current_id += 1

# Diamond tier (5명): 300-499 points
for i in range(5):
    users.append({
        "model": "accounts.user",
        "pk": current_id,
        "fields": {
            "password": hashed_password,
            "last_login": None,
            "is_superuser": False,
            "username": f"user{current_id}",
            "first_name": random.choice(first_name),
            "last_name": random.choice(last_name),
            "email": "",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-01-01T00:00:00Z",
            "level": "Beginner",
            "goal": "SAT",
            "prefer_genre": "Action",
            "points": random.randint(300, 499),  # 300-499 points
            "tier": "Diamond",
            "nickname": f"{adjectives[(i+4) % 10]}{nouns[(i+8) % 10]}{random.randint(1, 9999)}",
            "bio": "영어 공부 열심히 하겠습니다!"
        }
    })
    current_id += 1

# Ruby tier (2명): 500+ points
for i in range(2):
    users.append({
        "model": "accounts.user",
        "pk": current_id,
        "fields": {
            "password": hashed_password,
            "last_login": None,
            "is_superuser": False,
            "username": f"user{current_id}",
            "first_name": random.choice(first_name),
            "last_name": random.choice(last_name),
            "email": "",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2024-01-01T00:00:00Z",
            "level": "Beginner",
            "goal": "SAT",
            "prefer_genre": "Action",
            "points": random.randint(500, 700),  # 500+ points
            "tier": "Ruby",
            "nickname": f"{adjectives[(i+9) % 10]}{nouns[(i+4) % 10]}{random.randint(1, 9999)}",
            "bio": "영어 공부 열심히 하겠습니다!"
        }
    })
    current_id += 1

# JSON 파일로 저장
with open('users.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, ensure_ascii=False, indent=2)
