let isLoading = false;
let observer = null;

function createAttractionCard(attraction, container) {
  const card = document.createElement('div');
  card.classList.add('attraction-card');
  container.appendChild(card);

  const attractionImage = document.createElement('div');
  attractionImage.classList.add('attraction-image');
  const imgURL = document.createElement('img');
  imgURL.src = attraction.images.split(",")[0];
  attractionImage.appendChild(imgURL);
  card.appendChild(attractionImage);

  const attractionName = document.createElement('div');
  attractionName.classList.add('attraction-name');
  const name = document.createElement('p');
  name.textContent = attraction.name;
  attractionName.appendChild(name);
  attractionImage.appendChild(attractionName);

  const info = document.createElement('div');
  info.classList.add('attraction-info');
  const mrt = document.createElement('div');
  mrt.classList.add('attraction-mrt');
  mrt.textContent = attraction.mrt;
  const category = document.createElement('div');
  category.classList.add('attraction-category');
  category.textContent = attraction.category;
  info.appendChild(mrt);
  info.appendChild(category);
  card.appendChild(info);

  card.addEventListener('click', () => {
    window.location.href = `/attraction/${attraction.id}`;
  });
}

function loadNextPage(url, container, queryString = '') {
  let nextPage = 0;

  function load() {
    if (isLoading || nextPage === null) return;

    isLoading = true;

    fetch(`${url}?page=${nextPage}&${queryString}`)
      .then(response => response.json())
      .then(data => {
        if (data && data.data.length > 0) {
          data.data.forEach(attraction => {
            createAttractionCard(attraction, container);
          });

          nextPage = data.nextPage;
        } else {
          nextPage = null; // No more pages to load
        }

        isLoading = false;
      })
      .catch(error => {
        console.error('Error:', error);
        isLoading = false;
      });
  }

  if (observer) {
    observer.disconnect();
  }

  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      load();
    }
  }, {
    rootMargin: '0px',
    threshold: 1.0
  });

  const bottomElement = document.querySelector('.bottom');
  observer.observe(bottomElement);
}

function resetLoading() {
  isLoading = false;
  if (observer) {
    observer.disconnect();
    observer = null;
  }
}

export { createAttractionCard, loadNextPage, resetLoading};
