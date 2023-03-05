const addTaskForm = document.getElementById("add-new-task-form");
const addTaskContainer = document.getElementById("add-modal-container");
const newTaskButton = document.getElementById("add-new-task-button");

newTaskButton.addEventListener("click", () => {
  addTaskContainer.classList.add("visible");
});

addTaskForm.addEventListener("click", (event) => {
  event.stopPropagation();
});

addTaskContainer.addEventListener("click", () => {
  hideModal();
});

const hideModal = () => {
  if (addTaskContainer.classList.contains("visible")) {
    addTaskContainer.classList.remove("visible");
  }
};
