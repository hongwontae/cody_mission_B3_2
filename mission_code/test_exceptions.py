import unittest
import subprocess
import requests
import io

from unittest.mock import patch
from contextlib import redirect_stderr

from mission_code.main import main, MAX_DIFF_LENGTH


class TestExceptions(unittest.TestCase):

    def setUp(self):
        self.env_patch = patch.dict(
            "os.environ",
            {"FREE_OPEN_API_KEY": "test-api-key"}
        )

        self.args_patch = patch(
            "sys.argv",
            ["main.py", "commit"]
        )

        self.env_patch.start()
        self.args_patch.start()

        self.addCleanup(self.env_patch.stop)
        self.addCleanup(self.args_patch.stop)

    # Git diff 입력 길이 초과
    @patch("main.call_ai")
    @patch("main.get_git_diff")
    def test_diff_too_large(self, mock_diff, mock_ai):
        mock_diff.return_value = "a" * (MAX_DIFF_LENGTH + 1)

        output = io.StringIO()

        with redirect_stderr(output):
            result = main()

        self.assertEqual(result, 1)
        self.assertIn("Git diff가 너무 큽니다.", output.getvalue())

        mock_ai.assert_not_called()

    # API 응답 시간 초과
    @patch("main.requests.post")
    @patch("main.get_git_diff")
    def test_api_timeout(self, mock_diff, mock_post):
        mock_diff.return_value = "-int age = 10;\n+int age = 20;"

        mock_post.side_effect = requests.exceptions.Timeout(
            "테스트용 Timeout"
        )

        output = io.StringIO()

        with redirect_stderr(output):
            result = main()

        self.assertEqual(result, 1)
        self.assertIn("API 응답 시간 초과", output.getvalue())

    # Git 명령 실행 시간 초과
    @patch("main.subprocess.run")
    def test_git_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["git", "diff", "--cached"],
            timeout=10
        )

        output = io.StringIO()

        with redirect_stderr(output):
            result = main()

        self.assertEqual(result, 1)
        self.assertIn("Git 명령 실행 시간 초과", output.getvalue())

    # Git 미설치 상황
    @patch("main.subprocess.run")
    def test_git_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError()

        output = io.StringIO()

        with redirect_stderr(output):
            result = main()

        self.assertEqual(result, 1)
        self.assertIn("Git이 설치되어 있지 않습니다.", output.getvalue())

    # 네트워크 연결 실패
    @patch("main.requests.post")
    @patch("main.get_git_diff")
    def test_connection_error(self, mock_diff, mock_post):
        mock_diff.return_value = "-int age = 10;\n+int age = 20;"

        mock_post.side_effect = requests.exceptions.ConnectionError(
            "테스트용 연결 오류"
        )

        output = io.StringIO()

        with redirect_stderr(output):
            result = main()

        self.assertEqual(result, 1)
        self.assertIn("API 요청 실패", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)