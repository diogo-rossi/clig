# cSpell: disable
import os
import sys
import pytest

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

    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == "A foo that bars"


def test_only_description_long_docstring():
    def foo():
        """Aliquam alias quia earum.

        Corporis ullam nam ut dolores sed. Nemo ea deserunt facere numquam velit aut. Architecto provident
        consequatur ratione est quas qui dolor ratione. Laudantium fugit at.

        Ullam et temporibus eum. Sit voluptatem tempora totam dolores. Pariatur accusamus voluptate totam.
        Fugit rerum nemo reiciendis veritatis modi sit distinctio ratione id.

        Voluptates tenetur quos qui exercitationem laudantium aliquid. Neque qui eum qui. Qui tenetur facilis
        non voluptatem ut corporis harum fugiat.
        """
        pass

    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == clig.normalize_docstring(foo.__doc__)


@pytest.mark.xfail(raises=AssertionError, reason="\nError expected: 'Description Only' is found before\n\n")
def test_only_description_and_epilog_docstring():
    def foo():
        """Aliquam alias quia earum.

        Corporis ullam nam ut dolores sed. Nemo ea deserunt facere numquam velit aut. Architecto provident
        consequatur ratione est quas qui dolor ratione. Laudantium fugit at.

        Ullam et temporibus eum. Sit voluptatem tempora totam dolores. Pariatur accusamus voluptate totam.
        Fugit rerum nemo reiciendis veritatis modi sit distinctio ratione id.

        Voluptates tenetur quos qui exercitationem laudantium aliquid. Neque qui eum qui. Qui tenetur facilis
        non voluptatem ut corporis harum fugiat.
        """
        pass

    nopar_example_epilog = adjust_epilog_for_test(
        """
        Corporis ullam nam ut dolores sed. Nemo ea deserunt facere numquam velit aut. Architecto provident
        consequatur ratione est quas qui dolor ratione. Laudantium fugit at.

        Ullam et temporibus eum. Sit voluptatem tempora totam dolores. Pariatur accusamus voluptate totam.
        Fugit rerum nemo reiciendis veritatis modi sit distinctio ratione id.

        Voluptates tenetur quos qui exercitationem laudantium aliquid. Neque qui eum qui. Qui tenetur facilis
        non voluptatem ut corporis harum fugiat.
        """
    )

    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == "Aliquam alias quia earum."
    assert data.epilog == nopar_example_epilog


def test_numpy_docstring():
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

    data = clig.Command(foo).get_inferred_docstring_data()
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
    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == "Qui accusantium harum debitis et."
    assert data.epilog == sphinx_example_epilog
    assert data.helps["a"] == "Atque pariatur excepturi sed dolorem sint impedit molestiae."
    assert data.helps["b"] == "magni optio voluptatibus"
    assert data.helps["c"] == "Sit eligendi consequatur recusandae doloribus enim amet."
    assert data.helps["d"] == "Soluta dolorum amet et., defaults to True"
    assert data.helps["e"] == "Fugiat provident amet iste natus ab voluptas., defaults to None"


def test_google_docstring():
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
    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == "Voluptatum dolorem quis dolorum voluptas atque non temporibus."
    assert data.epilog == google_example_epilog
    assert data.helps["a"] == "Qui eum eius nihil voluptas quia aut numquam."
    assert data.helps["b"] == "Quasi voluptates dicta cumque similique qui dolorem architecto."
    assert data.helps["c"] == "Sint harum et omnis nobis numquam quos omnis."
    assert data.helps["d"] == "Ex voluptas animi.. Defaults to True."
    assert data.helps["e"] == "In vero ut nisi officia ut.. Defaults to None."


