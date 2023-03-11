import { get, post } from "../_api.js";
import { getFormData } from "../_helper.js";

const addTaskForm = document.getElementById("add-new-task-form");
const addTaskContainer = document.getElementById("add-modal-container");
const infoModalContainer = document.getElementById("info-modal-container");
const newTaskButton = document.getElementById("add-new-task-button");
const logOutButton = document.getElementById("logout-button");

newTaskButton.addEventListener("click", () => {
  addTaskContainer.classList.add("visible");
});

// Add the task to the database linking to the logged user
addTaskForm.addEventListener("submit", async (event) => {
  // If the try doesn't pass, the user didn't fill all the information
  try {
    const obj = getFormData(event, addTaskForm);
    const { status } = await post("/home/add", obj);

    if (status === 201) {
      window.location.reload();
    } else {
      const message = encodeURIComponent(`The action couldn't be completed`);
      window.location.href = `/home?message=${message}`;
    }
  } catch (error) {
    window.location.href = `/home?message=${error.message}`;
  }
});

// If there's a message, display it
if (infoModalContainer) {
  infoModalContainer.addEventListener("click", () => {
    window.location.href = `/home`;
  });
}

logOutButton.addEventListener("click", async () => {
  await get("/auth/logout");
  window.location.href = "/auth/login";
});
