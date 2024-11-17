import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../src"))
import clig

google_example = """Voluptatum dolorem quis dolorum voluptas atque non temporibus temporibus porro.

    Maiores occaecati quam asperiores non sunt est dolor laborum est. Eius corporis nobis accusamus
    rerum et et et. Ducimus tempore voluptas qui aut consectetur saepe quos cum delectus. Tempora
    adipisci odit qui. Optio eum magni non. Placeat repudiandae quasi nostrum mollitia sunt neque
    fuga id possimus.

    Args:
        a (int): Qui eum eius nihil voluptas quia aut numquam.
        b (str): Quasi voluptates dicta cumque similique qui dolorem architecto dolorum nesciunt.
        c (float): Sint harum et omnis nobis numquam quos omnis.
        d (bool, optional): Ex voluptas animi.. Defaults to True.
        e (list[str] | None, optional): In vero ut nisi officia ut.. Defaults to None.

    Returns:
        tuple[str, ...]: Pariatur aut asperiores aut omnis maxime ratione nemo ut.
    """

clig_example = """Fugit voluptatibus enim odit velit facilis.

    Neque dolores expedita repellat in perspiciatis dolorem aliquid et. Commodi fugit minima
    laudantium beatae et ut. Id possimus soluta magnam quisquam laboriosam impedit.

    Ad quaerat ut culpa aut iure id quia. Ut aut alias adipisci quia. Veritatis ratione
    dignissimos laborum. Molestiae molestias id earum.

    Nesciunt quas corrupti tenetur officiis occaecati asperiores eaque. Qui voluptas ut ea dolor
    et harum beatae quos. Est tenetur ut ipsum. Eveniet rem beatae error eum voluptatem tempora
    velit in. Ea doloribus similique.

    Parameters
    ----------
    - `a` (`int`):
        Quidem natus sunt molestiae et reprehenderit voluptas optio.

    - `b` (`str`):
        Unde rerum aut a et assumenda fugit dolorem eligendi corrupti.

    - `c` (`float`):
        Dolorum officiis totam aspernatur fuga voluptas similique.

    - `d` (`bool`, optional): Defaults to `True`.
        Ducimus sunt eum in vel voluptatibus aut facere perspiciatis voluptas.

    - `e` (`list[str] | None`, optional): Defaults to `None`.
        Sit et consequatur a asperiores sequi sint dolores id ipsam.

    Returns
    -------
    `tuple[str, ...]`:
        illo odit ut
    """


def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> tuple[str, ...]:
    return ("my", "function")


