import pytest
import clig
from resources import CapSys

help_msg_ex13 = """
usage: main [-h] [-b BAR] foo

positional arguments:
  foo

options:
  -h, --help         show this help message and exit
  -b BAR, --bar BAR
""".strip()


def test_ex13(capsys: CapSys):
    """https://clig.readthedocs.io/en/latest/notebooks/advancedfeatures.html#using-make-shorts"""

    def main(foo: str, bar: int = 42):
        return locals()

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--help"], make_shorts=True)

    assert e.value.code == 0
    output = capsys.readouterr().out.strip()
    assert output in help_msg_ex13

    assert clig.run(main, ["test", "--bar", "45"], make_shorts=True) == {"foo": "test", "bar": 45}
    assert clig.run(main, ["test", "-b", "13"], make_shorts=True) == {"foo": "test", "bar": 13}


help_msg_ex14 = """
usage: main [-h] -f FOO [-b BAR]

options:
  -h, --help         show this help message and exit
  -f FOO, --foo FOO
  -b BAR, --bar BAR
""".strip()


def test_ex14(capsys: CapSys):

    def main(foo: str, bar: int = 42):
        return locals()

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--help"], make_shorts=True, make_flags=True)

    assert e.value.code == 0
    output = capsys.readouterr().out.strip()
    assert output in help_msg_ex14

    assert clig.run(main, ["--foo", "test", "--bar", "45"], make_flags=True, make_shorts=True) == {
        "foo": "test",
        "bar": 45,
    }
    assert clig.run(main, ["-f", "test", "-b", "13"], make_flags=True, make_shorts=True) == {
        "foo": "test",
        "bar": 13,
    }


help_msg_ex15 = """
usage: main [-h] [-f FILE] [-F FILENAME] [-fi FILEDIR] [-FI FILEPATH]
            [-fn FILE_NAME] [-fd FILE_DIR] [-fp FILE_PATH] [-fo FOLDER]
            [-FO FOLDERNAME] [-fol FOLDERDIR] [-FOL FOLDERPATH]
            [-fona FOLDER_NAME] [-fodi FOLDER_DIR] [-fopa FOLDER_PATH]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE
  -F FILENAME, --filename FILENAME
  -fi FILEDIR, --filedir FILEDIR
  -FI FILEPATH, --filepath FILEPATH
  -fn FILE_NAME, --file-name FILE_NAME
  -fd FILE_DIR, --file-dir FILE_DIR
  -fp FILE_PATH, --file-path FILE_PATH
  -fo FOLDER, --folder FOLDER
  -FO FOLDERNAME, --foldername FOLDERNAME
  -fol FOLDERDIR, --folderdir FOLDERDIR
  -FOL FOLDERPATH, --folderpath FOLDERPATH
  -fona FOLDER_NAME, --folder-name FOLDER_NAME
  -fodi FOLDER_DIR, --folder-dir FOLDER_DIR
  -fopa FOLDER_PATH, --folder-path FOLDER_PATH
""".strip()


def test_ex15(capsys: CapSys):
    def main(
        file: str = ".",
        filename: str = ".",
        filedir: str = ".",
        filepath: str = ".",
        file_name: str = ".",
        file_dir: str = ".",
        file_path: str = ".",
        folder: str = ".",
        foldername: str = ".",
        folderdir: str = ".",
        folderpath: str = ".",
        folder_name: str = ".",
        folder_dir: str = ".",
        folder_path: str = ".",
    ): ...

    with pytest.raises(SystemExit) as e:
        clig.run(main, ["--help"], make_shorts=True)

    assert e.value.code == 0
    output = capsys.readouterr().out.strip()
    assert output in help_msg_ex15
