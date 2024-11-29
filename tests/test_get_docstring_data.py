# cSpell: disable
import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../src"))
import clig


def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> tuple[str, ...]:
    return ("my", "function")


def adjust_epilog_for_test(text: str) -> str:
    """First and last lines must be always empty"""
    return "\n".join([line.strip() for line in text.splitlines()[1:-1]])


def test_only_description_docstring():
    def foo():
        """A foo that bars"""
        pass

    data = clig.Command(foo, docstring_template=clig.DESCRIPTION_DOCSTRING).get_docstring_data()
    assert data is not None
    assert data.description == "A foo that bars"


def test_numpy_docsring():
    def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> None:
        """Distinctio et ratione sequi hic.

        Blanditiis velit consequatur omnis odit magnam quo dignissimos. Qui ex et illo. Et
        necessitatibus ea placeat consectetur itaque dolore fugiat quo autem. Ut accusamus incidunt
        repellat minima est soluta ut est. Id aut enim ad. Quia qui sint ex eos eveniet eveniet
        earum unde.

        Non rerum aut consectetur ut ducimus ut similique ut illum. Aut qui et distinctio. Nihil id
        sit incidunt minus omnis. Quo unde inventore fuga. Quasi ea ea dolores quam.

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
        pass

    numpy_example_epilog = adjust_epilog_for_test(
        """
        Blanditiis velit consequatur omnis odit magnam quo dignissimos. Qui ex et illo. Et
        necessitatibus ea placeat consectetur itaque dolore fugiat quo autem. Ut accusamus incidunt
        repellat minima est soluta ut est. Id aut enim ad. Quia qui sint ex eos eveniet eveniet
        earum unde.

        Non rerum aut consectetur ut ducimus ut similique ut illum. Aut qui et distinctio. Nihil id
        sit incidunt minus omnis. Quo unde inventore fuga. Quasi ea ea dolores quam.

        Esse temporibus voluptas nulla. Odio voluptas nisi quae cupiditate consequatur cumque ut ex
        dolorem. Est doloremque quis nostrum voluptates doloremque quia. Ex sunt dolores consectetur
        veritatis maxime suscipit. Fugit dolorem facilis quasi.
        """
    )

    data = clig.Command(foo, docstring_template=clig.NUMPY_DOCSTRING).get_docstring_data()
    assert data is not None
    assert data.description == "Distinctio et ratione sequi hic."
    assert data.epilog == numpy_example_epilog
    assert all([p in d for p, d in zip(["a", "b", "c", "d", "e"], data.helps.keys())])
    assert data.helps["a"] == "Neque ut qui non nulla odit esse accusantium aut suscipit."
    assert data.helps["b"] == "Nihil dolores autem autem nulla sit nihil molestiae vero est."
    assert data.helps["c"] == "Animi magnam ut sapiente maiores."
    assert data.helps["d"] == "Consequatur provident neque optio consequatur., by default True"
    assert data.helps["e"] == "Corrupti molestiae in aspernatur., by default None"


def test_sphinx_example():
    def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> None:
        """Qui accusantium harum debitis et.

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
        pass

    sphinx_example_epilog = adjust_epilog_for_test(
        """
        Est nam quia voluptatem vero architecto laborum. Accusantium delectus et aut repudiandae
        voluptatibus qui iure ut debitis. Voluptatibus ut enim consequatur iusto eaque dolor.
        """
    )
    data = clig.Command(foo, docstring_template=clig.SPHINX_DOCSTRING).get_docstring_data()
    assert data is not None
    assert data.description == "Qui accusantium harum debitis et."
    assert data.epilog == sphinx_example_epilog
    assert data.helps["a"] == "Atque pariatur excepturi sed dolorem sint impedit molestiae."
    assert data.helps["b"] == "magni optio voluptatibus"
    assert data.helps["c"] == "Sit eligendi consequatur recusandae doloribus enim amet."
    assert data.helps["d"] == "Soluta dolorum amet et., defaults to True"
    assert data.helps["e"] == "Fugiat provident amet iste natus ab voluptas., defaults to None"


