document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.querySelector('.search-input');
  const searchBtn = document.querySelector('.search-button');
  const attractionsContainer = document.querySelector('.attractions');

  searchBtn.addEventListener('click', () => {
    const searchValue = searchInput.value;
    if (searchValue) {
      fetch(`/api/attractions?keyword=${encodeURIComponent(searchValue)}`)
        .then(response => response.json())
        .then(data => {
          if (data && data.data.length > 0) {
            searchInput.value = '';
            attractionsContainer.innerHTML = '';
            data.data.forEach(attraction => {
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
            });
            if (data.nextPage) {
              // 把程式碼寫在這邊
            }
          } else {
            searchInput.value = '';
            searchInput.placeholder = '找不到搜尋結果';
            console.error('Data format is incorrect:', data);
          }
        });
    } else {
      console.error('Search value is empty');
    }
  });
})
