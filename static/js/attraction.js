import { Carousel } from './carousel.js';

document.addEventListener('DOMContentLoaded', () => {
  const showAttractionBooking = document.querySelector('.show-attraction-booking');
  const showAttractionImageCarouselContainer = document.querySelector('.show-attraction-image-carousel-container');
    const showAttractionImageCarousel = document.querySelector('.show-attraction-image-carousel');
  const showAttractionName = document.querySelector('.show-attraction-name');
  const showAttractionCategoryMrt = document.querySelector('.show-attraction-category-mrt');
  const showAttractionAddress = document.querySelector('.show-attraction-address');
  const showAttractionDescription = document.querySelector('.show-attraction-description');
  const showAttractionTransport = document.querySelector('.show-attraction-transport');
  const showAttractionDateInput = document.querySelector('#show-attraction-date-input');
  const showAttractionDateInputField = document.querySelector('#show-attraction-date-input-field');
  const attractionPrice = showAttractionBooking.querySelector('.show-attraction-reserve-price');
  const bookingBtn = document.querySelector('.show-attraction-reserve-button');

  let urlElement = window.location.href.split("/");
  let queryString = urlElement[urlElement.length - 1];
  let attraction_api = `/api/attraction/${queryString}`
  fetch(attraction_api)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data) {
        let attraction = data.data
        console.log(attraction)

        let images = attraction.images;
        if (images.length > 0) {
          for (let i = 0; i < images.length; i++) {
            const slide = document.createElement('div');
            slide.classList.add('show-attraction-carousel-slide');
            const img = document.createElement('img');
            img.src = images[i];
            slide.appendChild(img)
            showAttractionImageCarousel.appendChild(slide);

            const dot = document.createElement('span');
            const carouselDots = showAttractionImageCarouselContainer.querySelector('.carousel-dots');
            dot.classList.add('dot');
            carouselDots.appendChild(dot);
          }
        } else {
          const img = document.createElement('img');
          img.src = 'https://via.placeholder.com/150';
          showAttractionImageCarousel.appendChild(img);
        }

        const carousel = new Carousel(showAttractionImageCarouselContainer,
          {
            imagesSelector: '.show-attraction-image-carousel',
            dotsSelector: '.dot',
            leftButtonSelector: '.attraction-scroll-btn-left',
            rightButtonSelector: '.attraction-scroll-btn-right'
          }
        );

        if (carousel.dots) {
          carousel.dots[0].classList.add('active');
        }

        let name = attraction.name;
        showAttractionName.textContent = name;

        let category = attraction.category
        let mrt = attraction.mrt
        showAttractionCategoryMrt.textContent = `${category} at ${mrt}`;

        // seperateLine

        let description = attraction.description;
        let descriptionDiv = document.createElement('div');
        descriptionDiv.textContent = description;
        showAttractionDescription.appendChild(descriptionDiv);

        let address = attraction.address;
        let addressDiv = document.createElement('div');
        addressDiv.textContent = address;
        showAttractionAddress.appendChild(addressDiv);

        let transport = attraction.transport;
        let transportDiv = document.createElement('div');
        transportDiv.textContent = transport;
        showAttractionTransport.appendChild(transportDiv);

        // bookingBtn
        bookingBtn.addEventListener('click', async (event) => {
          event.preventDefault();
          const token = localStorage.getItem('token');
          if (token) {
            if (showAttractionDateInputField.value !== "" && attractionPrice.innerText !== "") {
              let attractionId = attraction.id;
              let date = showAttractionDateInputField.value;
              let time;
              showAttractionBooking.querySelectorAll('.radio').forEach((radio) => {
                if (radio.checked) {
                  time = radio.id;
                  return;
                }
              });
              let price = (time === "morning") ? 2000 : 2500;

              try {
                const response = await fetch("/api/booking", {
                  method: "POST",
                  headers: {
                    "Authorization": `Bearer ${token}`,
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ attractionId, date, time, price }),
                });

                const result = await response.json();
                if (response.status === 200 && result.ok) {
                  window.location.href = '/booking';
                } else {
                  console.error('預約失敗');
                }
              } catch (e) {
                console.error(e);
                alert("帳號驗證失敗");
              }
            } else {
              alert("請填寫完整預約資訊");
            }
          } else {
            alert("請先登入");
          }
        });
      }
    })

  showAttractionBooking.querySelectorAll('.radio').forEach(radio => {
    radio.addEventListener('click', () => {
      let price = radio.value
      attractionPrice.textContent = `新台幣${price} 元`
    })
  })

  showAttractionDateInput.addEventListener('click', () => {
    showAttractionDateInputField.showPicker();
  });

})
