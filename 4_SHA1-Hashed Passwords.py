import hashlib
import itertools

def calculate_sha1(password: str) -> str:
    """计算字符串的SHA1哈希值，返回40位十六进制字符串（匹配文档中SHA1算法的应用场景）"""
    # 按UTF-8编码转换为字节流，计算SHA1哈希并转为小写（哈希大小写不敏感）
    return hashlib.sha1(password.encode('utf-8')).hexdigest().lower()

def crack_sha1_from_keyboard():
    # 1. 文档中明确的关键参数
    TARGET_HASH = "67ae1a64661ac8b4494666f58c4822408dd0a3e4".lower()  # 泄露的管理员密码SHA1哈希
    # 2. 文档德语键盘有指纹的可打印候选字符（排除功能键，仅保留可能的密码字符）、
    CANDIDATE_CHARS = "QqWw%58(=0Ii*+nN"
    # 3. 常见管理员密码长度范围（4-8位，平衡破解效率与覆盖性）
    PASSWORD_LENGTH_RANGE = range(4, 9)

    print(f"开始破解文档中的SHA1哈希：{TARGET_HASH}")
    print(f"候选字符集（来自德语键盘指纹）：{CANDIDATE_CHARS}")
    print(f"尝试密码长度：{PASSWORD_LENGTH_RANGE.start}~{PASSWORD_LENGTH_RANGE.stop-1}位")

    # 遍历可能的密码长度
    for length in PASSWORD_LENGTH_RANGE:
        print(f"\n正在尝试{length}位密码...")
        # 生成该长度下所有候选字符的组合
        for combo in itertools.product(CANDIDATE_CHARS, repeat=length):
            password = ''.join(combo)
            current_hash = calculate_sha1(password)
            # 比对哈希值
            if current_hash == TARGET_HASH:
                print(f"✅ 破解成功！文档中管理员的原始密码：{password}")
                return password

    print(f"❌ 未找到匹配密码（可尝试调整密码长度范围或核对候选字符集）")
    return None

# 执行破解
if __name__ == "__main__":
    crack_sha1_from_keyboard()