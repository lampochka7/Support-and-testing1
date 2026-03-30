# test_calculator.py
import unittest
from calculator import add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
    """Тесты для калькулятора"""
    
    def test_add(self):
        """Тестирование функции сложения"""
        # Проверка сложения целых чисел
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(10, 15), 25)
        self.assertEqual(add(0, 0), 0)
        
        # Проверка сложения отрицательных чисел
        self.assertEqual(add(-1, -1), -2)
        self.assertEqual(add(-5, 3), -2)
        self.assertEqual(add(5, -3), 2)
        
        # Проверка сложения дробных чисел
        self.assertEqual(add(1.5, 2.5), 4.0)
        self.assertEqual(add(0.1, 0.2), 0.3)
        self.assertAlmostEqual(add(1.333, 2.666), 3.999, places=3)
    
    def test_subtract(self):
        """Тестирование функции вычитания"""
        # Проверка вычитания целых чисел
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(10, 4), 6)
        
        # Проверка вычитания с отрицательным результатом
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(3, 10), -7)
        
        # Дополнительные проверки
        self.assertEqual(subtract(5, 0), 5)
        self.assertEqual(subtract(-5, -3), -2)
        self.assertEqual(subtract(-5, 3), -8)
        
        # Проверка вычитания дробных чисел
        self.assertEqual(subtract(5.5, 2.3), 3.2)
        self.assertAlmostEqual(subtract(3.1415, 1.1415), 2.0, places=4)
    
    def test_multiply(self):
        """Тестирование функции умножения"""
        # Проверка умножения положительных чисел
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(4, 5), 20)
        self.assertEqual(multiply(1, 100), 100)
        
        # Проверка умножения на ноль
        self.assertEqual(multiply(5, 0), 0)
        self.assertEqual(multiply(0, 10), 0)
        self.assertEqual(multiply(0, 0), 0)
        
        # Проверка умножения отрицательного и положительного числа
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(4, -5), -20)
        self.assertEqual(multiply(-7, -8), 56)  # отрицательное на отрицательное
        
        # Проверка умножения дробных чисел
        self.assertEqual(multiply(2.5, 4), 10.0)
        self.assertAlmostEqual(multiply(1.5, 1.5), 2.25, places=2)
    
    def test_divide(self):
        """Тестирование функции деления"""
        # Проверка деления обычных чисел
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(divide(15, 3), 5.0)
        self.assertEqual(divide(100, 25), 4.0)
        
        # Проверка деления с остатком
        self.assertAlmostEqual(divide(7, 3), 2.3333333333333335)
        self.assertAlmostEqual(divide(10, 3), 3.3333333333333335)
        self.assertAlmostEqual(divide(1, 3), 0.3333333333333333)
        
        # Проверка деления дробных чисел
        self.assertEqual(divide(5.5, 2.2), 2.5)
        self.assertAlmostEqual(divide(1, 3), 1/3)
        
        # Проверка деления отрицательных чисел
        self.assertEqual(divide(-10, 2), -5.0)
        self.assertEqual(divide(10, -2), -5.0)
        self.assertEqual(divide(-10, -2), 5.0)
        
        # Проверка деления на ноль - должно выбрасываться исключение ValueError
        with self.assertRaises(ValueError):
            divide(10, 0)
        
        with self.assertRaises(ValueError):
            divide(5, 0)
        
        with self.assertRaises(ValueError):
            divide(0, 0)  # деление нуля на ноль тоже должно выбрасывать исключение
        
        # Проверка сообщения об ошибке
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero.")


if __name__ == '__main__':
    unittest.main()
