// Находим кнопку выхода и добавляем обработчик
document.getElementById('logoutButton').addEventListener('click', function(e) {
    e.preventDefault();

    fetch("{% url 'users:logout' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '{% url "courses:course_list" %}'; // Перенаправление
        } else {
            alert('Ошибка при выходе!');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при выходе');
    });
});
