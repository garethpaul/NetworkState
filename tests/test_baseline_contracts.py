import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "networkstate_check_baseline", ROOT / "scripts/check-baseline.py"
)
CHECK_BASELINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_BASELINE)


class GitignoreContractTests(unittest.TestCase):
    def test_comments_and_leading_whitespace_do_not_create_required_patterns(self):
        source = "# .explore/\n .explore/\n.explore-cache/\n\nDerivedData/\n"

        self.assertEqual(
            CHECK_BASELINE.active_gitignore_patterns(source),
            {" .explore/", ".explore-cache/", "DerivedData/"},
        )


if __name__ == "__main__":
    unittest.main()
