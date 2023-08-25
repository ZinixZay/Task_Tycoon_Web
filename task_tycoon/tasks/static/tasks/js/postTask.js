document.getElementById("submit-btn").addEventListener("click", function (e) {
  e.preventDefault();

  const form = document.getElementById("form-all-tasks");
  const formDataObject = {};

  formDataObject[0] = document.querySelector('input[name="title"]').value

  form.querySelectorAll(".task_content").forEach((task, key) => {
    const task_name = task.querySelector('.task_name').value

    if (task.classList.contains('task_test')) {
      const objFullResponse = []

      task.querySelectorAll('.task_full-response').forEach((fullResponse) => {
        const responseName = fullResponse.querySelector('.task_response_name').value
        const responseCheckbox = fullResponse.querySelector('input[type="checkbox"]').checked

        objFullResponse.push({
          response_name: responseName,
          response_right: responseCheckbox,
        })
      })

      formDataObject[key + 1] = {
        task_name: task_name,
        responses: objFullResponse,
      }
    } else {
      formDataObject[key + 1] = {
        task_name: task_name,
        responses: 0,
      }
    }
  })
  function getCookie(name) {
    const value = `; ${document.cookie};`
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  fetch("http://127.0.0.1:8000/api/v1/addtask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(formDataObject),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      form.reset()
      document.querySelector('.title').value = ''
      document.querySelector('.all-tasks').innerHTML = ''

      window.location.href = 'http://127.0.0.1:8000/tasks/'

      return response.json();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});