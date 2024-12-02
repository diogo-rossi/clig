# cSpell: disable
import sys
from pathlib import Path
from argparse import BooleanOptionalAction

this_dir = Path(__file__).parent

sys.path.insert(0, str((this_dir).resolve()))
sys.path.insert(0, str((this_dir / "../src").resolve()))
sys.path.insert(0, str((this_dir / "../src").resolve()))
from clig import Command, CompleteKeywordArguments, normalize_docstring
import functions as fun


def test_inferarg_simple():
    cmd = Command(fun.posNoType_kwNoType)
    arg_1, arg_2 = cmd.argument_data
    assert cmd.inferarg(arg_1) == (
        (),
        CompleteKeywordArguments(
            action="store",
            dest="first",
            type=str,
            default=None,
            nargs=None,
            choices=None,
            help=None,
        ),
    )
    assert cmd.inferarg(arg_2) == (
        ("--second",),
        CompleteKeywordArguments(
            action="store",
            dest="second",
            type=str,
            default="test",
            nargs=None,
            choices=None,
            help=None,
        ),
    )


def test_inferarg_with_types():
    cmd = Command(fun.posNoType_poslWithType_kwWithType)
    arg_a, arg_b, arg_c = cmd.argument_data
    assert cmd.inferarg(arg_a) == (
        (),
        CompleteKeywordArguments(
            action="store",
            dest="a",
            type=str,
            default=None,
            nargs=None,
            choices=None,
            help=None,
        ),
    )
    assert cmd.inferarg(arg_b) == (
        (),
        CompleteKeywordArguments(
            action="store",
            dest="b",
            type=float,
            default=None,
            nargs=None,
            choices=None,
            help=None,
        ),
    )
    assert cmd.inferarg(arg_c) == (
        ("--c",),
        CompleteKeywordArguments(
            action="store",
            dest="c",
            type=int,
            default=123,
            nargs=None,
            choices=None,
            help=None,
        ),
    )


def test_inferarg_with_types_and_helps():
    cmd = Command(fun.posWithType_kwWithType_kwBoolWithType_cligDocMultiline)
    arg_a, arg_b, arg_c = cmd.argument_data
    assert cmd.inferarg(arg_a) == (
        (),
        CompleteKeywordArguments(
            action="store",
            dest="a",
            type=str,
            default=None,
            nargs=None,
            choices=None,
            help=arg_a.help,
        ),
    )
    assert cmd.inferarg(arg_b) == (
        ("--b",),
        CompleteKeywordArguments(
            action="store",
            dest="b",
            type=int,
            default=123,
            nargs=None,
            choices=None,
            help=arg_b.help,
        ),
    )
    assert cmd.inferarg(arg_c) == (
        ("--c",),
        CompleteKeywordArguments(
            action="store_false",
            dest="c",
            default=True,
            help=arg_c.help,
        ),
    )


def test_inferarg_with_types_and_metadata():
    cmd = Command(fun.posWithMetadataWithFlags_posWithMetadata_kwBool)
    arg_a, arg_b, arg_c = cmd.argument_data
    assert cmd.inferarg(arg_a) == (
        ("-f", "--first"),
        CompleteKeywordArguments(
            dest="a",
            default=None,
            nargs=None,
            required=True,
            choices=None,
            action="store",
            type=str,
            help="The first argument",
        ),
    )
    assert cmd.inferarg(arg_b) == (
        (),
        CompleteKeywordArguments(
            dest="b",
            action="store_const",
            default=None,
            const=123,
            help=None,
        ),
    )
    assert cmd.inferarg(arg_c) == (
        ("--c",),
        CompleteKeywordArguments(
            dest="c",
            help=None,
            default=True,
            action="store_false",
        ),
    )


def test_inferarg_with_types_and_numpy_doc():
    cmd = Command(fun.posWithType_posWithType_posWithType_kwBoolWithType_optKwListWithType_numpyDocMultiline)
    args_a, args_b, args_c, args_d, args_e = cmd.argument_data
    assert cmd.inferarg(args_a) == (
        (),
        CompleteKeywordArguments(
            dest="a",
            default=None,
            action="store",
            type=int,
            nargs=None,
            choices=None,
            help=normalize_docstring(
                """Fuga nemo provident vero odio qui sint et aut veritatis. Facere necessitatibus ut. Voluptatem
                natus natus veritatis earum. Reprehenderit voluptate dolorem dolores consequuntur magnam impedit
                eius. Est ut nisi aut accusamus."""
            ),
        ),
    )
    assert cmd.inferarg(args_b) == (
        (),
        CompleteKeywordArguments(
            dest="b",
            default=None,
            action="store",
            type=str,
            nargs=None,
            choices=None,
            help="Culpa asperiores incidunt molestias aliquam soluta voluptas excepturi nulla.",
        ),
    )


def test_inferarg_posWithType_posBoolWithType_cligDoc():
    cmd = Command(fun.posWithType_posBoolWithType_cligDoc)
    arg_name, arg_flag = cmd.argument_data
    assert cmd.inferarg(arg_name) == (
        (),
        CompleteKeywordArguments(
            dest="name",
            default=None,
            action="store",
            type=str,
            nargs=None,
            choices=None,
            help="Sequi deserunt est quia qui.",
        ),
    )
    assert cmd.inferarg(arg_flag) == (
        ("--flag",),
        CompleteKeywordArguments(
            dest="flag",
            default=None,
            action=BooleanOptionalAction,
            required=True,
            help="Labore eius et voluptatem quos et consequatur dolores.",
        ),
    )
