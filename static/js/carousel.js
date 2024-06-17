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
    this.leftButton.addEventListener('click', () => this.scrollPrevious());
    this.rightButton.addEventListener('click', () => this.scrollNext());
  }

  onResize() {
    const imageWidth = this.images.firstChild.clientWidth;
    this.images.style.left = `-${this.currentIndex * imageWidth}px`;
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
    const imageWidth = this.images.firstChild.clientWidth;
    this.images.style.left = `-${index * imageWidth}px`;
    this.dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
  }

}
