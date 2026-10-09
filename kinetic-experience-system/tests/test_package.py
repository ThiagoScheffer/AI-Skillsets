"""KX tests require only the Python standard library."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(filename):
    path = ROOT / 'scripts' / filename
    spec = importlib.util.spec_from_file_location(filename.replace('.py', ''), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load('validate_blueprint.py')
skills = load('validate_skills.py')
installer = load('install.py')
auditor = load('audit_repo.py')


class TestBlueprint(unittest.TestCase):
    def setUp(self):
        self.blueprint = json.loads((ROOT / 'examples/blueprints/portfolio.json').read_text())

    def test_all_example_blueprints(self):
        for file in (ROOT / 'examples/blueprints').glob('*.json'):
            with self.subTest(file=file.name):
                self.assertEqual([], validator.validate_blueprint(json.loads(file.read_text())))

    def test_missing_required_field(self):
        bad = copy.deepcopy(self.blueprint)
        del bad['navigation']['focusPolicy']
        self.assertTrue(any('focusPolicy' in e for e in validator.validate_blueprint(bad)))

    def test_duplicate_transition_ids(self):
        bad = copy.deepcopy(self.blueprint)
        bad['transitions'].append(copy.deepcopy(bad['transitions'][0]))
        self.assertTrue(any('duplicate transition' in e for e in validator.validate_blueprint(bad)))

    def test_different_engines_same_property(self):
        bad = copy.deepcopy(self.blueprint)
        p = copy.deepcopy(bad['ownership'][0])
        p['owner'] = 'gsap' if p['owner'] != 'gsap' else 'motion'
        bad['ownership'].append(p)
        self.assertTrue(any('conflicting owners' in e for e in validator.validate_blueprint(bad)))

    def test_invalid_beat_reference(self):
        bad = copy.deepcopy(self.blueprint)
        bad['transitions'][0]['beats'][0]['at'] = 'after:not-defined'
        self.assertTrue(any('missing beat reference' in e for e in validator.validate_blueprint(bad)))


class TestSkills(unittest.TestCase):
    def test_skill_package(self):
        self.assertEqual([], skills.validate(ROOT))


class TestInstaller(unittest.TestCase):
    def test_both_platforms_and_safe_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            tasks = installer.install(target, 'both')
            self.assertEqual(len(tasks), 29)  # 11 skills * 2 + 7 resource dirs
            self.assertTrue((target / '.agents/skills/kx-orchestrator/SKILL.md').is_file())
            self.assertTrue((target / '.claude/skills/kx-orchestrator/SKILL.md').is_file())
            self.assertTrue((target / '.kinetic-experience/schemas/motion-blueprint.schema.json').is_file())
            with self.assertRaises(FileExistsError):
                installer.install(target, 'both')
            installer.install(target, 'both', force=True)

    def test_dry_run_does_not_mutate(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            installer.install(target, 'codex', dry_run=True)
            self.assertEqual(list(target.iterdir()), [])


class TestAudit(unittest.TestCase):
    def test_audit_repo_is_non_mutating(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'package.json').write_text('{"name":"demo","dependencies":{"react-router":"8.0.0","gsap":"3.0.0"}}')
            before = set(root.rglob('*'))
            result = auditor.audit(root)
            self.assertEqual(result['package_name'], 'demo')
            self.assertIn('gsap', result['motion_packages'])
            self.assertEqual(set(root.rglob('*')), before)


if __name__ == '__main__':
    unittest.main()
