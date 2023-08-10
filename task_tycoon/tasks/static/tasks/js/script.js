// Скрытие всех заданий
function hideAllForms() {
  const taskTestForm = document.querySelector('.task_test');
  const taskDetailedForm = document.querySelector('.task_detailed');
  taskTestForm.classList.add('task_test_off');
  taskDetailedForm.classList.add('task_detailed_off');
}

// Отображения тест. зад.
function showTestForm() {
  const taskTestForm = document.querySelector('.task_test');
  taskTestForm.classList.remove('task_test_off');
}

//Отображения развер. зад.
function showDetailedForm() {
  const taskDetailedForm = document.querySelector('.task_detailed');
  taskDetailedForm.classList.remove('task_detailed_off');
}


// При клике на кнопку "Добавить тестовое задание"
document.querySelector('.test-btn').addEventListener('click', function () {
  hideAllForms(); // Скрываем все формы
  showTestForm(); // Показываем форму тест зад
});

// При клике на кнопку "Добавить развернутое задание"
document.querySelector('.detailed-btn').addEventListener('click', function () {
  hideAllForms();
  showDetailedForm(); // Показываем форму развер зад
});


// При клике на кнопку "+"
document.querySelector('.task_response_add').addEventListener('click', function (e) {
  e.preventDefault();

  const taskResponses = document.querySelector('.task_responses');

  // Создаем новый обобщающий блок
  const newResponseDiv = document.createElement('div');
  newResponseDiv.classList.add('task_response');

  // Создаем поля
  const responseInput = document.createElement('input');
  responseInput.classList.add("task_response_name")
  responseInput.type = 'text';
  responseInput.placeholder = 'Ответ';
  responseInput.name = 'response';

  const checkboxInput = document.createElement('input');
  checkboxInput.type = 'checkbox';

  const responseDel = document.createElement('button');
  responseDel.classList.add("task_response_del")
  responseDel.innerText  = '-'

  // Добавляем элементы в блок
  newResponseDiv.appendChild(responseInput);
  newResponseDiv.appendChild(checkboxInput);
  newResponseDiv.appendChild(responseDel);

  //Добавляем в родительский
  taskResponses.appendChild(newResponseDiv);
});


const submitButtons = document.querySelectorAll('.task_ready');
let count = 0

submitButtons.forEach((button) => {
  button.addEventListener('click', function (e) {
    e.preventDefault()

    const allTasksDiv = document.querySelector('.all-tasks');
    const newResponseDiv = document.createElement('div');
    newResponseDiv.classList.add('task_content');

    const newCount = document.createElement('p');
    count++
    newCount.textContent = count
    newResponseDiv.insertBefore(newCount, newResponseDiv.firstChild);


    const form = e.target.closest('form');

    const taskName = form.querySelector('.task_name');
    const clonedTaskName = taskName.cloneNode(true);
    const newTaskDel = document.createElement('button');
    newTaskDel.classList.add('task_task_del');
    newTaskDel.innerHTML = 'Удалить'

    newResponseDiv.appendChild(clonedTaskName);
    newResponseDiv.appendChild(newTaskDel);

    if (form.querySelector('.task_response_name')) {
      newResponseDiv.classList.add('task_test');

      const taskResponseDivs = document.querySelectorAll('.task_response');
      taskResponseDivs.forEach((taskResponseDiv) => {
        const responseNameInput = taskResponseDiv.querySelector('.task_response_name')
        const cloneResponseNameInput = responseNameInput.cloneNode(true);
        const checkboxInput = taskResponseDiv.querySelector('input[type="checkbox"]')
        const cloneCheckboxInput = checkboxInput.cloneNode(true);
        const responseDel = taskResponseDiv.querySelector('.task_response_del')
        const cloneResponseDel = responseDel.cloneNode(true);
        const newFullResponse = document.createElement('div');
        newFullResponse.classList.add('task_full-response');

        newFullResponse.appendChild(cloneResponseNameInput);
        newFullResponse.appendChild(cloneCheckboxInput);
        newFullResponse.appendChild(cloneResponseDel);

        newResponseDiv.appendChild(newFullResponse);

        allTasksDiv.appendChild(newResponseDiv);

        responseNameInput.value = '';
        taskName.value = ''
        checkboxInput.checked = false;
      });
    } else {
      newResponseDiv.classList.add('task_detailed');

      allTasksDiv.appendChild(newResponseDiv);

      taskName.value = ''
    }

    const parentBlock = document.querySelector('.task_responses');
    const firstElement = parentBlock.firstElementChild;

    parentBlock.innerHTML = '';
    parentBlock.appendChild(firstElement);
  })
})



//Реализация кнопки удаления ответа
const taskResponses = document.querySelector('.wrapper');

taskResponses.addEventListener('click', (e) => {
  if (e.target.classList.contains('task_response_del')) {

    const taskResponse = e.target.parentElement;

    taskResponse.remove();
  }
});


const taskDel = document.querySelector('.all-tasks');
const paragraphs = taskDel.querySelectorAll('.task_content p')

taskDel.addEventListener('click', (e) => {
  e.stopPropagation()
  if (e.target.classList.contains('task_task_del')) {
    e.preventDefault();

    const taskResponse = e.target.parentElement;
    taskResponse.remove();
  }
});












