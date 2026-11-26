"""Replay the computer-assisted proof of z(17,17;3,3)=138 using a temporary directory."""
from pathlib import Path
from subprocess import PIPE, Popen, run
from tempfile import TemporaryDirectory

from check_final_cores import finish, lower_bound

HERE = Path(__file__).resolve().parent


def compile_program(name, directory, nauty=False):
    binary = directory / name
    command = ['c++', '-O3', '-std=c++20', str(HERE / (name + '.cpp'))]
    if nauty:
        command.append('-lnauty')
    run(command + ['-o', binary], check=True)
    return binary


def main(directory):
    import sys

    if not __debug__:
        raise RuntimeError('Run with Python assertions enabled')
    lower_bound('witness-138.txt')
    lower_bound('witness-138-six.txt')
    ten = compile_program('ten_border', directory, nauty=True)
    generator = compile_program('six_row_core', directory, nauty=True)
    audit = compile_program('audit_core_catalogue', directory)
    run([sys.executable, HERE/'ten_columns.py'], check=True)
    with Popen([sys.executable, HERE/'ten_cores_139.py'], stdout=PIPE) as cores:
        run([ten], stdin=cores.stdout, check=True)
        assert cores.wait() == 0

    cases = [('column','6',4201,0), ('row','6',29,0),
             ('column','7',671685,2), ('row','7',9396,0), ('column','regular139',12,0)]
    spectra = []
    for mark, border, expected, exceptions in cases:
        path = directory / 'catalogue.txt'
        run([generator,mark,border,'0','3',path,'--catalogue-only'], check=True, stdout=PIPE)
        with path.open() as source:
            log = run([audit,mark,border,'--show'], stdin=source, check=True,
                      text=True, stdout=PIPE).stdout.splitlines()
        assert log[-1].startswith(f'{expected} projections, ')
        assert log[-1].endswith(f', {exceptions} admit a completion before final degree tests')
        print(mark, border, log[-1], flush=True)
        assert len(log)-1 == exceptions
        for line in log[:-1]:
            fields = line.split()
            assert fields[0] == 'core' and (mark,border) == ('column','7')
            prefix = list(map(int, fields[1:10]))
            spectrum = finish(prefix)
            assert spectrum and max(spectrum) < 7
            spectra.append(spectrum)
    assert len(spectra) == 2 and sum(sum(s.values()) for s in spectra) == 3
    print('All three surviving cores accept at most six extra ones. Exact value 138.', flush=True)


if __name__ == '__main__':
    with TemporaryDirectory(prefix='z17-proof-') as tmp:
        main(Path(tmp))
