import random

def estimate_pi(iterations):
    point_circle = 0  # C的個數
    point_square = 0  # N的個數

    for _ in range(iterations):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        distance = x**2 + y**2
        if distance <= 1:
            point_circle += 1
        point_square += 1

    return 4 * point_circle / point_square

iterations = 100

# 使用蒙地卡羅方法估算PI值
pi = estimate_pi(iterations)
print(f"The PI is {pi}")

# 寫入文字檔內
output_file = "Monte_carlo_pi_OUTPUT.txt"
with open(output_file, 'w') as file:
    file.write(f"PI value over {iterations} experiments:{pi}\n")