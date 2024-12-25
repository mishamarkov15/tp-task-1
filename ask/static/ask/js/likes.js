"use strict"

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const questions = document.getElementsByClassName('question-article');

for (const question of questions) {
    const questionId = question.dataset.questionId;
    const likeButton = question.querySelector('.like-btn');
    const likeCounter = question.querySelector('.like-counter');
    // console.log({question, likeButton, likeCounter});
    likeButton.addEventListener('click', () => {
      const request = new Request(`question/${questionId}/like`, {
          method: "POST",
          headers: {
              'X-CSRFToken': csrftoken,
          },
          mode: 'same-origin',
          body: JSON.stringify({question_id: `${questionId}`})
      });

      fetch(request)
          .then((response) => {
              response.json().then(
                  (data) => {
                      console.log(data);
                      likeCounter.innerHTML = data.likes_count;
                  }
              )
          })
          .catch()
          .finally();

    })
}