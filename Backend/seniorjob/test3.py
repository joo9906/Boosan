# 앞 2개, 뒤 2개, 앞+뒤 1개씩 뽑아내서 모두 같은 숫자인 경우에는 날릴 수 있고 아니면 못함. 최대 변경 가능 횟수
def solution(A):
    # 처음부터 1개짜리 배열을 줄 수 있으니 그런 경우에는 바로 0
    if len(A) < 2:
        return 0
    
    # 문제 조건에 길이가 1000이고 중복 안ㄴ된다는 말이 없어서 재귀로 밀어넣으면 터짐
    # 따라서 중복되는 배열 + tg가 나오는 경우 한번만 들어가게끔
    visited = set()
    
    # 재귀로 풀어보자
    def cut(current, target_num, cnt):
        nonlocal max_cnt

        # 현재 가지고 있는 배열과 tg를 확인해서 재귀 돌린적 있으면 멈추고 아니면 추가한다음 진행
        now = (tuple(current), target_num)
        if now in visited:
            return
        
        visited.add(now)

        if len(current) < 2:
            # 없애고 나서 재귀 들어왔는데 길이가 1이 된 경우도 cnt를 반환
            max_cnt = max(max_cnt, cnt)
            return
        
        # 앞쪽 2개의 합이 타겟 넘버랑 같다면 없애고 다시 들어감
        if sum(current[:2]) == target_num:
            cut(current[2:], target_num, cnt+1)
        
        # 뒤쪽 2개의 합이 타겟 넘버와 같다면 없애고 cnt + 1
        if sum(current[-2:]) == target_num:
            cut(current[:-2], target_num, cnt+1)
        
        # 앞뒤 끝의 합이 타겟과 같아면 없애고 cnt + 1
        if current[0] + current[-1] == target_num:
            cut(current[1:-1], target_num, cnt+1)

        max_cnt = max(max_cnt, cnt)

    tg_first = sum(A[:2])
    tg_last = sum(A[-2:])
    tg_btw = A[0] + A[-1]

    max_cnt = 0
    cut(A, tg_first, 0)
    cut(A, tg_last, 0)
    cut(A, tg_btw, 0)

    return max_cnt


a = [3, 3]
b = (a, 2)
c = set()
c.add(b)
print(b)


[3, 1, 5, 3, 3, 4, 2]


[4, 1, 4, 3, 3, 2, 5, 2]


[1, 9, 1, 1, 1, 1, 1, 1, 8, 1]


[1, 9, 8, 9, 5, 1, 2]


[1, 1, 2, 3, 1, 2, 2, 1, 1, 2]
