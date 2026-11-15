"""Behavioral smoke tests for the opt-in ownership hook."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'hooks' / 'ownership.py'

class GateTest(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name) / 'repo'
        self.root.mkdir()
        subprocess.run(['git','init', '-q', str(self.root)], check=True)
        subprocess.run(['git','-C',str(self.root),'config','user.email','test@example.com'],check=True)
        subprocess.run(['git','-C',str(self.root),'config','user.name','Tester'],check=True)
        (self.root/'README.md').write_text('baseline\n')
        subprocess.run(['git','-C',str(self.root),'add','.'],check=True)
        subprocess.run(['git','-C',str(self.root),'commit','-qm','initial'],check=True)
        self.env = {**os.environ, 'OWNERSHIP_STATE_DIR':str(Path(self.t.name)/'states')}

    def cmd(self, command, extra=None, event=None):
        proc=subprocess.run([sys.executable,str(SCRIPT),command]+(extra or []), cwd=self.root, env=self.env,
                            input=json.dumps(event) if event else None, text=True,capture_output=True)
        return proc

    def event(self, tool='Write', **inp):
        return {'cwd':str(self.root),'tool_name':tool,'tool_input':inp}

    def test_activation_lock_and_manual_next(self):
        self.assertEqual(self.cmd('pre', event=self.event()).returncode,0)
        self.assertEqual(self.cmd('init', ['--budget','5']).returncode,0)
        self.assertEqual(self.cmd('pre', event=self.event()).returncode,2)
        self.assertEqual(self.cmd('pre', event=self.event('Read')).returncode,0)
        self.assertEqual(self.cmd('pre', event=self.event('Bash')).returncode,2)
        self.assertEqual(self.cmd('next',['--label','feature one']).returncode,0)
        self.assertEqual(self.cmd('pre', event=self.event('Write',content='a\nb\n')).returncode,0)
        (self.root/'new.py').write_text('a\nb\nc\nd\ne\n')
        self.assertEqual(self.cmd('post',event=self.event()).returncode,0)
        self.assertIn('locked',self.cmd('status').stdout)
        self.assertEqual(self.cmd('next').returncode,1)
        self.assertEqual(self.cmd('resume').returncode,1)

    def test_resume_after_early_stop(self):
        self.assertEqual(self.cmd('init',['--budget','20']).returncode,0)
        self.assertEqual(self.cmd('next',['--label','feature one']).returncode,0)
        self.assertEqual(self.cmd('stop',event=self.event('')).returncode,0)
        self.assertIn('open',self.cmd('status').stdout)
        (self.root/'new.py').write_text('a\n')
        self.assertEqual(self.cmd('stop',event=self.event('')).returncode,0)
        self.assertIn('locked',self.cmd('status').stdout)
        self.assertEqual(self.cmd('resume').returncode,0)
        self.assertIn('open',self.cmd('status').stdout)
        subprocess.run(['git','-C',str(self.root),'add','.'],check=True)
        subprocess.run(['git','-C',str(self.root),'commit','-qm','slice'],check=True)
        self.assertEqual(self.cmd('next',['--label','feature two']).returncode,0)
        self.assertEqual(self.cmd('off').returncode,0)
        self.assertEqual(self.cmd('pre',event=self.event()).returncode,0)

    def test_large_single_write_preblocked(self):
        self.assertEqual(self.cmd('init',['--budget','3']).returncode,0)
        self.assertEqual(self.cmd('next').returncode,0)
        self.assertEqual(self.cmd('pre',event=self.event('Write',content='\n'.join('x' for _ in range(5)))).returncode,2)

if __name__ == '__main__':
    unittest.main()
