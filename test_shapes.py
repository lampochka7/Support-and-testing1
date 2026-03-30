# test_shapes.py
import pytest
import math
from shapes import Circle, Rectangle

# ==================== Тесты для класса Circle ====================

def test_circle_creation_positive_radius():
    """Проверка успешного создания круга с положительным радиусом."""
    circle = Circle(5)
    assert circle.radius == 5


def test_circle_negative_radius():
    """Проверка, что при отрицательном радиусе выбрасывается ValueError."""
    with pytest.raises(ValueError, match="Radius must be positive."):
        Circle(-1)


def test_circle_zero_radius():
    """Проверка, что при радиусе равном 0 выбрасывается ValueError."""
    with pytest.raises(ValueError, match="Radius must be positive."):
        Circle(0)


@pytest.mark.parametrize("radius, expected_area, expected_perimeter", [
    (1, math.pi, 2 * math.pi),                     # Радиус 1
    (2.5, math.pi * (2.5 ** 2), 2 * math.pi * 2.5), # Радиус 2.5
    (10, math.pi * 100, 2 * math.pi * 10),         # Радиус 10
    (0.5, math.pi * 0.25, 2 * math.pi * 0.5),      # Радиус 0.5 (дополнительный тест)
])
def test_circle_area_and_perimeter(radius, expected_area, expected_perimeter):
    """
    Параметризованный тест для проверки площади и периметра круга.
    Сравнение производится с округлением до 5 знаков.
    """
    circle = Circle(radius)
    assert round(circle.area(), 5) == round(expected_area, 5)
    assert round(circle.perimeter(), 5) == round(expected_perimeter, 5)


# ==================== Тесты для класса Rectangle ====================

def test_rectangle_creation_positive_dimensions():
    """Проверка успешного создания прямоугольника с положительными сторонами."""
    rectangle = Rectangle(3, 4)
    assert rectangle.width == 3
    assert rectangle.height == 4


def test_rectangle_negative_width():
    """Проверка, что при отрицательной ширине выбрасывается ValueError."""
    with pytest.raises(ValueError, match="Width and height must be positive."):
        Rectangle(-2, 5)


def test_rectangle_negative_height():
    """Проверка, что при отрицательной высоте выбрасывается ValueError."""
    with pytest.raises(ValueError, match="Width and height must be positive."):
        Rectangle(2, -5)


def test_rectangle_zero_width():
    """Проверка, что при нулевой ширине выбрасывается ValueError."""
    with pytest.raises(ValueError, match="Width and height must be positive."):
        Rectangle(0, 5)


def test_rectangle_zero_height():
    """Проверка, что при нулевой высоте выбрасывается ValueError."""
    with pytest.raises(ValueError, match="Width and height must be positive."):
        Rectangle(5, 0)


@pytest.mark.parametrize("width, height, expected_area, expected_perimeter", [
    (1, 1, 1, 4),        # Квадрат 1x1
    (3, 4, 12, 14),      # Прямоугольник 3x4
    (2.5, 4, 10.0, 13.0), # Прямоугольник с десятичными числами
    (5, 10, 50, 30),     # Прямоугольник 5x10
])
def test_rectangle_area_and_perimeter(width, height, expected_area, expected_perimeter):
    """
    Параметризованный тест для проверки площади и периметра прямоугольника.
    """
    rectangle = Rectangle(width, height)
    # Для целых чисел округление не требуется, но для единообразия округляем
    assert round(rectangle.area(), 5) == round(expected_area, 5)
    assert round(rectangle.perimeter(), 5) == round(expected_perimeter, 5)


# ==================== Тесты с фикстурами ====================

@pytest.fixture
def circle():
    """
    Фикстура, возвращающая объект Circle с радиусом 1.
    """
    return Circle(1)


def test_circle_fixture_area(circle):
    """
    Тест, использующий фикстуру circle для проверки площади.
    """
    assert circle.radius == 1
    assert round(circle.area(), 5) == round(math.pi, 5)


def test_circle_fixture_perimeter(circle):
    """
    Дополнительный тест, использующий фикстуру circle для проверки периметра.
    """
    assert round(circle.perimeter(), 5) == round(2 * math.pi, 5)
