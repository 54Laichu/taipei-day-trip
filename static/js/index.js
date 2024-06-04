document.addEventListener('DOMContentLoaded', () => {
  // mrt list
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

  // attractions api
  const attractionsContainer = document.querySelector('.attractions');

  fetch('/api/attractions')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(infos => {
      for (const attraction of infos.data) {
        const card = document.createElement('div');
        card.classList.add('attraction-card');
        attractionsContainer.appendChild(card);

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
    })
});