def test_clig_docstring():
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
    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == "Fugit voluptatibus enim odit velit facilis."
    assert data.epilog == clig_example_epilog
    assert data.helps["a"] == "Quidem natus sunt molestiae et reprehenderit voluptas optio."
    assert data.helps["b"] == "Unde rerum aut a et assumenda fugit dolorem eligendi corrupti."
    assert data.helps["c"] == "Dolorum officiis totam aspernatur fuga voluptas similique."
    assert data.helps["d"] == "Ducimus sunt eum in vel voluptatibus aut facere perspiciatis."
    assert data.helps["e"] == "Sit et consequatur a asperiores sequi sint dolores id ipsam."


def test_numpy_docstring_multiline_parameters():
    def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> None:
        """Voluptatibus eos ipsa ex debitis voluptatem dignissimos.

        Qui deserunt sequi aut illo. Minima modi illo sit occaecati. Ducimus illum et. Deleniti repellendus
        cum quasi ut et natus dolorem. Aliquam aut aperiam qui.

        Sint maiores dolorum. Nobis quo distinctio consequuntur. Recusandae fuga qui perspiciatis quisquam.
        Nostrum asperiores neque nisi. Enim voluptatem eum illo.

        Est labore illum voluptatibus at ut. Deleniti ut aut ut aperiam consequatur aut. Reprehenderit
        voluptatem est voluptates temporibus et voluptate accusamus dolores. Placeat nihil dignissimos sed
        sequi sequi.

        Parameters
        ----------
        a : int
            Fuga nemo provident vero odio qui sint et aut veritatis. Facere necessitatibus ut. Voluptatem
            natus natus veritatis earum. Reprehenderit voluptate dolorem dolores consequuntur magnam impedit
            eius. Est ut nisi aut accusamus.
        b : str
            Culpa asperiores incidunt molestias aliquam soluta voluptas excepturi nulla.
        c : float
            Non vitae qui non magni harum eum maiores qui. Dicta sunt voluptatem voluptate. At quibusdam
            aliquam autem et perspiciatis et assumenda. Perferendis qui velit quam numquam iste.
        d : bool, optional
            Aut ipsam aut velit impedit. Quidem expedita aliquid sed officia in ex et. Nihil rem adipisci ut
            perferendis iure., by default True
        e : list[str] | None, optional
            Ratione consequatur molestiae quia deserunt quo. Non cupiditate sunt commodi vero labore
            doloremque voluptatem officiis est. Iusto voluptate reiciendis iusto in. Occaecati quia soluta
            minus perspiciatis alias illum iste aperiam et. Autem accusamus unde omnis est cum ducimus. Iure
            adipisci id omnis quis placeat impedit rerum ab aspernatur.

            Praesentium id rerum quod provident odit dolores adipisci veniam natus. Porro repellat aliquid
            quibusdam recusandae hic voluptas accusantium voluptatem voluptatem. Laboriosam similique nobis
            aut iusto et ab minima cum.

            Voluptas molestiae mollitia autem distinctio magnam dolorem molestiae aliquid. Neque provident
            impedit et. Quod quibusdam nulla cupiditate. Praesentium neque vel ea velit consequatur quis
            voluptate iste. Quae veniam sequi et nihil qui vel voluptatem maxime. Laborum corrupti dolores
            voluptate placeat fugit non nobis., by default None
        """
        pass

    epilog = adjust_epilog_for_test(
        """
        Qui deserunt sequi aut illo. Minima modi illo sit occaecati. Ducimus illum et. Deleniti repellendus
        cum quasi ut et natus dolorem. Aliquam aut aperiam qui.

        Sint maiores dolorum. Nobis quo distinctio consequuntur. Recusandae fuga qui perspiciatis quisquam.
        Nostrum asperiores neque nisi. Enim voluptatem eum illo.

        Est labore illum voluptatibus at ut. Deleniti ut aut ut aperiam consequatur aut. Reprehenderit
        voluptatem est voluptates temporibus et voluptate accusamus dolores. Placeat nihil dignissimos sed
        sequi sequi.
        """
    )
    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == "Voluptatibus eos ipsa ex debitis voluptatem dignissimos."
    assert data.epilog == epilog
    assert (
        data.helps["a"]
        == """Fuga nemo provident vero odio qui sint et aut veritatis. Facere necessitatibus ut. Voluptatem
    natus natus veritatis earum. Reprehenderit voluptate dolorem dolores consequuntur magnam impedit
    eius. Est ut nisi aut accusamus."""
    )
    assert (
        data.helps["b"] == """Culpa asperiores incidunt molestias aliquam soluta voluptas excepturi nulla."""
    )
    assert (
        data.helps["c"]
        == """Non vitae qui non magni harum eum maiores qui. Dicta sunt voluptatem voluptate. At quibusdam
    aliquam autem et perspiciatis et assumenda. Perferendis qui velit quam numquam iste."""
    )
    assert (
        data.helps["d"]
        == """Aut ipsam aut velit impedit. Quidem expedita aliquid sed officia in ex et. Nihil rem adipisci ut
    perferendis iure., by default True"""
    )
    assert (
        data.helps["e"]
        == """Ratione consequatur molestiae quia deserunt quo. Non cupiditate sunt commodi vero labore
    doloremque voluptatem officiis est. Iusto voluptate reiciendis iusto in. Occaecati quia soluta
    minus perspiciatis alias illum iste aperiam et. Autem accusamus unde omnis est cum ducimus. Iure
    adipisci id omnis quis placeat impedit rerum ab aspernatur.

    Praesentium id rerum quod provident odit dolores adipisci veniam natus. Porro repellat aliquid
    quibusdam recusandae hic voluptas accusantium voluptatem voluptatem. Laboriosam similique nobis
    aut iusto et ab minima cum.

    Voluptas molestiae mollitia autem distinctio magnam dolorem molestiae aliquid. Neque provident
    impedit et. Quod quibusdam nulla cupiditate. Praesentium neque vel ea velit consequatur quis
    voluptate iste. Quae veniam sequi et nihil qui vel voluptatem maxime. Laborum corrupti dolores
    voluptate placeat fugit non nobis., by default None"""
    )


