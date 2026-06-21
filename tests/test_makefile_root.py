import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MakefileRootTests(unittest.TestCase):
    def hosted_commands(self, root=ROOT):
        workflow = (root / ".github/workflows/check.yml").read_text(encoding="utf-8")
        commands = []
        lines = workflow.splitlines()
        index = 0
        while index < len(lines):
            match = re.match(r"^      - run: (.*)$", lines[index])
            if not match:
                index += 1
                continue
            value = match.group(1)
            if value != "|":
                commands.append(value)
                index += 1
                continue
            index += 1
            block = []
            while index < len(lines) and lines[index].startswith("          "):
                block.append(lines[index][10:])
                index += 1
            commands.append("\n".join(block))
        self.assertTrue(commands, workflow)
        return "\n".join(commands)

    def write_hosted_fixture(self, root, makefile):
        (root / "scripts").mkdir(parents=True)
        (root / "tests").mkdir()
        (root / "Makefile").write_text(makefile, encoding="utf-8")
        expected_makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        (root / "scripts/check-baseline.py").write_text(
            "from pathlib import Path\n"
            "import sys\n"
            "root = Path(__file__).resolve().parents[1]\n"
            "print('REAL_HOSTED_POLICY')\n"
            f"expected = {expected_makefile!r}\n"
            "if (root / 'Makefile').read_text(encoding='utf-8') != expected:\n"
            "    print('hosted policy rejected Makefile mutation', file=sys.stderr)\n"
            "    raise SystemExit(1)\n",
            encoding="utf-8",
        )
        (root / "tests/test_smoke.py").write_text(
            "import unittest\n\n"
            "class Smoke(unittest.TestCase):\n"
            "    def test_real_python_tests(self):\n"
            "        print('REAL_PYTHON_TESTS')\n"
            "        self.assertTrue(True)\n",
            encoding="utf-8",
        )
        (root / "build.sh").write_text("#!/bin/sh\necho REAL_PROJECT_CHECK\n", encoding="utf-8")
        (root / "build.sh").chmod(0o755)

    def run_make(self, *arguments, environment=None):
        with tempfile.TemporaryDirectory(prefix="networkstate make path ") as directory:
            root = Path(directory)
            checkout = root / "checkout [hostile] 'quote"
            checkout.mkdir()
            makefile = checkout / "Makefile"
            shutil.copyfile(ROOT / "Makefile", makefile)
            external = root / "external caller"
            external.mkdir()
            env = os.environ.copy()
            if environment:
                env.update(environment)
            result = subprocess.run(
                ["make", "--no-print-directory", "-n", "-f", str(makefile), *arguments],
                cwd=external,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            return result, str(checkout)

    def test_all_aliases_preserve_spaced_absolute_makefile_path(self):
        for target in ("check", "lint", "static-check", "test", "build", "verify"):
            for name, arguments, environment in (
                ("none", (target,), None),
                ("command", (target, "ROOT=/tmp/attacker-root"), None),
                ("environment", (target,), {"ROOT": "/tmp/attacker-root"}),
            ):
                with self.subTest(target=target, override=name):
                    result, checkout = self.run_make(*arguments, environment=environment)
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertIn(checkout, result.stdout)
                    self.assertNotIn("/tmp/attacker-root", result.stdout)

    def test_command_line_makefile_list_override_fails_closed(self):
        result, _ = self.run_make("check", "MAKEFILE_LIST=/tmp/attacker/Makefile")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stderr)

    def test_environment_makefile_list_override_fails_closed(self):
        result, _ = self.run_make(
            "-e", "check", environment={"MAKEFILE_LIST": "/tmp/attacker/Makefile"}
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stderr)

    def test_hosted_sequence_rejects_make_authority_bypasses(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        mutations = {
            "duplicate global root": "\noverride ROOT := $(CURDIR)/fake-root\n",
            "duplicate target root": "\nstatic-check: override ROOT := $(CURDIR)/fake-root\n",
            "recipe override": "\nstatic-check:\n\t@echo FAKE_CHECK_OVERRIDE\n",
            "combined recipe and root": (
                "\nstatic-check:\n\t@echo FAKE_CHECK_OVERRIDE\n"
                "\ntest: override ROOT := $(CURDIR)/fake-root\n"
            ),
        }
        with tempfile.TemporaryDirectory(prefix="networkstate hosted policy ") as directory:
            temporary_root = Path(directory)
            for name, mutation in mutations.items():
                with self.subTest(name=name):
                    checkout = temporary_root / name
                    checkout.mkdir()
                    self.write_hosted_fixture(checkout, makefile + mutation)
                    fake_root = checkout / "fake-root"
                    fake_root.mkdir()
                    (fake_root / "build.sh").write_text(
                        "#!/bin/sh\necho FAKE_PROJECT_CHECK\n", encoding="utf-8"
                    )
                    (fake_root / "build.sh").chmod(0o755)

                    result = subprocess.run(
                        ["/bin/sh", "-e", "-c", self.hosted_commands()],
                        cwd=checkout,
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                    self.assertNotEqual(0, result.returncode, result.stdout)
                    self.assertIn("REAL_HOSTED_POLICY", result.stdout)
                    self.assertIn("hosted policy rejected Makefile mutation", result.stderr)
                    self.assertNotIn("FAKE_CHECK_OVERRIDE", result.stdout)
                    self.assertNotIn("FAKE_PROJECT_CHECK", result.stdout)

    def test_hosted_sequence_ignores_caller_shell(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="networkstate hosted shell ") as directory, tempfile.TemporaryDirectory(
            prefix="networkstate-shell-"
        ) as tool_directory:
            checkout = Path(directory) / "checkout with spaces 'quote' [hostile]"
            checkout.mkdir()
            self.write_hosted_fixture(checkout, makefile)
            fake_shell_log = Path(tool_directory) / "fake-shell-ran"
            fake_shell = Path(tool_directory) / "fake-shell"
            fake_shell.write_text(
                "#!/bin/sh\n"
                f"printf invoked > {str(fake_shell_log)!r}\n"
                "exit 0\n",
                encoding="utf-8",
            )
            fake_shell.chmod(0o755)
            environment = os.environ.copy()
            environment["SHELL"] = str(fake_shell)
            environment["MAKEFLAGS"] = "SHELL={}".format(fake_shell)

            result = subprocess.run(
                ["/bin/sh", "-e", "-c", self.hosted_commands()],
                cwd=checkout,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("REAL_HOSTED_POLICY", result.stdout)
            self.assertIn("REAL_PYTHON_TESTS", result.stdout)
            self.assertIn("REAL_PROJECT_CHECK", result.stdout)
            self.assertFalse(fake_shell_log.exists())

    def test_make_aliases_do_not_trust_python_from_path(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        targets = ("check", "lint", "static-check", "test", "build", "verify")
        with tempfile.TemporaryDirectory(prefix="networkstate fake python ") as directory:
            root = Path(directory)
            checkout = root / "checkout"
            external = root / "external caller"
            tools = root / "tools"
            checkout.mkdir()
            external.mkdir()
            tools.mkdir()
            self.write_hosted_fixture(checkout, makefile)
            fake_python_log = root / "fake-python-ran"
            fake_python = tools / "python3"
            fake_python.write_text(
                "#!/bin/sh\n"
                f"printf 'fake python %s\\n' \"$*\" >> {str(fake_python_log)!r}\n"
                "exit 0\n",
                encoding="utf-8",
            )
            fake_python.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = str(tools) + os.pathsep + environment["PATH"]

            for target in targets:
                with self.subTest(target=target):
                    if fake_python_log.exists():
                        fake_python_log.unlink()
                    result = subprocess.run(
                        [
                            "make",
                            "--no-print-directory",
                            "-f",
                            str(checkout / "Makefile"),
                            target,
                        ],
                        cwd=external,
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertIn("REAL_HOSTED_POLICY", result.stdout)
                    self.assertIn("REAL_PYTHON_TESTS", result.stdout)
                    self.assertFalse(fake_python_log.exists(), fake_python_log.read_text() if fake_python_log.exists() else "")

    def test_python_entrypoints_ignore_pythonpath_startup_code(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="networkstate pythonpath ") as directory:
            root = Path(directory)
            checkout = root / "checkout"
            startup = root / "startup"
            checkout.mkdir()
            startup.mkdir()
            self.write_hosted_fixture(checkout, makefile)
            marker = root / "sitecustomize-ran"
            (startup / "sitecustomize.py").write_text(
                "import os\n"
                "from pathlib import Path\n"
                "Path(os.environ['NETWORKSTATE_STARTUP_MARKER']).write_text('ran\\n')\n"
                "os._exit(0)\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(startup)
            environment["NETWORKSTATE_STARTUP_MARKER"] = str(marker)

            make_result = subprocess.run(
                ["make", "--no-print-directory", "-f", str(checkout / "Makefile"), "check"],
                cwd=root,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, make_result.returncode, make_result.stderr)
            self.assertIn("REAL_HOSTED_POLICY", make_result.stdout)
            self.assertIn("REAL_PYTHON_TESTS", make_result.stdout)
            self.assertFalse(marker.exists())

            hosted_result = subprocess.run(
                ["/bin/sh", "-e", "-c", self.hosted_commands()],
                cwd=checkout,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, hosted_result.returncode, hosted_result.stderr)
            self.assertIn("REAL_HOSTED_POLICY", hosted_result.stdout)
            self.assertIn("REAL_PYTHON_TESTS", hosted_result.stdout)
            self.assertIn("REAL_PROJECT_CHECK", hosted_result.stdout)
            self.assertFalse(marker.exists())

    def test_make_aliases_do_not_trust_command_line_or_makeflags_shell(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        targets = ("check", "lint", "static-check", "test", "build", "verify")
        with tempfile.TemporaryDirectory(prefix="networkstate-fake-shell-") as directory:
            root = Path(directory)
            checkout = root / "checkout"
            external = root / "external caller"
            tools = root / "tools"
            checkout.mkdir()
            external.mkdir()
            tools.mkdir()
            self.write_hosted_fixture(checkout, makefile)
            fake_shell = tools / "fake-shell"
            fake_shell.write_text(
                "#!/bin/sh\n"
                "printf 'fake shell %s\\n' \"$*\" >> \"$FAKE_SHELL_LOG\"\n"
                "exit 0\n",
                encoding="utf-8",
            )
            fake_shell.chmod(0o755)

            for target in targets:
                for channel in ("command line", "MAKEFLAGS"):
                    with self.subTest(target=target, channel=channel):
                        fake_shell_log = root / f"fake-shell-{target}-{channel.replace(' ', '-')}.log"
                        environment = os.environ.copy()
                        environment["FAKE_SHELL_LOG"] = str(fake_shell_log)
                        arguments = [
                            "make",
                            "--no-print-directory",
                            "-f",
                            str(checkout / "Makefile"),
                            target,
                        ]
                        if channel == "command line":
                            arguments.append(f"SHELL={fake_shell}")
                        else:
                            environment["MAKEFLAGS"] = f"SHELL={fake_shell}"

                        result = subprocess.run(
                            arguments,
                            cwd=external,
                            env=environment,
                            capture_output=True,
                            text=True,
                            check=False,
                        )

                        self.assertEqual(0, result.returncode, result.stderr)
                        self.assertIn("REAL_HOSTED_POLICY", result.stdout)
                        self.assertIn("REAL_PYTHON_TESTS", result.stdout)
                        self.assertFalse(fake_shell_log.exists(), fake_shell_log.read_text() if fake_shell_log.exists() else "")

    def test_contract_keeps_additional_makefiles_outside_local_make_trust_boundary(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertNotIn(".SECONDEXPANSION", makefile)
        self.assertNotIn("MAKEFILE_LIST_GUARD", makefile)

        docs = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in [
                "README.md",
                "SECURITY.md",
                "AGENTS.md",
                "CHANGES.md",
                "docs/plans/2026-06-21-spaced-makefile-path.md",
            ]
        )
        for phrase in [
            "additional `-f` Makefiles are caller-supplied Make programs",
            "outside the local Make trust boundary",
            "hosted direct workflow remains authoritative",
        ]:
            self.assertIn(phrase, docs)
        for overclaim in [
            "reject additional `-f`",
            "additional `-f` Makefiles before",
            "recipe replacement were rejected",
            "before a replaced recipe can claim success",
        ]:
            self.assertNotIn(overclaim, docs)

    def test_hosted_direct_chain_rejects_repository_mutation_before_make(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        commands = self.hosted_commands()
        self.assertNotIn("make ", commands)
        self.assertNotIn("make\n", commands)
        with tempfile.TemporaryDirectory(prefix="networkstate hosted direct mutation ") as directory:
            checkout = Path(directory) / "checkout"
            checkout.mkdir()
            self.write_hosted_fixture(
                checkout,
                makefile + "\ncheck:\n\t@echo MAKE_WOULD_CLAIM_SUCCESS\n",
            )

            result = subprocess.run(
                ["/bin/sh", "-e", "-c", commands],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(0, result.returncode, result.stdout)
            self.assertIn("REAL_HOSTED_POLICY", result.stdout)
            self.assertIn("hosted policy rejected Makefile mutation", result.stderr)
            self.assertNotIn("MAKE_WOULD_CLAIM_SUCCESS", result.stdout)

    def test_workflow_rejects_authority_mutations(self):
        workflow = (ROOT / ".github/workflows/check.yml").read_text(encoding="utf-8")
        mutations = {
            "job environment": workflow.replace(
                "    runs-on: macos-15\n",
                "    runs-on: macos-15\n    env:\n      PATH: .:${{ env.PATH }}\n",
            ),
            "step environment": workflow.replace(
                "      - run: |\n",
                "      - env:\n          PATH: .:${{ env.PATH }}\n        run: |\n",
            ),
            "extra step": workflow + "      - run: echo extra\n",
            "custom shell": workflow.replace(
                "      - run: |\n",
                "      - shell: python\n        run: |\n",
            ),
            "command addition": workflow.replace(
                "          /bin/sh ./build.sh\n",
                "          echo injected\n          /bin/sh ./build.sh\n",
            ),
        }
        with tempfile.TemporaryDirectory(prefix="networkstate workflow policy ") as directory:
            for name, mutated_workflow in mutations.items():
                with self.subTest(name=name):
                    checkout = Path(directory) / name
                    shutil.copytree(
                        ROOT,
                        checkout,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
                    )
                    (checkout / ".github/workflows/check.yml").write_text(
                        mutated_workflow, encoding="utf-8"
                    )
                    result = subprocess.run(
                        ["/usr/bin/python3", "-I", "-B", "scripts/check-baseline.py"],
                        cwd=checkout,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertNotEqual(0, result.returncode, result.stdout)
                    self.assertIn("exact reviewed workflow", result.stderr)

    def test_hosted_sequence_rejects_checked_in_native_tools(self):
        with tempfile.TemporaryDirectory(prefix="networkstate hosted tools ") as directory:
            checkout = Path(directory) / "checkout"
            shutil.copytree(
                ROOT,
                checkout,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            workflow_path = checkout / ".github/workflows/check.yml"
            malicious_workflow = workflow_path.read_text(encoding="utf-8").replace(
                "    runs-on: macos-15\n",
                "    runs-on: macos-15\n    env:\n      PATH: .:${{ env.PATH }}\n",
            )
            workflow_path.write_text(malicious_workflow, encoding="utf-8")
            (checkout / "tests/test_makefile_root.py").write_text(
                "import unittest\n\n"
                "class Smoke(unittest.TestCase):\n"
                "    def test_policy_completed(self): self.assertTrue(True)\n",
                encoding="utf-8",
            )
            fake_tool_log = checkout / "fake-native-tool-ran"
            for tool in ("xcrun", "xcodebuild"):
                tool_path = checkout / tool
                tool_path.write_text(
                    "#!/bin/sh\n"
                    f"printf '%s\\n' {tool} >> {str(fake_tool_log)!r}\n"
                    "exit 0\n",
                    encoding="utf-8",
                )
                tool_path.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = ".{}{}".format(os.pathsep, environment["PATH"])

            result = subprocess.run(
                ["/bin/sh", "-e", "-c", self.hosted_commands(checkout)],
                cwd=checkout,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(0, result.returncode, result.stdout)
            self.assertIn("exact reviewed workflow", result.stderr)
            self.assertFalse(fake_tool_log.exists())


if __name__ == "__main__":
    unittest.main()
