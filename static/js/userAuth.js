document.addEventListener('DOMContentLoaded', function () {
  const signInButton = document.querySelector('#sign-in-button');
  const signInContainer = document.querySelector('.sign-in-container');
  const overlay = document.querySelector('#overlay');
  const closeBtn = document.querySelector('.close-btn');
  const loginForm = document.querySelector('#login-form');
  const inputField = loginForm.querySelector("input[type='text']");
  const passwordField = loginForm.querySelector("input[type='password']");
  const submitBtn = loginForm.querySelector("input[type='button']");

  let messageDiv;  //先建立變數，有錯誤發生再灌入文字

  const showMessage = (message, color = 'red') => {
    if (!messageDiv) {
      messageDiv = document.createElement('div');
      messageDiv.id = 'register-message';
      signInContainer.appendChild(messageDiv);
    }
    messageDiv.style.color = color;
    messageDiv.textContent = message;
  };

  const removeMessage = () => {
    if (messageDiv) {
      messageDiv.remove();
      messageDiv = null;
    }
  }

  overlay.addEventListener('click', removeMessage);
  closeBtn.addEventListener('click', removeMessage);
  inputField.value = '';
  passwordField.value = '';

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  // ----------登入功能------------
  submitBtn.addEventListener('click', async () => {
    const email = loginForm.querySelector("input[name='email']").value;
    const password = loginForm.querySelector("input[name='password']").value;

    if (!validateEmail(email)) {
      showMessage('請輸入有效的電子郵件地址');
      return;
    }

    // PUT /api/user/signin
    if (submitBtn.value === "登入帳戶") {
      try {
        if (!email || !password) {
          showMessage('請輸入完整帳號或密碼');
          return;
        }

        const response = await fetch('/api/user/auth', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        const result = await response.json();

        if (response.status === 200 && result.token) {
          localStorage.setItem('token', result.token);
          showMessage('登入成功', 'green');
          signInButton.innerHTML = '<p>登出系統</p>';
        } else {
          showMessage(result.message || '登入失敗');
        }
      } catch (error) {
        showMessage('登入失敗，請稍後再試');
      }
    }

    //POST /api/user/signup
    else if (submitBtn.value === "註冊新帳戶") {
      const name = loginForm.querySelector("input[name='name']").value;
      try {
        if (!name || !email || !password) {
          showMessage('請輸入完整註冊資訊');
          return;
        }

        const response = await fetch('/api/user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name, email, password }),
        });

        const result = await response.json();

        if (response.status === 200 && result.token) {
          localStorage.setItem('token', result.token);
          showMessage('註冊成功', 'green');
          signInButton.innerHTML = '<p>登出系統</p>';
        } else {
          showMessage(result.message || '註冊失敗');
        }
      } catch (error) {
        showMessage('註冊失敗，請稍後再試');
      }
    }
  });

  // GET /api/user/auth
  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await fetch('/api/user/auth', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        const result = await response.json();
        if (response.status === 200 && result.data) {
          signInButton.innerHTML = '<p>登出系統</p>';
        } else {
          localStorage.removeItem('token');
          signInButton.innerHTML = '<p>登入/註冊</p>';
        }
      } catch (error) {
        localStorage.removeItem('token');
        signInButton.innerHTML = '<p>登入/註冊</p>';
      }
    } else {
      signInButton.innerHTML = '<p>登入/註冊</p>';
    }
  };

  // signout
  signInButton.addEventListener('click', () => {
    if (signInButton.textContent.trim() === '登出系統') {
      localStorage.removeItem('token');
      location.reload(true);
    } else {
      signInContainer.style.display = 'block';
      overlay.style.display = 'block';
    }
  });

  checkAuth();
});
