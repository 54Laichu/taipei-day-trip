//signinContainer.js
document.addEventListener('DOMContentLoaded', function() {
  const signInButton = document.querySelector('#sign-in-button');
  const signInContainer = document.querySelector('.sign-in-container');
  const overlay = document.querySelector('#overlay');
  const closeBtn = document.querySelector('.close-btn');
  const registerBtn = document.querySelector('#register-btn')
  const loginForm = document.querySelector('#login-form');
  const submitBtn = loginForm.querySelector("input[type='button']")
  const inputField = loginForm.querySelector("input[type='text']");
  const passwordField = loginForm.querySelector("input[type='password']");

  // view effects
  signInButton.addEventListener('click', function () {
    if (signInButton.textContent.trim() === '登入/註冊') {
      signInContainer.style.display = 'block';
      overlay.style.display = 'block';
    }
  });

  overlay.addEventListener('click', function() {
    signInContainer.style.display = 'none';
    overlay.style.display = 'none';
    inputField.value = '';
    passwordField.value = '';
  });

  closeBtn.addEventListener('click', function() {
    signInContainer.style.display = 'none';
    overlay.style.display = 'none';
    inputField.value = '';
    passwordField.value = '';
  });

  registerBtn.addEventListener('click', function(event) {
    event.preventDefault();
    const nameDiv = document.createElement('div');

    if (submitBtn.value === "登入帳戶") {
      const nameInput = document.createElement('input');
      nameInput.type = 'text';
      nameInput.name = 'name';
      nameInput.placeholder = '輸入姓名';
      nameDiv.appendChild(nameInput);
      loginForm.insertBefore(nameDiv, loginForm.firstChild);

      signInContainer.querySelector('p').textContent = '註冊會員帳號';
      registerBtn.textContent = '已經有帳戶了？點此登入';
      submitBtn.value = '註冊新帳戶';

    } else if ((submitBtn.value === "註冊新帳戶")) {
      loginForm.removeChild(loginForm.firstChild);

      signInContainer.querySelector('p').textContent = '登入會員帳號';
      registerBtn.textContent = '還沒有帳戶？點此註冊';
      submitBtn.value = '登入帳戶';
    }
  })

});
