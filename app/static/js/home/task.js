import { patch, remove } from "../_api.js";

const tasks = document.getElementsByClassName("task");

for (const task of tasks) {
  const actionButtons = task.getElementsByClassName("action-button");
  for (const actionButton of actionButtons) {
    console.log(actionButton);
    actionButton.addEventListener("click", async () => {
      let status;
      const action = actionButton.getAttribute("data-action");
      const taskUuid = actionButton.getAttribute("data-taskUuid");

      if (action !== "delete") {
        status = await patch(`/home/move/${action}`, {
          uuid: taskUuid,
        });
      } else {
        status = await remove(`/home/remove`, taskUuid);
      }

      if (status !== 500) {
        window.location.reload();
      } else {
        const message = encodeURIComponent(`The action couldn't be completed`);
        window.location.href = `/home?message=${message}`;
      }
    });
  }
}
