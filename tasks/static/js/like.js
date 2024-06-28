const ratingButtons = document.querySelectorAll('.rating-buttons');
ratingButtons.forEach(button => {
    button.addEventListener('click', event => {
        // Получаем значение рейтинга из data-атрибута кнопки
        const value = parseInt(event.target.dataset.value)
        const otzyvId = parseInt(event.target.dataset.otzyv)
        const ratingSum = button.querySelector('.rating-sum');
        // Создаем объект FormData для отправки данных на сервер
        const formData = new FormData();
        // Добавляем id статьи, значение кнопки
        formData.append('otzyv_id', otzyvId);
        formData.append('value', value);
        // Отправляем AJAX-Запрос на сервер
        fetch("/rating", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            // Обновляем значение на кнопке
            ratingSum.textContent = data.rating_sum;
        })
        .catch(error => console.error(error));
    });
});
function show()
{   const otzyvId = parseInt(document.querySelector('.btn-primary').dataset.otzyv);

    const ratingSum = document.querySelector('.rating-sum');
    var formData = {
        otzyv_id: otzyvId,
    };
    $.ajax({
        type: "POST",
        url: "/upload-rating",
        data: formData,
        cache: false,
        success: function(data){
            ratingSum.textContent = data.rating;
        }
    });
}


$(document).ready(function(){

    show();
    setInterval('show()',1000);
});
