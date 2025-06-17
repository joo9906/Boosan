from django.test import TestCase
from collections import deque
# Create your tests here.
from collections import deque

def solution(maps):
    n, m = len(maps[0]), len(maps)
    visited = [[False] * n for _ in range(m)]
    delta = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    check = 0
    for dx, dy in delta:
        ex = n + dx
        ey = m + dy
        if 0 <= ex < n and 0 <= ey < m and maps[ex][ey] == 0:
            check +=1
    if check >= 2:
        return -1
    
    q = deque([])
    q.append((1, 0, 0))
    
    answer = 100000
    
    while q:
        cnt, y, x = q.popleft()

        if x == n-1 and y == m-1:
            answer = min(answer, cnt)
        
        for dy, dx in delta:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < m and visited[ny][nx] == False and maps[ny][nx] == 1:
                q.append((cnt+1, ny, nx))
                visited[ny][nx] = True

    return answer

maps = [[1,0,1,1,1],[1,0,1,0,1],[1,0,1,1,1],[1,1,1,0,1],[0,0,0,0,1]]
print(solution(maps))