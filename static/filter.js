// Получение элементов DOM
const searchInput = document.getElementById('search-input');
const categorySelect = document.getElementById('category-select');
const courseList = document.getElementById('course-list');

// Обработчик события при изменении значений в полях
searchInput.addEventListener('input', fetchCourses);
categorySelect.addEventListener('change', fetchCourses);

function fetchCourses() {
  const searchQuery = searchInput.value;
  const selectedCategory = categorySelect.value;

  // Отправка AJAX-запроса на сервер
  fetch(`/api/courses?search=${searchQuery}&category=${selectedCategory}`)
    .then(response => response.json())
    .then(data => {
      // Обновление списка курсов на странице
      courseList.innerHTML = '';
      data.forEach(course => {
        // Создаем элемент списка для каждого курса
        const li = document.createElement('li');
        li.textContent = course.title;
        courseList.appendChild(li);
      });
    });
}