from combat import apply_damage, apply_healing, is_alive


def test_apply_damage():
    result = apply_damage(100, 30)
    assert result == ...  # TODO: What should the result be?


def test_apply_damage_floor():
    # HP cannot drop below 0, even if damage exceeds current HP
    result = apply_damage(20, 50)
    assert result == ...  # TODO: What is the minimum possible HP?


def test_apply_healing():
    result = apply_healing(70, 20, 100)
    assert result == ...  # TODO: 70 + 20 = ?


def test_apply_healing_capped():
    # Healing should not exceed max_hp
    result = apply_healing(90, 20, 100)
    assert result == ...  # TODO: Can hero.hp go above max_hp?


def test_is_alive_true():
    result = is_alive(52)
    assert result is ...  # TODO: Is a hero with 52 HP alive?


def test_is_alive_false():
    result = is_alive(0)
    assert result is ...  # TODO: Is a hero with 0 HP alive?
