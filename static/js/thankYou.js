document.addEventListener('DOMContentLoaded', async () => {
  const userData = JSON.parse(localStorage.getItem('userData'));
  const usernameContainer = document.querySelector('.order-username-container');
  const orderInfoContainer = document.querySelector('.order-info-container');


  if (userData && userData.name) {
    const usernameP = document.createElement('p');
    usernameP.setAttribute("class", "order-username");
    usernameP.innerText = `您好，${userData.name}，已購買的行程資訊如下：`;
    usernameContainer.appendChild(usernameP);

    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    const params = new URLSearchParams(url.search);
    const order_number = params.get('number');
    orderInfoContainer.textContent = `訂單序號： ${order_number}`;
  } else {
    console.error('User data not exist.');
    window.location.herf = '/';
  }
});
