const inputBoxes = document.getElementsByClassName("input-box");

const notificationModalContainer = document.getElementById(
  "notification-modal-container"
);
const notificationModal = document.getElementById("notification-modal");

for (const inputBox of inputBoxes) {
  const input = inputBox.getElementsByTagName("input")[0];
  input.addEventListener("input", (event) => {
    if (event.target.value) {
      inputBox.classList.add("active");
    } else {
      inputBox.classList.remove("active");
    }
  });
}

if (notificationModalContainer) {
  notificationModalContainer.addEventListener("click", () => {
    window.location.href = `/auth/login`;
  });
}
