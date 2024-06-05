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
}

function loadNextPage(url, container, queryString = '') {
  let currentPage = 0;
  let isLoading = false;

  function load() {
    if (isLoading) return;

    isLoading = true;

    fetch(`${url}?page=${currentPage}&${queryString}`)
      .then(response => response.json())
      .then(data => {
        if (data && data.data.length > 0) {
          data.data.forEach(attraction => {
            createAttractionCard(attraction, container);
          });

          currentPage++;
        }

        isLoading = false;
      })
      .catch(error => {
        console.error('Error:', error);
        isLoading = false;
      });
  }

  window.addEventListener('scroll', () => {
    const { scrollTop, clientHeight, scrollHeight } = document.documentElement;

    if (scrollTop + clientHeight >= scrollHeight - 100) {
      load();
    }
  });

  load();
}

export { createAttractionCard, loadNextPage };
