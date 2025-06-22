import csv
import json

# 중복 user_id를 가진 User 객체를 찾아 하나만 남기고 나머지는 삭제하는 스크립트
if __name__ == "__main__":
    from account.models import User
    from collections import Counter

    user_ids = list(User.objects.values_list('user_id', flat=True))
    dupes = [item for item, count in Counter(user_ids).items() if count > 1]
    print("중복 user_id:", dupes)

    for uid in dupes:
        users = User.objects.filter(user_id=uid)
        print(f"user_id={uid} -> ids: {[u.id for u in users]}")
        # 첫 번째만 남기고 나머지 삭제
        for u in users[1:]:
            print(f"Deleting user id={u.id}, user_id={u.user_id}")
            u.delete()

