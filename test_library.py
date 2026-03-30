# test_library.py
import unittest
from library import Library


class TestLibrary(unittest.TestCase):
    """Тесты для класса Library"""
    
    def setUp(self):
        """Создание чистой библиотеки перед каждым тестом"""
        self.library = Library()
    
    # ==================== Тесты для add_book ====================
    
    def test_add_book_success(self):
        """Успешное добавление книги с валидными данными"""
        self.library.add_book("1984", "George Orwell", "12345")
        books = self.library.list_books()
        
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], "1984")
        self.assertEqual(books[0]['author'], "George Orwell")
        self.assertEqual(books[0]['isbn'], "12345")
    
    def test_add_book_multiple_books(self):
        """Добавление нескольких книг"""
        self.library.add_book("Book1", "Author1", "111")
        self.library.add_book("Book2", "Author2", "222")
        
        books = self.library.list_books()
        self.assertEqual(len(books), 2)
    
    def test_add_book_empty_title_raises_error(self):
        """Проверка: пустое название вызывает ValueError"""
        with self.assertRaises(ValueError) as context:
            self.library.add_book("", "Author", "123")
        self.assertEqual(str(context.exception), "Title, author, and ISBN must not be empty.")
    
    def test_add_book_empty_author_raises_error(self):
        """Проверка: пустой автор вызывает ValueError"""
        with self.assertRaises(ValueError) as context:
            self.library.add_book("Title", "", "123")
        self.assertEqual(str(context.exception), "Title, author, and ISBN must not be empty.")
    
    def test_add_book_empty_isbn_raises_error(self):
        """Проверка: пустой ISBN вызывает ValueError"""
        with self.assertRaises(ValueError) as context:
            self.library.add_book("Title", "Author", "")
        self.assertEqual(str(context.exception), "Title, author, and ISBN must not be empty.")
    
    def test_add_book_none_title_raises_error(self):
        """Проверка: None в названии вызывает ValueError"""
        with self.assertRaises(ValueError):
            self.library.add_book(None, "Author", "123")
    
    def test_add_book_none_author_raises_error(self):
        """Проверка: None в авторе вызывает ValueError"""
        with self.assertRaises(ValueError):
            self.library.add_book("Title", None, "123")
    
    def test_add_book_none_isbn_raises_error(self):
        """Проверка: None в ISBN вызывает ValueError"""
        with self.assertRaises(ValueError):
            self.library.add_book("Title", "Author", None)
    
    def test_add_book_duplicate_isbn_raises_error(self):
        """Проверка: добавление книги с существующим ISBN вызывает ValueError"""
        self.library.add_book("Book1", "Author1", "111")
        
        with self.assertRaises(ValueError) as context:
            self.library.add_book("Book2", "Author2", "111")
        self.assertEqual(str(context.exception), "Book with this ISBN already exists.")
    
    def test_add_book_with_spaces(self):
        """Добавление книги с пробелами в полях (пробелы считаются валидными)"""
        self.library.add_book("   ", "Author", "123")
        books = self.library.list_books()
        
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], "   ")
        self.assertEqual(books[0]['author'], "Author")
        self.assertEqual(books[0]['isbn'], "123")
    
    def test_add_book_isbn_type_sensitivity(self):
        """Проверка: ISBN как строка и как число считаются разными"""
        self.library.add_book("Book1", "Author1", "123")
        
        # ISBN "123" уже существует, но 123 как число - это другой тип
        # В Python строка "123" не равна числу 123, поэтому исключения не будет
        self.library.add_book("Book2", "Author2", 123)
        
        books = self.library.list_books()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['isbn'], "123")
        self.assertEqual(books[1]['isbn'], 123)
    
    def test_add_book_after_removal_same_isbn(self):
        """После удаления книги можно добавить новую с тем же ISBN"""
        self.library.add_book("Book1", "Author1", "111")
        self.library.remove_book("111")
        self.library.add_book("Book2", "Author2", "111")
        
        books = self.library.list_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], "Book2")
    
    # ==================== Тесты для remove_book ====================
    
    def test_remove_book_success(self):
        """Успешное удаление книги по ISBN"""
        self.library.add_book("1984", "George Orwell", "12345")
        self.library.remove_book("12345")
        
        books = self.library.list_books()
        self.assertEqual(len(books), 0)
    
    def test_remove_book_nonexistent_raises_error(self):
        """Удаление несуществующей книги вызывает ValueError"""
        with self.assertRaises(ValueError) as context:
            self.library.remove_book("99999")
        self.assertEqual(str(context.exception), "Book not found.")
    
    def test_remove_book_from_multiple_books(self):
        """Удаление книги из нескольких"""
        self.library.add_book("Book1", "Author1", "111")
        self.library.add_book("Book2", "Author2", "222")
        self.library.add_book("Book3", "Author3", "333")
        
        self.library.remove_book("222")
        
        books = self.library.list_books()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['isbn'], "111")
        self.assertEqual(books[1]['isbn'], "333")
    
    def test_remove_book_type_sensitive(self):
        """ISBN с разными типами считаются разными"""
        self.library.add_book("Book1", "Author1", "123")
        
        # Попытка удалить число 123, но в библиотеке есть строка "123"
        with self.assertRaises(ValueError):
            self.library.remove_book(123)
        
        # Убедимся, что книга все еще в библиотеке
        books = self.library.list_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['isbn'], "123")
    
    # ==================== Тесты для find_book_by_title ====================
    
    def test_find_book_by_title_success(self):
        """Поиск книги по названию"""
        self.library.add_book("1984", "George Orwell", "12345")
        
        found = self.library.find_book_by_title("1984")
        
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]['title'], "1984")
        self.assertEqual(found[0]['author'], "George Orwell")
        self.assertEqual(found[0]['isbn'], "12345")
    
    def test_find_book_by_title_multiple_books(self):
        """Поиск нескольких книг с одинаковым названием"""
        self.library.add_book("Python Programming", "Author A", "111")
        self.library.add_book("Python Programming", "Author B", "222")
        self.library.add_book("Python Basics", "Author C", "333")
        
        found = self.library.find_book_by_title("Python Programming")
        
        self.assertEqual(len(found), 2)
        self.assertEqual(found[0]['author'], "Author A")
        self.assertEqual(found[1]['author'], "Author B")
    
    def test_find_book_by_title_nonexistent(self):
        """Поиск несуществующей книги возвращает пустой список"""
        self.library.add_book("1984", "George Orwell", "12345")
        
        found = self.library.find_book_by_title("Nonexistent Book")
        
        self.assertEqual(found, [])
        self.assertEqual(len(found), 0)
    
    def test_find_book_by_title_case_sensitive(self):
        """Поиск чувствителен к регистру"""
        self.library.add_book("Python", "Author", "111")
        
        found_lower = self.library.find_book_by_title("python")
        found_upper = self.library.find_book_by_title("PYTHON")
        
        self.assertEqual(len(found_lower), 0)
        self.assertEqual(len(found_upper), 0)
    
    def test_find_book_by_title_empty_library(self):
        """Поиск в пустой библиотеке возвращает пустой список"""
        found = self.library.find_book_by_title("Any Book")
        
        self.assertEqual(found, [])
    
    def test_find_book_by_title_after_removal(self):
        """После удаления книги она не находится"""
        self.library.add_book("1984", "George Orwell", "12345")
        self.library.remove_book("12345")
        
        found = self.library.find_book_by_title("1984")
        
        self.assertEqual(found, [])
    
    # ==================== Тесты для list_books ====================
    
    def test_list_books_returns_copy(self):
        """Проверка: list_books возвращает копию, а не оригинальный список"""
        self.library.add_book("Book1", "Author1", "111")
        self.library.add_book("Book2", "Author2", "222")
        
        books = self.library.list_books()
        # Изменяем полученный список
        books.append({'title': 'Hacked', 'author': 'Hacker', 'isbn': '999'})
        
        # Внутренний список библиотеки не должен измениться
        internal_books = self.library.list_books()
        self.assertEqual(len(internal_books), 2)
        self.assertEqual(internal_books[0]['title'], "Book1")
        self.assertEqual(internal_books[1]['title'], "Book2")
    
    def test_list_books_order_preserved(self):
        """Проверка: порядок книг сохраняется при добавлении"""
        self.library.add_book("First Book", "Author1", "111")
        self.library.add_book("Second Book", "Author2", "222")
        self.library.add_book("Third Book", "Author3", "333")
        
        books = self.library.list_books()
        
        self.assertEqual(books[0]['title'], "First Book")
        self.assertEqual(books[1]['title'], "Second Book")
        self.assertEqual(books[2]['title'], "Third Book")
    
    def test_list_books_empty(self):
        """Пустая библиотека возвращает пустой список"""
        books = self.library.list_books()
        
        self.assertEqual(books, [])
        self.assertEqual(len(books), 0)
    
    def test_list_books_after_removal_order(self):
        """Порядок сохраняется после удаления книги"""
        self.library.add_book("Book1", "Author1", "111")
        self.library.add_book("Book2", "Author2", "222")
        self.library.add_book("Book3", "Author3", "333")
        
        self.library.remove_book("222")
        
        books = self.library.list_books()
        
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['title'], "Book1")
        self.assertEqual(books[1]['title'], "Book3")
    
    def test_list_books_modification_does_not_affect_internal_state(self):
        """Изменение возвращенного списка не влияет на внутреннее состояние"""
        self.library.add_book("Book1", "Author1", "111")
        
        books = self.library.list_books()
        books[0]['title'] = "Modified Title"
        
        # Внутреннее состояние не должно измениться
        internal_books = self.library.list_books()
        self.assertEqual(internal_books[0]['title'], "Book1")
    
    # ==================== Комплексные тесты ====================
    
    def test_complete_workflow(self):
        """Тестирование полного рабочего процесса"""
        # Добавление книг
        self.library.add_book("1984", "George Orwell", "111")
        self.library.add_book("Animal Farm", "George Orwell", "222")
        self.library.add_book("Brave New World", "Aldous Huxley", "333")
        
        # Проверка списка
        self.assertEqual(len(self.library.list_books()), 3)
        
        # Поиск по названию
        found = self.library.find_book_by_title("1984")
        self.assertEqual(len(found), 1)
        
        # Поиск книг автора
        orwell_books = [b for b in self.library.list_books() if b['author'] == "George Orwell"]
        self.assertEqual(len(orwell_books), 2)
        
        # Удаление книги
        self.library.remove_book("111")
        self.assertEqual(len(self.library.list_books()), 2)
        
        # Проверка, что удаленная книга не находится
        found = self.library.find_book_by_title("1984")
        self.assertEqual(found, [])
        
        # Повторное добавление с тем же ISBN
        self.library.add_book("1984", "George Orwell", "111")
        self.assertEqual(len(self.library.list_books()), 3)


if __name__ == '__main__':
    unittest.main()
