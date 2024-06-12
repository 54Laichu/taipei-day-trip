export class Carousel {
  constructor(container, options = {}) {
    this.container = container;
    this.images = container.querySelector(options.imagesSelector || '.images');
    this.dots = container.querySelectorAll(options.dotsSelector || '.dot');
    this.leftButton = container.querySelector(options.leftButtonSelector || '.left-btn');
    this.rightButton = container.querySelector(options.rightButtonSelector || '.right-btn');
    this.currentIndex = 0;
    this.totalImages = this.images.childElementCount;
    this.bindScrollEvent();
    this.onResize();
  window.addEventListener('resize', this.onResize.bind(this));
  }

  bindScrollEvent() {
    const leftButton = this.container.querySelector('.attraction-scroll-btn-left');
    const rightButton = this.container.querySelector('.attraction-scroll-btn-right');

    leftButton.addEventListener('click', () => this.scrollPrevious());
    rightButton.addEventListener('click', () => this.scrollNext());
  }

  onResize() {
    const containerWidth = this.container.clientWidth;
    this.images.style.left = `-${this.currentIndex * containerWidth}px`;
  }

  scrollNext() {
    this.currentIndex = (this.currentIndex + 1) % this.totalImages;
    this.showCurrentIndex(this.currentIndex);
  }

  scrollPrevious() {
    this.currentIndex = (this.currentIndex - 1 + this.totalImages) % this.totalImages;
    this.showCurrentIndex(this.currentIndex);
  }

  showCurrentIndex(index) {
    const containerWidth = this.container.clientWidth;
    this.images.style.left = `-${index * containerWidth}px`;
    this.dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
  }

}
