#!/usr/bin/env python3
"""Run all 5 verification checks + generate all figures. Writes results to stdout and a log file.

   Usage: uv run python scripts/run_all.py [--log results.log]
"""

import argparse, subprocess, sys, os, datetime

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)

# (script_name, extra_args) — extra_args added after the script name
CHECKS = [
    ('plot_graph',     ['--cells', '8', '--channels', '3']),
    ('check_qubo',     ['--cells', '8', '--channels', '3']),
    ('check_qaoa',     ['--cells', '8', '--channels', '3', '--maxiter', '120', '--nruns', '3']),
    ('check_dynamics', ['--cells', '8', '--channels', '3', '--maxiter', '25', '--snapshots', '5']),
    ('check_encoding', []),   # uses its own internal combos
    ('check_scale',    ['--cells', '10', '--channels', '3', '--maxiter', '40']),
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--log', default='results.log')
    args = p.parse_args()

    log_path = os.path.join(PROJECT_ROOT, args.log)
    started = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    lines = []

    def emit(s):
        print(s)
        lines.append(s)

    emit(f'{"=" * 70}')
    emit(f'ISIT 2026 QHack — Verification Run')
    emit(f'Started: {started}')
    emit(f'{"=" * 70}')

    passed = 0
    failed = 0
    for name, extra_args in CHECKS:
        emit(f'\n{"─" * 50}')
        emit(f'Running: {name}')
        emit(f'{"─" * 50}')

        script = os.path.join(SCRIPTS_DIR, f'{name}.py')
        env = os.environ.copy()
        env['PYTHONPATH'] = PROJECT_ROOT
        cmd = [sys.executable, script] + extra_args
        r = subprocess.run(cmd, cwd=PROJECT_ROOT, env=env,
                           capture_output=True, text=True, timeout=600)

        for line in r.stdout.splitlines():
            if line.strip():
                emit(f'  {line}')
        if r.stderr.strip():
            for line in r.stderr.splitlines()[-5:]:
                emit(f'  [stderr] {line}')

        if r.returncode != 0:
            emit(f'  >>> FAILED (exit {r.returncode})')
            failed += 1
        elif 'PASS' in r.stdout:
            emit(f'  >>> PASS')
            passed += 1
        else:
            emit(f'  >>> DONE')
            passed += 1

    finished = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emit(f'\n{"=" * 70}')
    emit(f'Finished: {finished}')
    emit(f'Results: {passed} passed, {failed} failed out of {len(CHECKS)}')
    emit(f'{"=" * 70}')

    # Write log
    with open(log_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'\nLog saved: {log_path}')

    # List generated figures
    emit('\nGenerated figures:')
    for f in sorted(os.listdir(PROJECT_ROOT)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(PROJECT_ROOT, f))
            emit(f'  {f}  ({sz:,} bytes)')

    return 1 if failed > 0 else 0


if __name__ == '__main__':
    raise SystemExit(main())