def test_sphinx_docstring_multiline_parameters():
    def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> None:
        """Est sit minus quasi soluta unde vero deleniti eligendi.

        Quia aspernatur doloribus id doloribus sunt ratione et voluptatum. Eligendi numquam sed. Voluptas
        consequuntur quibusdam debitis quia unde doloribus ducimus sunt. Et provident assumenda hic eum sint
        quia ipsum sit sed.

        :param a: Velit ratione harum in quia laborum ut est quis.
        :type a: int
        :param b: Adipisci voluptates aut fugiat qui nam non. Eveniet molestiae voluptas explicabo fuga.
            Beatae ex sed nostrum incidunt.
        :type b: str
        :param c: Non non voluptatum ipsum sit maiores et eum adipisci. Autem sit possimus et similique atque.
            Nihil tempore et excepturi.

            Nisi magnam et. Illum minus ea enim eligendi doloremque consequatur odit est officiis. Dolorem
            dolores repellat esse vero quae. Laboriosam ab qui quo eveniet quia ex et. Aut facilis molestias
            qui. Dolorum sit magni repellat iusto aut vel.

            Laborum dolores illum modi. Id et qui nisi harum aperiam doloribus. Quod quibusdam dolorum iusto.
        :type c: float
        :param d: Et magni harum adipisci accusantium aut et ipsum impedit. Sit modi voluptatem. Esse quis aut
            ex. Dicta quam rem repellendus accusantium aut molestias praesentium fugiat corporis. Assumenda
            eum natus voluptatem alias dolorem vitae dolor repudiandae inventore. Et deleniti repellendus
            quo., defaults to True
        :type d: bool, optional
        :param e: Corporis est rerum. Aspernatur dolor porro a culpa omnis. Repudiandae totam necessitatibus
            quibusdam ipsum numquam eveniet dolor quasi. Dolores dolorem voluptate aut. Deleniti officia qui
            molestiae. Quo deserunt nulla aut sit sunt quam nostrum odit et., defaults to None
        :type e: list[str] | None, optional
        """
        pass

    epilog = adjust_epilog_for_test(
        """
        Quia aspernatur doloribus id doloribus sunt ratione et voluptatum. Eligendi numquam sed. Voluptas
        consequuntur quibusdam debitis quia unde doloribus ducimus sunt. Et provident assumenda hic eum sint
        quia ipsum sit sed.
        """
    )
    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == "Est sit minus quasi soluta unde vero deleniti eligendi."
    assert data.epilog == epilog
    assert data.helps["a"] == """Velit ratione harum in quia laborum ut est quis."""
    assert (
        data.helps["b"]
        == """Adipisci voluptates aut fugiat qui nam non. Eveniet molestiae voluptas explicabo fuga.
    Beatae ex sed nostrum incidunt."""
    )
    assert (
        data.helps["c"]
        == """Non non voluptatum ipsum sit maiores et eum adipisci. Autem sit possimus et similique atque.
    Nihil tempore et excepturi.

    Nisi magnam et. Illum minus ea enim eligendi doloremque consequatur odit est officiis. Dolorem
    dolores repellat esse vero quae. Laboriosam ab qui quo eveniet quia ex et. Aut facilis molestias
    qui. Dolorum sit magni repellat iusto aut vel.

    Laborum dolores illum modi. Id et qui nisi harum aperiam doloribus. Quod quibusdam dolorum iusto."""
    )
    assert (
        data.helps["d"]
        == """Et magni harum adipisci accusantium aut et ipsum impedit. Sit modi voluptatem. Esse quis aut
    ex. Dicta quam rem repellendus accusantium aut molestias praesentium fugiat corporis. Assumenda
    eum natus voluptatem alias dolorem vitae dolor repudiandae inventore. Et deleniti repellendus
    quo., defaults to True"""
    )
    assert (
        data.helps["e"]
        == """Corporis est rerum. Aspernatur dolor porro a culpa omnis. Repudiandae totam necessitatibus
    quibusdam ipsum numquam eveniet dolor quasi. Dolores dolorem voluptate aut. Deleniti officia qui
    molestiae. Quo deserunt nulla aut sit sunt quam nostrum odit et., defaults to None"""
    )


