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
            const img = document.createElement('img');
            img.src = images[i];
            showAttractionImageCarousel.appendChild(img);

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
      }
    })

  showAttractionBooking.querySelectorAll('.radio').forEach(radio => {
    radio.addEventListener('click', () => {
      let price = radio.value
      showAttractionBooking.querySelector('.show-attraction-reserve-price').textContent = `新台幣${price} 元`
    })
  })
})
