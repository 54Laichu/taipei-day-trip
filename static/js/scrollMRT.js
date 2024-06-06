import { createAttractionCard, loadNextPage, resetLoading } from './loadAttractions.js';

function scrollMRT() {
  const mrtList = document.querySelector('.mrt-list');
  const scrollBtnLeft = document.querySelector('.scroll-btn.left');
  const scrollBtnRight = document.querySelector('.scroll-btn.right');
  const mrtListContainer = document.querySelector('.mrt-list-container');

  fetch('/api/mrts')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(mrts => {
      if (mrts && Array.isArray(mrts.data)) {
        mrts.data.forEach(station => {
          const p = document.createElement('p');
          p.textContent = station;
          mrtList.appendChild(p);

          p.addEventListener('click', event => {
            const attractionsContainer = document.querySelector('.attractions');
            const mrt = event.target.textContent;
            if (mrt) {
              attractionsContainer.innerHTML = '';
              resetLoading();
              loadNextPage(`/api/attractions`, attractionsContainer, `keyword=${encodeURIComponent(mrt)}`);
            }
          });
        });
      } else {
        console.error('Data format is incorrect:', data);
      }
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });

  scrollBtnLeft.addEventListener('click', () => {
    mrtListContainer.scrollBy({
      top: 0,
      left: -100,
      behavior: 'smooth'
    });
  });

  scrollBtnRight.addEventListener('click', () => {
    mrtListContainer.scrollBy({
      top: 0,
      left: 100,
      behavior: 'smooth'
    });
  });
}

export { scrollMRT };



