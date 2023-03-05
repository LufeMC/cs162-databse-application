const emailInputBox = document.getElementById("email-input-box");
const passwordInputBox = document.getElementById("password-input-box");
const firstNameInputBox = document.getElementById("first-name-input-box");
const lastNameInputBox = document.getElementById("last-name-input-box");

const emailInput = document.getElementById("email-input");
const passwordInput = document.getElementById("password-input");
const firstNameInput = document.getElementById("first-name-input");
const lastNameInput = document.getElementById("last-name-input");

const notificationModalContainer = document.getElementById(
  "notification-modal-container"
);
const notificationModal = document.getElementById("notification-modal");

emailInput.addEventListener("input", (event) => {
  if (event.target.value) {
    console.log(event.target.value);
    emailInputBox.classList.add("active");
  } else {
    emailInputBox.classList.remove("active");
  }
});

passwordInput.addEventListener("input", (event) => {
  if (event.target.value) {
    passwordInputBox.classList.add("active");
  } else {
    passwordInputBox.classList.remove("active");
  }
});

if (firstNameInput) {
  firstNameInput.addEventListener("input", (event) => {
    if (event.target.value) {
      firstNameInputBox.classList.add("active");
    } else {
      firstNameInputBox.classList.remove("active");
    }
  });
}

if (lastNameInput) {
  lastNameInput.addEventListener("input", (event) => {
    if (event.target.value) {
      lastNameInputBox.classList.add("active");
    } else {
      lastNameInputBox.classList.remove("active");
    }
  });
}

if (notificationModalContainer) {
  notificationModalContainer.addEventListener("click", () => {
    console.log("oi");
    window.location = "/auth/login";
  });
}

if (notificationModal) {
  notificationModal.addEventListener("click", (e) => {
    e.stopPropagation();
  });
}
