import sys
import hmac
import hashlib
import base64


def hmac_sha256_hash(value: str, security_key: str) -> str:
    if not value or not security_key:
        return ""

    key_bytes = security_key.encode("utf-8")

    message_bytes = value.encode("utf-8")

    hmac_obj = hmac.new(key_bytes, message_bytes, hashlib.sha256)

    hash_bytes = hmac_obj.digest()

    return base64.b64encode(hash_bytes).decode("utf-8")


def main():
    if len(sys.argv) != 3:
        print("Использование: python create-hash.py <input_file> <security_key>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file + ".hash"

    security_key = sys.argv[2]

    try:
        with open(input_file, "rb") as f:
            file_content = f.read().decode("utf-8")

        hmac_digest = hmac_sha256_hash(file_content, security_key)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(hmac_digest)

        print(f"HMAC-SHA256 успешно вычислен и сохранён в {output_file}")

    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден.")

        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

        sys.exit(1)


if __name__ == "__main__":
    main()