def test_google():
    def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> None:
        """Voluptatum dolorem quis dolorum voluptas atque non temporibus.

        Maiores occaecati quam asperiores non sunt est dolor laborum est. Eius corporis nobis
        accusamus rerum et et et. Ducimus tempore voluptas qui aut consectetur saepe quos cum
        delectus. Tempora adipisci odit qui. Optio eum magni non. Placeat repudiandae quasi nostrum
        mollitia sunt neque fuga id possimus.

        Args:
            a (int): Qui eum eius nihil voluptas quia aut numquam.
            b (str): Quasi voluptates dicta cumque similique qui dolorem architecto.
            c (float): Sint harum et omnis nobis numquam quos omnis.
            d (bool, optional): Ex voluptas animi.. Defaults to True.
            e (list[str] | None, optional): In vero ut nisi officia ut.. Defaults to None.

        Returns:
            tuple[str, ...]: Pariatur aut asperiores aut omnis maxime ratione nemo ut.
        """
        pass

    google_example_epilog = adjust_epilog_for_test(
        """
        Maiores occaecati quam asperiores non sunt est dolor laborum est. Eius corporis nobis
        accusamus rerum et et et. Ducimus tempore voluptas qui aut consectetur saepe quos cum
        delectus. Tempora adipisci odit qui. Optio eum magni non. Placeat repudiandae quasi nostrum
        mollitia sunt neque fuga id possimus.
        """
    )
    data = clig.Command(foo, docstring_template=clig.GOOGLE_DOCSTRING).get_docstring_data()
    assert data is not None
    assert data.description == "Voluptatum dolorem quis dolorum voluptas atque non temporibus."
    assert data.epilog == google_example_epilog
    assert data.helps["a"] == "Qui eum eius nihil voluptas quia aut numquam."
    assert data.helps["b"] == "Quasi voluptates dicta cumque similique qui dolorem architecto."
    assert data.helps["c"] == "Sint harum et omnis nobis numquam quos omnis."
    assert data.helps["d"] == "Ex voluptas animi.. Defaults to True."
    assert data.helps["e"] == "In vero ut nisi officia ut.. Defaults to None."


def test_clig():
    def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> None:
        """Fugit voluptatibus enim odit velit facilis.

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
            Ducimus sunt eum in vel voluptatibus aut facere perspiciatis.

        - `e` (`list[str] | None`, optional): Defaults to `None`.
            Sit et consequatur a asperiores sequi sint dolores id ipsam.

        Returns
        -------
        `tuple[str, ...]`:
            illo odit ut
        """
        pass

    clig_example_epilog = adjust_epilog_for_test(
        """
        Neque dolores expedita repellat in perspiciatis dolorem aliquid et. Commodi fugit minima
        laudantium beatae et ut. Id possimus soluta magnam quisquam laboriosam impedit.

        Ad quaerat ut culpa aut iure id quia. Ut aut alias adipisci quia. Veritatis ratione
        dignissimos laborum. Molestiae molestias id earum.

        Nesciunt quas corrupti tenetur officiis occaecati asperiores eaque. Qui voluptas ut ea dolor
        et harum beatae quos. Est tenetur ut ipsum. Eveniet rem beatae error eum voluptatem tempora
        velit in. Ea doloribus similique.
        """
    )
    data = clig.Command(foo, docstring_template=clig.CLIG_DOCSTRING).get_docstring_data()
    assert data is not None
    assert data.description == "Fugit voluptatibus enim odit velit facilis."
    assert data.epilog == clig_example_epilog
    assert data.helps["a"] == "Quidem natus sunt molestiae et reprehenderit voluptas optio."
    assert data.helps["b"] == "Unde rerum aut a et assumenda fugit dolorem eligendi corrupti."
    assert data.helps["c"] == "Dolorum officiis totam aspernatur fuga voluptas similique."
    assert data.helps["d"] == "Ducimus sunt eum in vel voluptatibus aut facere perspiciatis."
    assert data.helps["e"] == "Sit et consequatur a asperiores sequi sint dolores id ipsam."


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

    def aba(a, b):
        """My function

        My sumary

        Parameters
        ----------
        a : str
            one string
        b : ing
            one int
        """

    def gue(a, b):
        """
        My function

        My sumary

        Parameters
        ----------
        a : str
            one string
        b : ing
            one int

        """

    assert clig.normalize_docstring(foo.__doc__) == clig.normalize_docstring(bar.__doc__)
    assert clig.normalize_docstring(aba.__doc__) == clig.normalize_docstring(gue.__doc__)


def test_inspect():
    def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> None:
        """Fugit voluptatibus enim odit velit facilis.

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
            Ducimus sunt eum in vel voluptatibus aut facere perspiciatis.

        - `e` (`list[str] | None`, optional): Defaults to `None`.
            Sit et consequatur a asperiores sequi sint dolores id ipsam.

        Returns
        -------
        `tuple[str, ...]`:
            illo odit ut
        """
        pass
        assert foo.__doc__ is not None
        assert clig.normalize_docstring(foo.__doc__) == inspect.cleandoc(foo.__doc__)
