# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(Board):
    n = len(Board)
    m = len(Board[0])
    max_num = 0
    visited = [[False] * m for _ in range(n)] # 방문한곳 재사용 X
    
    delta = [(0, 1), (1, 0), (0, -1), (-1, 0)] # 2차원 배열이므로 델타로 탐색

    def dfs(x, y, arr, depth):
        nonlocal max_num

        #총 4자리수를 만들었으면 합쳐서 정수형으로 다시 변환(0을 넣으려고 할 떄 정수로 넣으면 안되니까 문자형으로 넣었음)
        if depth == 4: 
            num = int(''.join(arr))
            max_num = max(max_num, num)
            return

        #델타 돌면서 범위 내에 있고 방문 X면 arr에 추가하고 다음꺼 찾으러 감
        for dx, dy in delta:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 < ny < m and visited[nx][ny] == False:
                visited[nx][ny] = True
                dfs(nx, ny, arr + [str(Board[nx][ny])], depth + 1)
                visited[nx][ny] = False
    
    # Board의 모든 좌표를 시작점으로 잡아서 돌려보고 만들 수 있는 가장 큰 수를 반환
    for i in range(n):
        for j in range(m):
            visited[i][j] = True
            dfs(i, j, [str(Board[i][j])], 1)
            visited[i][j] = False
    
    return max_num


a2 = [[9, 1, 1, 0, 7], [1, 0, 2, 1, 0], [1, 9, 1, 1, 0]]
b2 = [[1, 1, 1], [1, 3, 4], [1, 4, 3]]
c2 = [[0, 1, 5, 0, 0]]
d = [[0, 1, 5, 0], [0, 0, 0, 0]]

print(solution(a2))
print(solution(b2))
print(solution(c2))
print(solution(d))

    