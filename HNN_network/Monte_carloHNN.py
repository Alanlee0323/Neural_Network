import random

def calculate_ber(original_vectors, recovered_vectors):
    total_bits = len(original_vectors[0]) * len(original_vectors)  # 總位元數
    error_bits = 0  # 錯誤位元數

    for original, recovered in zip(original_vectors, recovered_vectors):
        error_bits += sum(o != r for o, r in zip(original, recovered))

    return error_bits / total_bits


def calculate_ber_for_monte_carlo(size, N, iterations, bits_percentage):

    average_ber = 0
    # 計算PI所需的參數
    point_inside_circle = 0  # C的個數
    point_inside_square = 0  # N的個數

    for _ in range(iterations):
        # 步驟1: 生成隨機向量
        random_vectors = [[random.choice([-1, 1]) for _ in range(size)] for _ in range(N)]

        # 步驟2: 初始化權重矩陣並訓練
        weights = [[0 for _ in range(size)] for _ in range(size)]
        for p in random_vectors:
            for i in range(size):
                for j in range(size):
                    if i != j:
                        weights[i][j] += p[i] * p[j]

        # 步驟3: 正規化權重矩陣
        for i in range(size):
            for j in range(size):
                if i != j:
                    weights[i][j] /= len(random_vectors)
                    # weights[i][j] = 1 if weights[i][j] > 0 else -1 if weights[i][j] < 0 else random_vectors[i][j]

        # 步驟4: 添加雜訊
        noisy_patterns = []
        for random_vector in random_vectors:
            noise_pattern = random_vector.copy()
            noise_bits = int(len(noise_pattern) * bits_percentage)
            flip = random.sample(range(len(noise_pattern)), noise_bits)
            for idx in flip:
                noise_pattern[idx] *= -1
            noisy_patterns.append(noise_pattern)

        # 步驟5: 恢復向量
        recovered_vectors = []
        for noisy_pattern in noisy_patterns:
            recovered_vector = [0] * size
            for i in range(size):
                sum_input = sum(noisy_pattern[j] * weights[i][j] for j in range(size) if i != j)
                recovered_vector[i] = 1 if sum_input >= 0 else -1
            recovered_vectors.append(recovered_vector)

        # 計算BER值
        ber = calculate_ber(random_vectors, recovered_vectors)
        average_ber += ber

    return average_ber / iterations

# 使用蒙地卡羅方法計算平均BER
size = 100  # 向量的數量
N = 10  # 向量的長度
iterations = 1 # 蒙地卡羅迭代次數
bits_percentage = 0.0
average_ber = calculate_ber_for_monte_carlo(size, N, iterations, bits_percentage)

print("平均BER值: ", average_ber)

# 寫入文字檔內
output_file = "Monte_carloHNN_OUTPUT.txt"
with open(output_file, 'w') as file:
    file.write(f"Average BER over {iterations} experiments: {average_ber}\n")