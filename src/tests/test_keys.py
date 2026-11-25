from keys import generate_key, split_authors, name_parts


def test_several_authors_use_initials_and_short_year():
    key = generate_key("Meikäläinen, Matti; Niinistö, Sauli", "2020")

    assert key == "MN20"


def test_single_author_uses_first_name_and_short_year():
    assert generate_key("Meikäläinen, Matti", "2017") == "Matti17"


def test_name_without_comma_is_accepted():
    assert generate_key("Meikäläinen Matti", "2017") == "Matti17"


def test_and_separator_is_accepted():
    assert generate_key("Vihavainen, Arto and Paksula, Matti", "2011") == "VP11"


def test_three_authors():
    key = generate_key("Vihavainen, Arto; Paksula, Matti; Luukkainen, Matti", "2011")

    assert key == "VPL11"


def test_used_key_gets_letter_suffix():
    key = generate_key("Meikäläinen, Matti", "2017", ["Matti17"])

    assert key == "Matti17a"


def test_suffix_continues_until_free():
    key = generate_key("Meikäläinen, Matti", "2017", ["Matti17", "Matti17a"])

    assert key == "Matti17b"


def test_comparison_ignores_case():
    key = generate_key("Meikäläinen, Matti", "2017", ["matti17"])

    assert key == "Matti17a"


def test_split_authors():
    assert split_authors("A, B; C, D") == ["A, B", "C, D"]


def test_name_parts():
    assert name_parts("Meikäläinen, Matti") == ("Meikäläinen", "Matti")

def test_author_list_is_accepted():
    assert generate_key(["Meikäläinen, Matti", "Niinistö, Sauli"], "2020") == "MN20"
    assert generate_key(["Meikäläinen, Matti"], "2017") == "Matti17"
    