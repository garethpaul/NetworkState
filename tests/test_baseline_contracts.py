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
    def test_commented_patterns_are_not_active(self):
        source = "# .explore/\n.explore-cache/\n\nDerivedData/\n"

        self.assertEqual(
            CHECK_BASELINE.active_gitignore_patterns(source),
            {".explore-cache/", "DerivedData/"},
        )


if __name__ == "__main__":
    unittest.main()
