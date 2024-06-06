import { createAttractionCard, loadNextPage } from './loadAttractions.js';
import { scrollMRT } from './scrollMRT.js';

document.addEventListener('DOMContentLoaded', () => {
  // mrt list
  scrollMRT();

  // attractions api
  const attractionsContainer = document.querySelector('.attractions');
  loadNextPage('/api/attractions', attractionsContainer, '');
});
