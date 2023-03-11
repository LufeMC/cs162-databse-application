const validateForm = (obj) => {
  // Check if all keys inside the obj have a non-empty value
  for (const key of Object.keys(obj)) {
    if (`${obj[key]}`.trim() === "") {
      return false;
    }
  }

  return true;
};

// Get data from form to send to backend
export function getFormData(event, formHTMLElement) {
  event.preventDefault(); // Prevents the form to submit its default action

  // Gets the value of all inputs and textareas inside the form
  const inputs = formHTMLElement.getElementsByTagName("input");
  const textareas = formHTMLElement.getElementsByTagName("textarea");
  const obj = {};

  for (const input of inputs) {
    obj[input.name] = input.value;
  }

  for (const textarea of textareas) {
    obj[textarea.name] = textarea.value;
  }

  // Validate if all inputs/textareas inside the form are filled
  if (validateForm(obj)) {
    return obj;
  } else {
    throw new Error("Please, fill all the information");
  }
}
