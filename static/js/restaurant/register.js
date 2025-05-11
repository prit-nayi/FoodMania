document.addEventListener("DOMContentLoaded", () => {

  const forms = document.querySelectorAll(".form");
  const progressOptions = document.querySelectorAll(".progress-option");

  function showForm(formNumber) {
    forms.forEach((form) => {
      form.style.display = "none";
    });

    const selectedForm = document.getElementById(`form${formNumber}`);
    if (selectedForm) {
      selectedForm.style.display = "block";
    }

    progressOptions.forEach((option) => {
      option.classList.remove("active");
    });
    const activeOption = document.getElementById(`option${formNumber}`);
    if (activeOption) {
      activeOption.classList.add("active");
    }

    updateButtons(formNumber);
  }

  function changeForm(step) {
    const nextForm = currentForm + step;
    if (nextForm >= 1 && nextForm <= forms.length) {
      currentForm = nextForm;
      showForm(currentForm);
    }
  }

  function updateButtons(formNumber) {
    document.querySelectorAll(".next-btn").forEach(btn => {
      btn.style.display = formNumber === forms.length ? "none" : "block";
    });

    document.querySelectorAll(".prev-btn").forEach(btn => {
      btn.style.display = formNumber === 1 ? "none" : "block";
    });

    document.querySelectorAll(".submit-btn").forEach(btn => {
      btn.style.display = formNumber === forms.length ? "block" : "none";
    });
  }

  progressOptions.forEach((option, index) => {
    option.addEventListener("click", () => {
      currentForm = index + 1;
      showForm(currentForm);
    });
  });

  document.querySelectorAll(".next-btn").forEach(btn => {
    btn.addEventListener("click", () => changeForm(1));
  });

  document.querySelectorAll(".prev-btn").forEach(btn => {
    btn.addEventListener("click", () => changeForm(-1));
  });

  showForm(currentForm);
});

function checkPasswordMatch() 
{
     var password = document.getElementById("psw").value;
     var confirmPassword = document.getElementById("cpsw").value;
    var message = document.getElementById("passwordMessage");
    const submitButton = document.querySelector("#submit-btn");
    
    if (password !== confirmPassword) {
        message.textContent = "Passwords do not match!";
        submitButton.disabled = true;
    } else {
        message.textContent = "";
        submitButton.disabled = false;
        }
}
