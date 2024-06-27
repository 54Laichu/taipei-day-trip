document.addEventListener('DOMContentLoaded', async () => {
  const userData = JSON.parse(localStorage.getItem('userData'));
  const bookingSection = document.querySelector('#booking-section');
  const bookingSectionDefault = document.querySelector('#booking-section-default');
  const usernameContainer = document.querySelector('.booking-username-container');
  const imageContainer = document.querySelector('.booking-image-container');
  const bookingInfos = document.querySelectorAll('div.booking-info-container > p');
  const contactName = document.querySelector('#booking-contact-name');
  const contactEmail = document.querySelector('#booking-contact-email');
  const paymentContainer = document.querySelector('.booking-payment-container');
  const footerContainer = document.querySelector('.footer-container');
  const delBtn = document.querySelector("#booking-delete-btn");

  if (userData && userData.name) {
    const usernameP = document.createElement('p');
    usernameP.setAttribute("class", "booking-username");
    usernameP.innerText = `您好，${userData.name}，待預定的行程如下：`;
    usernameContainer.appendChild(usernameP);
  } else {
    console.error('User data not exist.');
  }

  const loadBooking = async () => {
    const token = localStorage.getItem('token');

    try {
      if (token) {
        const response = await fetch("/api/booking", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        const result = await response.json();

        if (response.status === 200 && result.data) {
          const resultData = result.data;
          const attraction = resultData.attraction;

          let bookTime = resultData.time;
          if (bookTime == "morning") {
            bookTime = "早上9點到下午4點";
          } else {
            bookTime = "下午4點到晚上8點";
          }

          // 將 result 資料放入 DOM element 中
          const bookingImage = document.createElement("img");
          bookingImage.src = attraction.image;
          imageContainer.appendChild(bookingImage);

          let info = [
            attraction.name,
            resultData.date,
            bookTime,
            `新台幣${resultData.price}元`,
            attraction.address
          ];
          for (let i = 0; i < bookingInfos.length; i++) {
            let span = document.createElement('span');
            span.innerText = info[i];
            bookingInfos[i].appendChild(span);
          }

          contactName.value = userData.name;
          contactEmail.value = userData.email;

          const paymentDiv = document.createElement('div');
          paymentDiv.innerText = `總價：新台幣 ${resultData.price} 元`;
          paymentContainer.prepend(paymentDiv);

          // 確認有資料後，顯示 booking-section
          bookingSection.style.display = 'block';
          bookingSectionDefault.style.display = 'none';
          footerContainer.style.height = 'auto';
        } else {
          bookingSection.style.display = 'none';
          bookingSectionDefault.style.display = "block";
          footerContainer.style.height = "100vh";
        }
      }
    } catch (e) {
      console.error(e);
    }

    try {
      if (token) {
        delBtn.addEventListener('click', async () => {
          try {
            const response = await fetch("/api/booking", {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${token}`,
              }
            });
            const result = await response.json();
            if (response.status === 200 && result.ok) {
              window.location.reload();
            } else {
              console.error('刪除失敗');
            }
          } catch (e) {
            console.error(e);
          }
        });
      }
    } catch (e) {
      console.error(e);
    }
  }

  await loadBooking();
});
