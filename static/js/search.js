import { createAttractionCard, loadNextPage, resetLoading } from './loadAttractions.js';

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.querySelector('.search-input');
  const searchBtn = document.querySelector('.search-button');
  const attractionsContainer = document.querySelector('.attractions');

  searchBtn.addEventListener('click', () => {
    const searchValue = searchInput.value;
    if (searchValue) {
      resetLoading();
      attractionsContainer.innerHTML = '';
      loadNextPage(`/api/attractions`, attractionsContainer, `keyword=${encodeURIComponent(searchValue)}`);

      searchInput.value = '';
    } else {
      searchInput.placeholder = '請在框框輸入景點';
      console.error('Search value is empty');
    }
  });
});