def test_numpy_docsring():
    numpy_example = """Distinctio et ratione sequi hic.

        Blanditiis velit consequatur omnis odit magnam quo dignissimos. Qui ex et illo. Et
        necessitatibus ea placeat consectetur itaque dolore fugiat quo autem. Ut accusamus incidunt
        repellat minima est soluta ut est. Id aut enim ad. Quia qui sint ex eos eveniet eveniet earum
        unde.

        Non rerum aut consectetur ut ducimus ut similique ut illum. Aut qui et distinctio. Nihil id sit
        incidunt minus omnis. Quo unde inventore fuga. Quasi ea ea dolores quam.

        Esse temporibus voluptas nulla. Odio voluptas nisi quae cupiditate consequatur cumque ut ex
        dolorem. Est doloremque quis nostrum voluptates doloremque quia. Ex sunt dolores consectetur
        veritatis maxime suscipit. Fugit dolorem facilis quasi.

        Parameters
        ----------
        a : int
            Neque ut qui non nulla odit esse accusantium aut suscipit.
        b : str
            Nihil dolores autem autem nulla sit nihil molestiae vero est.
        c : float
            Animi magnam ut sapiente maiores.
        d : bool, optional
            Consequatur provident neque optio consequatur., by default True
        e : list[str] | None, optional
            Corrupti molestiae in aspernatur., by default None

        Returns
        -------
        tuple[str, ...]
            Numquam maiores atque doloribus.
        """
    numpy_example_epilog = """
        Blanditiis velit consequatur omnis odit magnam quo dignissimos. Qui ex et illo. Et
        necessitatibus ea placeat consectetur itaque dolore fugiat quo autem. Ut accusamus incidunt
        repellat minima est soluta ut est. Id aut enim ad. Quia qui sint ex eos eveniet eveniet earum
        unde.

        Non rerum aut consectetur ut ducimus ut similique ut illum. Aut qui et distinctio. Nihil id sit
        incidunt minus omnis. Quo unde inventore fuga. Quasi ea ea dolores quam.

        Esse temporibus voluptas nulla. Odio voluptas nisi quae cupiditate consequatur cumque ut ex
        dolorem. Est doloremque quis nostrum voluptates doloremque quia. Ex sunt dolores consectetur
        veritatis maxime suscipit. Fugit dolorem facilis quasi."""
    numpy_example_epilog = "\n".join(
        [line.strip() for line in numpy_example_epilog.splitlines()[1:]]
    )
    data = clig.get_docstring_data(
        parameter_number=5,
        docstring=numpy_example,
        template=clig.NUMPY_DOCSTRING,
    )
    assert data is not None
    assert data.description == "Distinctio et ratione sequi hic."
    assert data.epilog == numpy_example_epilog
    assert all([p in d for p, d in zip(["a", "b", "c", "d", "e"], data.parameters.keys())])
    assert data.parameters["a"] == "Neque ut qui non nulla odit esse accusantium aut suscipit."
    assert data.parameters["b"] == "Nihil dolores autem autem nulla sit nihil molestiae vero est."
    assert data.parameters["c"] == "Animi magnam ut sapiente maiores."
    assert data.parameters["d"] == "Consequatur provident neque optio consequatur., by default True"
    assert data.parameters["e"] == "Corrupti molestiae in aspernatur., by default None"


def test_sphinx_example():
    sphinx_example = """Qui accusantium harum debitis et.

        Est nam quia voluptatem vero architecto laborum. Accusantium delectus et aut repudiandae
        voluptatibus qui iure ut debitis. Voluptatibus ut enim consequatur iusto eaque dolor.

        :param a: Atque pariatur excepturi sed dolorem sint impedit molestiae.
        :type a: int
        :param b: magni optio voluptatibus
        :type b: str
        :param c: Sit eligendi consequatur recusandae doloribus enim amet.
        :type c: float
        :param d: Soluta dolorum amet et., defaults to True
        :type d: bool, optional
        :param e: Fugiat provident amet iste natus ab voluptas., defaults to None
        :type e: list[str] | None, optional
        :return: Beatae perspiciatis ut in incidunt vitae.
        :rtype: tuple[str, ...]
        """
    sphinx_example_epilog = """
        Est nam quia voluptatem vero architecto laborum. Accusantium delectus et aut repudiandae
        voluptatibus qui iure ut debitis. Voluptatibus ut enim consequatur iusto eaque dolor."""
    sphinx_example_epilog = "\n".join(
        [line.strip() for line in sphinx_example_epilog.splitlines()[1:]]
    )
    data = clig.get_docstring_data(
        parameter_number=5,
        docstring=sphinx_example,
        template=clig.SPHINX_DOCSTRING,
    )
    assert data is not None
    assert data.description == "Qui accusantium harum debitis et."
    assert data.epilog == sphinx_example_epilog
    assert data.parameters["a"] == "Atque pariatur excepturi sed dolorem sint impedit molestiae."
    assert data.parameters["b"] == "magni optio voluptatibus"
    assert data.parameters["c"] == "Sit eligendi consequatur recusandae doloribus enim amet."
    assert data.parameters["d"] == "Soluta dolorum amet et., defaults to True"
    assert data.parameters["e"] == "Fugiat provident amet iste natus ab voluptas., defaults to None"


def test_normalize_docstring():
    def foo():
        """A multi-line
        docstring.
        """

    def bar():
        """
        A multi-line
        docstring.
        """

    assert clig.normalize_docstring(foo.__doc__) == clig.normalize_docstring(bar.__doc__)
