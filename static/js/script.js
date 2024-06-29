window.addEventListener('resize', adjustContainerMargin);
window.addEventListener('load', adjustContainerMargin);

function adjustContainerMargin() {
    const container = document.querySelector('.container');
    const viewportHeight = window.innerHeight;
    const containerHeight = container.clientHeight;
    const marginTop = (viewportHeight - containerHeight) / 2;
    container.style.marginTop = `${marginTop}px`;
}