def test_google_docstring_multiline_parameters():
    def foo(a: int, b: str, c: float, d: bool = True, e: list[str] | None = None) -> None:
        """nesciunt beatae asperiores

        Et perferendis quia et sit maxime. Accusantium vel sint quam perspiciatis minus explicabo. Incidunt
        iste error autem impedit deserunt tempore quo aut odit.

        Args:
            a (int): Vel similique placeat. Nam enim perspiciatis qui earum voluptas quis. Perspiciatis ut
                vitae. Aspernatur ab ratione libero ex hic consequatur. Nam cupiditate earum. Nihil ea
                exercitationem ut.
            b (str): Molestiae velit et expedita autem quam. Omnis dolorem placeat est. Quidem illum eveniet
                enim exercitationem aut qui dolore est et. Rerum est iste laudantium qui praesentium et. Et
                deserunt voluptates harum voluptas voluptates iste saepe consequatur.
            c (float): Quae minima eligendi veniam aperiam libero temporibus quia qui atque. Velit ea aut vel
                quibusdam commodi id laboriosam inventore aliquam. Nam nisi itaque et sed dolor praesentium
                molestiae quisquam cupiditate. Voluptatem mollitia dolorem est deleniti repellat cum
                voluptatem voluptas sit.

                Sit animi dolore neque libero voluptatibus. Illum voluptatum ullam distinctio quisquam sequi
                delectus quia similique sit. Id enim vel eius iure rerum veritatis eos rem et. Nemo est
                assumenda aut et quo. Et soluta corrupti amet perferendis maxime.

                Placeat aut consequatur vel quo impedit doloribus et in libero. Voluptas ducimus suscipit.
                Assumenda alias est sed asperiores similique id consequuntur. Voluptas rerum placeat
                perferendis possimus ratione at. Ea ut aut id explicabo voluptas.
            d (bool, optional): Error ut architecto fugit natus qui tempora vitae. A sed sequi reprehenderit
                quia autem voluptatem enim. Numquam cum minus cum eos est. Illo voluptas ducimus minus ipsam
                quae dolores quam quo. Quod qui sed incidunt rerum sed. Incidunt repellendus est est labore
                laudantium quia voluptas ipsum.. Defaults to True.
            e (list[str] | None, optional): Explicabo tenetur beatae consequuntur atque aut omnis et. Eveniet
                ipsum repellat voluptatibus sit.

                Placeat eum veritatis praesentium voluptates quia beatae
                repellendus suscipit. Sint neque deserunt quis. Incidunt quibusdam voluptatem animi voluptas
                in. Voluptas dolor aut quisquam.. Defaults to None.
        """
        pass

    epilog = adjust_epilog_for_test(
        """
        Et perferendis quia et sit maxime. Accusantium vel sint quam perspiciatis minus explicabo. Incidunt
        iste error autem impedit deserunt tempore quo aut odit.
        """
    )
    data = clig.Command(foo).get_inferred_docstring_data()
    assert data is not None
    assert data.description == "nesciunt beatae asperiores"
    assert data.epilog == epilog
    assert (
        data.helps["a"]
        == """Vel similique placeat. Nam enim perspiciatis qui earum voluptas quis. Perspiciatis ut
        vitae. Aspernatur ab ratione libero ex hic consequatur. Nam cupiditate earum. Nihil ea
        exercitationem ut."""
    )
    assert (
        data.helps["b"]
        == """Molestiae velit et expedita autem quam. Omnis dolorem placeat est. Quidem illum eveniet
        enim exercitationem aut qui dolore est et. Rerum est iste laudantium qui praesentium et. Et
        deserunt voluptates harum voluptas voluptates iste saepe consequatur."""
    )
    assert (
        data.helps["c"]
        == """Quae minima eligendi veniam aperiam libero temporibus quia qui atque. Velit ea aut vel
        quibusdam commodi id laboriosam inventore aliquam. Nam nisi itaque et sed dolor praesentium
        molestiae quisquam cupiditate. Voluptatem mollitia dolorem est deleniti repellat cum
        voluptatem voluptas sit.

        Sit animi dolore neque libero voluptatibus. Illum voluptatum ullam distinctio quisquam sequi
        delectus quia similique sit. Id enim vel eius iure rerum veritatis eos rem et. Nemo est
        assumenda aut et quo. Et soluta corrupti amet perferendis maxime.

        Placeat aut consequatur vel quo impedit doloribus et in libero. Voluptas ducimus suscipit.
        Assumenda alias est sed asperiores similique id consequuntur. Voluptas rerum placeat
        perferendis possimus ratione at. Ea ut aut id explicabo voluptas."""
    )
    assert (
        data.helps["d"]
        == """Error ut architecto fugit natus qui tempora vitae. A sed sequi reprehenderit
        quia autem voluptatem enim. Numquam cum minus cum eos est. Illo voluptas ducimus minus ipsam
        quae dolores quam quo. Quod qui sed incidunt rerum sed. Incidunt repellendus est est labore
        laudantium quia voluptas ipsum.. Defaults to True."""
    )
    assert (
        data.helps["e"]
        == """Explicabo tenetur beatae consequuntur atque aut omnis et. Eveniet
        ipsum repellat voluptatibus sit.

        Placeat eum veritatis praesentium voluptates quia beatae
        repellendus suscipit. Sint neque deserunt quis. Incidunt quibusdam voluptatem animi voluptas
        in. Voluptas dolor aut quisquam.. Defaults to None."""
    )
