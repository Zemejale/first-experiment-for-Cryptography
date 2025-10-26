import base64

def hamming_distance(a: bytes, b: bytes) -> int:
    """计算两个字节串的汉明距离（不同位的数量）"""
    distance = 0
    for x, y in zip(a, b):
        xor = x ^ y
        distance += bin(xor).count("1")  # 统计异或结果中1的位数
    return distance

def score_plaintext(plaintext: bytes) -> float:
    """评估明文的“英文自然度”（基于可打印字符、空格频率）"""
    if not plaintext:
        return 0.0
    # 可打印ASCII字符占比
    printable_ratio = len([c for c in plaintext if 32 <= c <= 126]) / len(plaintext)
    # 空格频率（英文文本中空格占比约15%，权重更高）
    space_freq = plaintext.count(32) / len(plaintext) if len(plaintext) > 0 else 0
    # 字母频率（大小写合并，统计a-z/A-Z占比）
    letter_count = sum(1 for c in plaintext if (65 <= c <= 90) or (97 <= c <= 122))
    letter_freq = letter_count / len(plaintext) if len(plaintext) > 0 else 0
    # 综合得分：可打印占比*0.3 + 空格频率*0.5 + 字母频率*0.2
    return printable_ratio * 0.3 + space_freq * 0.5 + letter_freq * 0.2

def find_single_key(ciphertext: bytes) -> tuple[int, bytes]:
    """破解单字节XOR：找到使明文最“像英文”的密钥字节"""
    best_score = -1.0
    best_key = 0
    best_plaintext = b""
    for key_byte in range(256):
        plaintext = bytes([b ^ key_byte for b in ciphertext])
        score = score_plaintext(plaintext)
        if score > best_score:
            best_score = score
            best_key = key_byte
            best_plaintext = plaintext
    return best_key, best_plaintext

def find_key_length(ciphertext: bytes, max_length: int = 40) -> int:
    """检测密钥长度：通过汉明距离归一化值筛选最可能的长度"""
    distances = {}
    for key_length in range(2, max_length + 1):
        # 取前4个等长块（长度为key_length）
        chunks = [
            ciphertext[i:i+key_length] 
            for i in range(0, 4 * key_length, key_length) 
            if i + key_length <= len(ciphertext)
        ]
        if len(chunks) < 2:
            continue
        # 计算所有块对的汉明距离，取平均后归一化
        total_distance = 0
        pair_count = 0
        for i in range(len(chunks)):
            for j in range(i + 1, len(chunks)):
                total_distance += hamming_distance(chunks[i], chunks[j])
                pair_count += 1
        if pair_count == 0:
            continue
        avg_distance = total_distance / pair_count
        normalized_distance = avg_distance / key_length
        distances[key_length] = normalized_distance
    # 按归一化距离升序排序，取最可能的长度
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    return sorted_distances[0][0] if sorted_distances else 2  # 默认返回最小长度2

def decrypt_repeating_key_xor(base64_cipher: str) -> str:
    """解密流程：Base64解码→找密钥长度→转置分块→单字节破解→拼接密钥→解密"""
    # 1. Base64解码为字节串
    ciphertext = base64.b64decode(base64_cipher)
    
    # 2. 检测密钥长度
    key_length = find_key_length(ciphertext)
    print(f"[+] 检测到可能的密钥长度: {key_length}")
    
    # 3. 转置分块：将密文按密钥长度分组，再按位置转置
    transposed_blocks = [[] for _ in range(key_length)]
    for i, byte in enumerate(ciphertext):
        transposed_blocks[i % key_length].append(byte)
    transposed_blocks = [bytes(block) for block in transposed_blocks]
    
    # 4. 对每个转置块，用单字节XOR破解密钥字节
    key = []
    for block in transposed_blocks:
        key_byte, _ = find_single_key(block)
        key.append(key_byte)
    key = bytes(key)
    print(f"[+] 恢复的密钥: {key.decode('ascii', errors='replace')}")
    
    # 5. 用密钥解密整个密文
    plaintext = bytes([ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext))])
    return plaintext.decode('ascii', errors='ignore')

if __name__ == "__main__":
    # 替换为实际的Base64密文（例如从文件读取或直接赋值）
    base64_cipher = """
    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
    """
    plaintext = decrypt_repeating_key_xor(base64_cipher)
    print("\n[+] 解密后的明文:")
    print(plaintext)