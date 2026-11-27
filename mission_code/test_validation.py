import unittest

from mission_code.main import validate_output, MAX_DIFF_LENGTH


class TestValidation(unittest.TestCase):

    # 정상적인 커밋 메시지
    def test_valid_commit(self):
        validate_output(
            "commit",
            "fix: 음수 나이 입력 방지"
        )

    # 잘못된 커밋 유형
    def test_invalid_commit_type(self):
        with self.assertRaises(ValueError):
            validate_output(
                "commit",
                "hello: 나이 입력 수정"
            )

    # 여러 줄의 커밋 메시지
    def test_multiline_commit(self):
        with self.assertRaises(ValueError):
            validate_output(
                "commit",
                "fix: 오류 수정\n추가 설명입니다."
            )

    # 빈 커밋 메시지
    def test_empty_commit(self):
        with self.assertRaises(ValueError):
            validate_output("commit", "")

    # 정상적인 PR 설명
    def test_valid_pr(self):
        text = """
# 학생 클래스 수정

## 변경 요약
학생 클래스 개선

## 주요 변경 사항
나이 입력 검증 추가

## 변경 목적
잘못된 입력 방지

## 테스트
테스트 수행 여부를 확인할 수 없습니다.

## 참고 사항
특이 사항 없음
"""

        validate_output("pr", text)

    # 필수 항목이 누락된 PR 설명
    def test_invalid_pr(self):
        text = """
# 학생 클래스 수정

## 변경 요약
학생 클래스 개선
"""

        with self.assertRaises(ValueError):
            validate_output("pr", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)