import random


#計算BER的函式
def calculate_ber(original_vectors, recovered_vectors):
    total_bits = len(original_vectors[0]) * len(original_vectors)
    error_bits = 0

    for original, recovered in zip(original_vectors, recovered_vectors):
        print("原始向量:", original, "恢復後向量:", recovered)  
        error_bits += sum(o != r for o, r in zip(original, recovered))

    return error_bits / total_bits

#----------------------------------------------------------------------------------------------------------

size = 100  # 向量的數量
N = 3  # 向量的長度

weights = [[0 for _ in range(size)] for _ in range(size)]  # 初始化權重為0
# print(weights)
random_vectors = [[random.choice([-1, 1]) for _ in range(size)] for _ in range(N)]
# print(random_vectors)

for p in random_vectors:
    print("訓練用 patterns", p)
    for i in range(size):   #pattern row
        for j in range(size):  #pattern column
            if i != j:
                weights[i][j] += p[i] * p[j]

# 產生T矩陣
for i in range(size):
    for j in range(size):
        if i != j:  # 保留對角線上的0值
            weights[i][j] /= len(random_vectors)
            # weights[i][j] = 1 if weights[i][j] > 0 else -1 if weights[i][j] < 0 else random_vectors[i][j]

print("T矩陣: ",weights)

noisy_patterns = []  # 用於存儲所有經過破壞的向量

for random_vector in random_vectors:
    noise_pattern = random_vector.copy()
    noise_bits = int(len(noise_pattern) * 0.4)  # 要破壞的比例
    print("破壞了", noise_bits, "個bits")
    flip = random.sample(range(len(noise_pattern)), noise_bits)

    for idx in flip:
        noise_pattern[idx] *= -1  # 翻轉神經元的狀態

    noisy_patterns.append(noise_pattern)  # 添加經過破壞的向量到列表


print("破壞後的向量:", noisy_patterns)


recovered_vectors = []
for noisy_pattern in noisy_patterns:
    recovered_vector = [0] * size  # 初始化恢復後的向量
    for i in range(size):
        sum_input = 0
        for j in range(size):
            if i != j:  # 忽略自連接
                sum_input += noisy_pattern[j] * weights[i][j]
        recovered_vector[i] = 1 if sum_input >= 0 else -1
    recovered_vectors.append(recovered_vector) 

# print("恢復後的向量: ")
# for vector in recovered_vectors:
#     print(vector)

# 計算BER值
ber = calculate_ber(random_vectors, recovered_vectors)
print("BER值: ", ber)
